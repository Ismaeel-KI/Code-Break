# TODO: this file is broken. Repair it, run it with python, and read what it prints.
# Helios-9 life-support program -- crashed 48 hours ago
O2_CODES = [72, 80, 89, 77, 83, 86, 94]
OFFSET = 7
SETTINGS = {"mode": "repair", "retries": 3

def restart_life_support(codes, offset)
    out = []
    for c in codes:
        if c > offset:
        out.append(chr(c - offset))
    return "".join(out)

if SETTINGS["retries"] > 0
    print(restart_life_support(O2_CODES, OFFSET)
