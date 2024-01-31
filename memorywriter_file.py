# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import memorywriter_sectoraddress
class MemorywriterFile(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class SectorheaderStruct(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.prevsector = memorywriter_sectoraddress.MemorywriterSectoraddress(self._io)
            self.nextsector = memorywriter_sectoraddress.MemorywriterSectoraddress(self._io)
            self.datasize = self._io.read_u1()
            self.fileid = self._io.read_u1()
            self.unknown = []
            for i in range(2):
                self.unknown.append(self._io.read_u1())



    class Sector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = MemorywriterFile.SectorheaderStruct(self._io, self, self._root)
            self.data = []
            for i in range(self.header.datasize):
                self.data.append(self._io.read_u1())



    class Linkedsectors(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            pass

        @property
        def sector(self):
            """The current sector."""
            if hasattr(self, '_m_sector'):
                return self._m_sector

            io = self._root._io
            _pos = io.pos()
            io.seek(self.offset)
            self._m_sector = MemorywriterFile.Sector(io, self, self._root)
            io.seek(_pos)
            return getattr(self, '_m_sector', None)

        @property
        def nextsector(self):
            """The next sector in the chain if there is one."""
            if hasattr(self, '_m_nextsector'):
                return self._m_nextsector

            if self.sector.header.nextsector.sector != 0:
                io = self._root._io
                self._m_nextsector = MemorywriterFile.Linkedsectors(self.sector.header.nextsector.offset, io, self, self._root)

            return getattr(self, '_m_nextsector', None)

        @property
        def prevsector(self):
            """The previous sector in the chain if there is one."""
            if hasattr(self, '_m_prevsector'):
                return self._m_prevsector

            if self.sector.header.prevsector.sector != 0:
                io = self._root._io
                self._m_prevsector = MemorywriterFile.Linkedsectors(self.sector.header.prevsector.offset, io, self, self._root)

            return getattr(self, '_m_prevsector', None)



