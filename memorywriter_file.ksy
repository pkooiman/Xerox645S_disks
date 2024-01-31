meta:
  id: memorywriter_file
  title: Xerox MemoryWriter 645S disk header file format
  imports:
    - memorywriter_sectoraddress  


types:
  sectorheader_struct:
  # Each sector that is part of a file starts with a sector header
  # The headers form a doubly linked list of the sectors that contain the file
    seq:
      - id: prevsector
        type: memorywriter_sectoraddress
        doc: Address of previous sector in file |
             set to track 0 sector 0 if this is the first sector
      - id: nextsector
        type: memorywriter_sectoraddress
        doc: Address of next sector in file |
             set to track 0 sector 0 if this is the last sector
      - id: datasize
        type: u1
        doc: Actual data bytes in this sector, not counting the header
      - id: fileid
        type: u1
        doc: An ID byte that corresponds to the ID byte in the disk directory
      - id: unknown
        type: u1
        repeat: expr
        repeat-expr: 2
  sector:
    seq:
      - id: header
        type: sectorheader_struct
        doc: The section header
      - id: data
        type: u1
        repeat: expr
        repeat-expr: header.datasize
        doc: The actual file data contained in the sector
  linkedsectors:
  # A recursive construct to follow a chain of linked sectors from beginning to end
    params:
    - id: offset
      type: u4
      doc: The offset in the image of the file's first sector
    instances:
      sector:
        io: _root._io
        pos: offset
        type: sector
        doc: The current sector
      nextsector:
        io: _root._io
        type: linkedsectors(sector.header.nextsector.offset)
        if: sector.header.nextsector.sector != 0
        doc: The next sector in the chain if there is one
      prevsector:
        io: _root._io
        type: linkedsectors(sector.header.prevsector.offset)
        if: sector.header.prevsector.sector != 0
        doc: The previous sector in the chain if there is one
  
      
  