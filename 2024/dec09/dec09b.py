import dataclasses
from turtledemo.penrose import start
from typing import List, Optional

@dataclasses.dataclass
class DiskBlock:
    id: Optional[int]
    start: int
    length: int

    def checksum(self):
        # could calculate this directly but plah.
        return sum(self.start + i for i in range(self.length)) * self.id

disk_blocks: List[DiskBlock] = []
disk_spaces: List[DiskBlock] = []

with open("input", "rt") as input_file:
    empty = False
    id = 0
    pos = 0
    for size in input_file.read():
        if size == "\n":
            continue
        size = int(size)
        if empty:
            disk_spaces.append(DiskBlock(start=pos, length=size, id=None))
        else:
            disk_blocks.append(DiskBlock(start=pos, length=size, id=id))
        pos += size
        if not empty:
            id += 1
            empty = True
        else:
            empty = False

print(disk_blocks)


checksum = 0
for move_file in reversed(list(disk_blocks)):
    # find space to move file to the right.
    # if it doesn't exist, don't move the file.
    space = next((space for space in disk_spaces if space.length >= move_file.length and space.start < move_file.start), None)
    if space is not None:  # found a space
        move_file.start = space.start
        space.start += move_file.length
        space.length -= move_file.length
    print(move_file)
    checksum += move_file.checksum()

print(checksum)