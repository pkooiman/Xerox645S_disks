meta:
  id: memorywriter_directory
  title: Xerox MemoryWriter 645S directory file
  imports:
    - memorywriter_sectoraddress  

seq:
# The directory is a file containing an array of directory entries
  - id: direntries
    type: directory_entry
    repeat: eos
    

types:
  directory_entry:
    seq:
      - id: fileid
        type: u1
        doc: An ID byte that corresponds to the ID byte in the file's sectors
      - id: name
        type: str
        encoding: UTF-8
        size: 10
        terminator: 0x20
        doc: File name, right padded with spaces
      - id: numsectors
        type: u2le
      - id: firstfilesector
        type: memorywriter_sectoraddress
        doc: First sector in the file
      - id: lastfilesector
        type: memorywriter_sectoraddress
        doc: Last sector in the file
      - id: unknown
        type: u1
        repeat: expr
        repeat-expr: 2
      
  