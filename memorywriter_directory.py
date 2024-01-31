# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import memorywriter_sectoraddress
class MemorywriterDirectory(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.direntries = []
        i = 0
        while not self._io.is_eof():
            self.direntries.append(MemorywriterDirectory.DirectoryEntry(self._io, self, self._root))
            i += 1


    class DirectoryEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.fileid = self._io.read_u1()
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(10), 32, False)).decode(u"UTF-8")
            self.numsectors = self._io.read_u2le()
            self.firstfilesector = memorywriter_sectoraddress.MemorywriterSectoraddress(self._io)
            self.lastfilesector = memorywriter_sectoraddress.MemorywriterSectoraddress(self._io)
            self.unknown = []
            for i in range(2):
                self.unknown.append(self._io.read_u1())




