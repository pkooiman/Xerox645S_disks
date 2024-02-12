# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class MemorywriterExec(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.chunks = []
        i = 0
        while not self._io.is_eof():
            self.chunks.append(MemorywriterExec.ChunkT(self._io, self, self._root))
            i += 1


    class ChunkHeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.chunktype = self._io.read_u1()
            self.chunksize = self._io.read_u2le()


    class ChunkT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = MemorywriterExec.ChunkHeaderT(self._io, self, self._root)
            _on = self.header.chunktype
            if _on == 6:
                self._raw_body = self._io.read_bytes(self.header.chunksize)
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = MemorywriterExec.LoadChunk(_io__raw_body, self, self._root)
            else:
                self._raw_body = self._io.read_bytes(self.header.chunksize)
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = MemorywriterExec.UnknownChunk(_io__raw_body, self, self._root)


    class LoadChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown = self._io.read_u1()
            self.loadaddress = self._io.read_u2le()
            self.data = self._io.read_bytes_full()


    class UnknownChunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes_full()



