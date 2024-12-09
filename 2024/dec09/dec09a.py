import dataclasses
from typing import List, Optional

disk_blocks: List[Optional[int]] = []

with open("input", "rt") as input_file:
    empty = False
    id = 0
    for size in input_file.read():
        if size == "\n":
            continue
        size = int(size)
        for _ in range(size):
            disk_blocks.append(None if empty else id)
        if not empty:
            id += 1
            empty = True
        else:
            empty = False

print(disk_blocks)


# PART A
# just calculate the checksum without actually sorting

checksum = 0
end_pointer = len(disk_blocks) - 1
for block_pos, file_id in enumerate(disk_blocks):
    if end_pointer <= block_pos:
        break  # nothing left to do
    if file_id is not None:
        # just take file as-is
        checksum += block_pos * file_id
    else:
        # need to take from the end, skip empty files
        while disk_blocks[end_pointer] is None and end_pointer > block_pos:
            end_pointer -= 1
        if end_pointer <= block_pos:
            break  # nothing left to do
        checksum += block_pos * disk_blocks[end_pointer]
        end_pointer -= 1
print(checksum)

