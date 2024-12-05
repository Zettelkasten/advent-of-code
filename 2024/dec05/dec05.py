from typing import Tuple, List, Set, Dict

rules: List[Tuple[int, int]] = []
found_empty_line = False
check_orders = []
with open("input", "rt") as input_file:
    for line in input_file.readlines():
        line = line.strip()
        if not found_empty_line:
            if len(line) == 0:
                found_empty_line = True
            else:
                pre, post = [int(n) for n in line.split("|")]
                rules.append((pre, post))
        else:
            check_orders.append([int(n) for n in line.split(",")])

print(len(rules), "rules")
print(len(check_orders), "test inputs")

pre_to_all_posts: Dict[int, Set[int]] = {}
for pre, post in rules:
    if pre not in pre_to_all_posts:
        pre_to_all_posts[pre] = set()
    pre_to_all_posts[pre].add(post)

print(pre_to_all_posts)


def part_a(order) -> bool:
    print("order", order)
    for i, printed_page in enumerate(order):
        before_pages = set(order[:i])
        forbidden_pages = pre_to_all_posts[printed_page]
        if len(forbidden_pages & before_pages) > 0:
            print(printed_page, "->", forbidden_pages)
            return False
    return True


sum = 0
for order in check_orders:
    if part_a(order):
        sum += order[len(order) // 2]
print(sum)

def part_b(order) -> List[int]:
    # part a
    print("order", order)
    i = 0
    while i < len(order):
        printed_page = order[i]
        before_pages = set(order[:i])
        forbidden_pages = pre_to_all_posts[printed_page]
        if len(forbidden_pages & before_pages) > 0:
            print(printed_page, "->", forbidden_pages)
            # swap
            order[i], order[i - 1] = order[i - 1], order[i]
            i -= 1  # don't know where to put it, maybe we need to go aaaaall the way back
        else:
            # progress :)
            i += 1
    return order


sum = 0
for order in check_orders:
    if not part_a(order):
        new_order = part_b(order)
        sum += new_order[len(new_order) // 2]
print(sum)