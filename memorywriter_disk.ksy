meta:
  id: memorywriter_disk
  title: Xerox MemoryWriter 645S disk header sector format
  imports:
    - memorywriter_sectoraddress

instances:
  diskheader:
    pos: 256 * 17 * 16
    type: diskheader_struct
  
types:
  diskheader_struct:
    seq:
      - id: label
        type: str
        encoding: UTF-8
        size: 11
      - id: firstdirsector
        type: memorywriter_sectoraddress
        doc: Adress of first sector of the file that contains the directory
      - id: lastdirsector
        type: memorywriter_sectoraddress
        doc: Adress of last sector of the file that contains the directory
      - id: unknown1
        type: u1
        repeat: expr
        repeat-expr: 14
      - id: sector_bitmap
        type: u1
        repeat: expr
        repeat-expr: 80
        doc: Sector in use bitmap, 1 bit for each sector |
             MSB of first byte represens track 0 sector 1
      - id: unknown2
        type: u1
        repeat: expr
        repeat-expr: 147
  