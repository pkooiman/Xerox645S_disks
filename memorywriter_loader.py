import struct
import argparse
import os
import io
import kaitaistruct
import memorywriter_exec

def unique_file_name(base_name, extension=''):
    '''
    Creates a unique file name based on the specified base name.

    @base_name - The base name to use for the unique file name.
    @extension - The file extension to use for the unique file name.

    Returns a unique file string.
    '''
    idcount = 0

    if extension and not extension.startswith('.'):
        extension = '.%s' % extension

    fname = base_name + extension

    while os.path.exists(fname):
        fname = "%s-%d%s" % (base_name, idcount, extension)
        idcount += 1

    return fname


def LoadExe(imagefilepath):
    """Load the contents of executable image file at 'imagefilepath'"""
    
        
    stream = kaitaistruct.KaitaiStream(open(imagefilepath, 'rb'))
    exe = memorywriter_exec.MemorywriterExec(stream)

    loadedimage = bytearray(0x10000)
    firstaddress = 0x10000
    lastaddress = 0x0


    for chunk in exe.chunks:
        if (chunk.checksum + sum(chunk._raw_body) + chunk.header.chunktype + sum(chunk.header.chunksize.to_bytes(2, 'little'))) % 256 != 0:
            print("Invalid checksum for chunk")
        if chunk.header.chunktype == 6:
            
            loadaddress = chunk.body.loadaddress
            chunklen = len(chunk.body.data)
            
            if loadaddress < firstaddress:
                firstaddress = loadaddress
            if loadaddress + chunklen > lastaddress:
                lastaddress = loadaddress + chunklen
            loadedimage[loadaddress:loadaddress + len(chunk.body.data)] = chunk.body.data

    
    basename = os.path.basename(imagefilepath)
    curdir = os.getcwd()

    outname = os.path.join(curdir, f'{basename}_0x{firstaddress:04x}.loaded')
    outname = unique_file_name(outname, extension='bin')
    chunklistname = unique_file_name(outname, extension='.txt')
    with open(outname, 'wb') as f:
        f.write(loadedimage[firstaddress:lastaddress])
    
    with open(chunklistname, 'wt') as f:
        for chunk in exe.chunks:
            if chunk.header.chunktype == 6:
                f.write(f'Loadable chunk, checksum {chunk.checksum:02x}, loaded at 0x{chunk.body.loadaddress:04x} - 0x{(chunk.body.loadaddress + len(chunk.body.data)):04x}\n')
            else:
                f.write(f'Chunk type 0x{chunk.header.chunktype:02x}, checksum {chunk.checksum:02x}, data {chunk.body.data.hex()}\n')
    




if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("filename")

    args = p.parse_args()
    LoadExe(args.filename)
