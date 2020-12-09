from typing import Dict, List, Set

def parse_input(lines):
    return [int(line.strip()) for line in lines]


def is_target_possible(possibilities: Dict[int, Set[int]], target: int) -> bool:
    for v in possibilities.values():
        if target in v:
            return True
    return False


def find_first_nonsum(preamble_size: int, nums: List[int]):
    for i in range(preamble_size, len(nums)):
        current_preamble = nums[i-preamble_size:i]
        # Maps indices into the nums list onto the things that can be created from that
        # If we have duplicate targets, we don't really care for the reverse mapping
        possibilities: Dict[int, Set[int]] = {i: set(x + y for y in current_preamble) 
                                          for i, x 
                                          in enumerate(current_preamble)}
        # Is the current number we're up to possible?
        current_num = nums[i]
        if not is_target_possible(possibilities, current_num):
            # Not possible, we're done
            return (i, current_num)

    return None




def part1(nums):
    preamble_size = nums[0]
    nums = nums[1:]
    return find_first_nonsum(preamble_size, nums)[1]


# Cumulative sums of the list to this point
def cum_sums(nums: List[int]):
    total = 0
    result = []
    for num in nums:
        total += num
        result.append(total)
    return result


# Given cumulative sums, get the sums of a range by subtracting the cumulative sum 
# from one below the lower bound
def find_indices_which_sum_to(sums: List[int], target: int):
    for lower in range(1, len(sums)):
        for upper in range(lower + 1, len(sums)):
            sum_diff = sums[upper] - sums[lower - 1]
            if sum_diff == target:
                return (lower, upper)
    return None


def part2(nums):
    first_nonsum = part1(nums)
    nums = nums[1:]
    sums = cum_sums(nums)
    (i, j) = find_indices_which_sum_to(sums, first_nonsum)
    return min(nums[i:j+1]) + max(nums[i:j+1])
    
