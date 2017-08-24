import sys

result, ref = sys.argv[1:]

result_lines = open(result).readlines()
ref_lines = open(ref).readlines()
for p, r in zip(result_lines, ref_lines):
    p_cells = p.strip().split('\t')
    r_cells = r.strip().split('\t')
    error_sign = ""
    if len(r_cells) < 5:
        continue
    else:
        if p_cells[0] != r_cells[0]:
            error_sign = "**"
        print("{} {} {} {} {}".format(error_sign, p_cells[0], r_cells[0], r_cells[3], 
                                         r_cells[13]))
