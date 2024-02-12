meta:
  id: memorywriter_exec


seq:
  - id: chunks
    type: chunk_t 
    repeat: eos


types:
  chunk_header_t:
    seq:
      - id: chunktype
        type: u1
      - id: chunksize
        type: u2le
  chunk_t:
    seq:
      - id: header
        type: chunk_header_t
      - id: body
        size: header.chunksize
        type:
          switch-on: header.chunktype
          cases:
            6: load_chunk
            _: unknown_chunk
      
            
  load_chunk:
    seq:
      - id: unknown
        type: u1
      - id: loadaddress
        type: u2le
      - id: data
        size-eos: true
  unknown_chunk:
    seq:
      - id: data
        size-eos: true
  