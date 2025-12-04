text = [line.strip() for line in open("input")]
bools = [[{".": False, "@": True}[c] for c in line] for line in text]

import torch
from torch.nn.functional import conv2d

x = torch.tensor(bools)
kernel = torch.tensor([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=torch.float64)
out = conv2d(x[None, None, :, :].double(), kernel[None, None, :, :], padding="same").squeeze([0, 1])

can_remove = (x.bool() & (out < 4))
removed_total = 0
while can_remove.any():
    removed_total += can_remove.sum()
    print("Removed total:", removed_total.item())
    x &= ~can_remove
    out = conv2d(x[None, None, :, :].double(), kernel[None, None, :, :], padding="same").squeeze([0, 1])
    can_remove = (x.bool() & (out < 4))
