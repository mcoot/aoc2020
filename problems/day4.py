import re
from typing import List, Optional, NamedTuple

from .utils import parse_paragraphs


def extract_fields(fields: List[str]):
    return {f: v for f,v in [(s.split(':')[0], s.split(':')[1]) for s in fields]}


def parse_line(line: str) -> List[str]:
    return line.strip().split(' ')


def parse_par(par: List[List[str]]):
    return extract_fields(field for line in par for field in line)


def parse_input(lines: List[str]):
    return parse_paragraphs(lines, parse_line, parse_par)


def is_doc_valid_pt1(doc):
    required_fields = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
    }
    return required_fields.issubset(doc.keys())


HEIGHT_RE = re.compile(r'^(\d+)(in|cm)$')
HAIR_COLOR_RE = re.compile(r'^#[\da-f]{6}$')
PID_RE = re.compile(r'^\d{9}$')

def doc_validation_pt2(doc):
    # Check fields exist
    if not is_doc_valid_pt1(doc):
        return 'Missing fields'

    byr = int(doc['byr'])
    iyr = int(doc['iyr'])
    eyr = int(doc['eyr'])
    hgt = doc['hgt']
    hcl = doc['hcl']
    ecl = doc['ecl']
    pid = doc['pid']

    # Validate birth year
    if byr < 1920 or byr > 2002:
        return f'Birth year {byr} invalid'

    # Validate issue year
    if iyr < 2010 or iyr > 2020:
        return f'Issue year {iyr} invalid'

    # Validate expiry year
    if eyr < 2020 or eyr > 2030:
        return f'Expiry year {eyr} invalid'

    # Validate height
    m = HEIGHT_RE.match(hgt)
    if not m:
        return False
    height_val = int(m.group(1))
    height_unit = m.group(2)
    if height_unit == 'cm' and (height_val < 150 or height_val > 193):
        return f'Height {height_val} in cm invalid'
    elif height_unit == 'in' and (height_val < 59 or height_val > 76):
        return f'Height {height_val} in in invalid'

    # Validate hair colour
    if not HAIR_COLOR_RE.match(hcl):
        return f'Hair color {hcl} invalid'

    # Validate eye colour
    if ecl not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
        return f'Eye color {ecl} invalid'

    # Validate passport id
    if not PID_RE.match(pid):
        return f'Passport id {pid} invalid'

    return None


def part1(documents):
    return sum(is_doc_valid_pt1(d) for d in documents)
    

def part2(documents):
    results = [doc_validation_pt2(d) for d in documents]
    return sum(r == None for r in results)