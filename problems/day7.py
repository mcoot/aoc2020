from dataclasses import dataclass
import re
from typing import List, Tuple

import networkx as nx

from .utils import parse_lines_regex

BAG_RE = re.compile(r'^(\w+) (\w+) bags?$')

@dataclass(frozen=True)
class Bag:
    adjective: str
    color: str


SHINY_GOLD_BAG = Bag('shiny', 'gold')


def build_object_description(raw: str) -> Bag:
    m = BAG_RE.match(raw.strip())
    if not m:
        raise ValueError(f'Failed to regex parse {raw}')
    return Bag(m.group(1), m.group(2))


def build_object_with_num(raw: str) -> Tuple[Bag, int]:
    num_split = raw.split(' ', 1)
    if num_split[0].strip() == 'no':
        return ((), 0)
    num = int(num_split[0].strip())
    return (build_object_description(num_split[1]), num)


def parse_input(lines):
    g = nx.DiGraph()
    for line in lines:
        clauses = line.strip().split(' contain ')
        subject = build_object_description(clauses[0].strip())
        objects = [build_object_with_num(o.strip().replace('.', '')) for o in clauses[1].split(', ')]
        # Add nodes for the subject and objects if they don't exist
        for o in [subject] + [o[0] for o in objects]:
            if o not in g.nodes and o != ():
                g.add_node(o)
        # Add edges
        for o in objects:
            if o[1] != 0:
                g.add_edge(subject, o[0], weight=o[1])
    return g


def part1(g: nx.DiGraph):
    source_paths = [list(nx.all_simple_paths(g, source, SHINY_GOLD_BAG)) for source in g.nodes]
    return sum(len(s) > 0 for s in source_paths)

def get_total_bags(g: nx.DiGraph(), node: Bag):
    # One for this bag
    count = 1
    for neighbour in g.adj[node]:
        weight = g.get_edge_data(node, neighbour)['weight']
        count += weight * get_total_bags(g, neighbour)
    return count


def part2(g: nx.DiGraph):
    # Subtract one for the shiny gold bag itself
    return get_total_bags(g, SHINY_GOLD_BAG) - 1