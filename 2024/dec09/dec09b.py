import dataclasses
from turtledemo.penrose import start
from typing import List, Optional

@dataclasses.dataclass
class DiskBlock:
    id: int
    start: int
    length: int

    def checksum(self):
        # could calculate this directly but plah.
        return sum(self.start + i for i in range(self.length)) * self.id

disk_blocks: List[DiskBlock] = []

with open("small_input", "rt") as input_file:
    empty = False
    id = 0
    pos = 0
    for size in input_file.read():
        if size == "\n":
            continue
        size = int(size)
        if not empty:
            disk_blocks.append(DiskBlock(start=pos, length=size, id=id))
        pos += size
        if not empty:
            id += 1
            empty = True
        else:
            empty = False

print(disk_blocks)


checksum = 0
left_block_id = 0
while left_block_id < len(disk_blocks):
    block = disk_blocks[left_block_id]
    # just take file as-is
    print(block)
    checksum += block.checksum()
    # no next block available
    if left_block_id == len(disk_blocks) - 1:
        break
    # need to take from the end, skip empty files
    next_block = disk_blocks[left_block_id + 1]
    block_start = block.start
    next_free_start = block.start + block.length
    for right_block_id, other_block in reversed(list(enumerate(disk_blocks[left_block_id + 1:], start=left_block_id + 1))):
        space = next_block.start - next_free_start
        if other_block.length <= space:
            # take this one
            other_block.start = next_free_start
            checksum += other_block.checksum()
            print(other_block)
            del disk_blocks[right_block_id]
            # there could be another, so don't directly break. but because they always grow smaller, we don't
            # need to look at the full list again
            next_free_start += other_block.length
    left_block_id += 1
print(checksum)
