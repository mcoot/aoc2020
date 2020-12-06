import re


def identity(x):
    return x


def parse_paragraphs(lines, transform_line=None, transform_par=None):
    # Optional transform functions
    if transform_line is None:
        transform_line = identity
    if transform_par is None:
        transform_par = identity

    pars = []
    cur_par = []
    for line in lines:
        if line.strip() == '':
            pars.append(transform_par(cur_par))
            cur_par = []
        else:
            cur_par.append(transform_line(line.strip()))
    if len(cur_par) > 0:
        pars.append(transform_par(cur_par))
    return pars


def parse_lines_regex(lines, regex: re.Pattern, transform_match=None):
    if transform_match is None:
        # Return match groups as a tuple by default
        transform_match = lambda m: m.groups()
    results = []
    for line in lines:
        m = regex.match(line.strip())
        if not m:
            raise ValueError(f'Failed to match {line}')
        results.append(transform_match(m))
    return results