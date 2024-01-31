meta:
  id: memorywriter_sectoraddress
  title: Xerox MemoryWriter 645S sector addressing


  # Sectors are addressed by track and sector within a track 
  # Tracks are numbered from 0-39 
  # Sectors in a track are numbered from 1-16
seq:
  - id: track
    type: u1
  - id: sector
    type: u1
instances:
  offset:
    value: 'sector == 0 ? 0: 256 * (track * 16 + (sector - 1))'
    doc: Offset in image corresponding to the sector address
