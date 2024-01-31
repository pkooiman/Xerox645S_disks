# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import memorywriter_sectoraddress
class MemorywriterDisk(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class DiskheaderStruct(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.label = (self._io.read_bytes(11)).decode(u"UTF-8")
            self.firstdirsector = memorywriter_sectoraddress.MemorywriterSectoraddress(self._io)
            self.lastdirsector = memorywriter_sectoraddress.MemorywriterSectoraddress(self._io)
            self.unknown1 = []
            for i in range(14):
                self.unknown1.append(self._io.read_u1())

            self.sector_bitmap = []
            for i in range(80):
                self.sector_bitmap.append(self._io.read_u1())

            self.unknown2 = []
            for i in range(147):
                self.unknown2.append(self._io.read_u1())



    @property
    def diskheader(self):
        if hasattr(self, '_m_diskheader'):
            return self._m_diskheader

        _pos = self._io.pos()
        self._io.seek(((256 * 17) * 16))
        self._m_diskheader = MemorywriterDisk.DiskheaderStruct(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_diskheader', None)


