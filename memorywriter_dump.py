import struct
import argparse
import os
import io
import kaitaistruct
import memorywriter_disk
import memorywriter_file
import memorywriter_directory

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

def ReadFile(stream, offset):
    """Read a file from disk image represented by Kaitai stream 'stream', 
       first sector is at offset 'offset'."""
    filedata = bytearray()
    sectorlist = memorywriter_file.MemorywriterFile.Linkedsectors(offset, stream)
    filedata.extend(sectorlist.sector.data)

    listtail = sectorlist.nextsector
    while listtail:
        filedata.extend(listtail.sector.data)
        listtail = listtail.nextsector

    return filedata

def GetDiskHeader(imagefilepath):
    """Read the disk header from disk image file at imagefilepath."""
    stream = kaitaistruct.KaitaiStream(open(imagefilepath, 'rb'))
    disk = memorywriter_disk.MemorywriterDisk(stream)
    diskheader = disk.diskheader
    disk.close()
    return diskheader

def GetDirectory(imagefilepath, offset):
    """Read the directory from disk image file at 'imagefilepath', 
       first sector is at offset 'offset'."""
    
    #First get the complete file containing the directory
    stream = kaitaistruct.KaitaiStream(open(imagefilepath, 'rb'))
    dirdata = ReadFile(stream, offset)
    
    #Now parse the directory file
    stream = kaitaistruct.KaitaiStream(io.BytesIO(dirdata))
    return memorywriter_directory.MemorywriterDirectory(stream)
    

def DumpDisk(imagefilepath):
    """Dump the contents of disk image file at 'imagefilepath'"""
    diskheader = GetDiskHeader(imagefilepath)
    diroffset = diskheader.firstdirsector.offset

    directory = GetDirectory(imagefilepath, diroffset)
    PrintDirectory(directory)


    basename = os.path.basename(imagefilepath)
    curdir = os.getcwd()

    outdir = os.path.join(curdir, '_' + basename)
    output_directory = unique_file_name(outdir, extension='extracted')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    stream = kaitaistruct.KaitaiStream(open(imagefilepath, 'rb'))
    for e in directory.direntries:
        filedata = ReadFile(stream, e.firstfilesector.offset)
        if not e.name:
            fname = '__empty__'
        else:
            fname = e.name
        with open(f'{output_directory}/{fname}', 'wb') as f:
            f.write(filedata)
    
    
def PrintDirectory(dir):
    direntries = dir.direntries
    print(f'Name       ID Start  End    #sect Unk')
    for e in direntries:
        print(f'{e.name:10} {e.fileid:02x} T{e.firstfilesector.track:02}S{e.firstfilesector.sector:02} T{e.lastfilesector.track:02}S{e.lastfilesector.sector:02} {e.numsectors:03}   {e.unknown[0]:02x}{e.unknown[1]:02x}')



if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("filename")

    args = p.parse_args()
    DumpDisk(args.filename)
