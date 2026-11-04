# TODO: this file is broken. Repair it, run it with python, and read what it prints.
# MERCY core routine -- corrupted during the purge countdown
CORE_CODES = [88, 70, 75, 74, 82, 84, 73, 74]
OFFSET = 5
SETTINGS = {"mode": "repair", "retries": 3

def restore_ethics_core(codes, offset)
    out = []
    for c in codes:
        if c > offset:
        out.append(chr(c - offset))
    return "".join(out)

if SETTINGS["retries"] > 0
    print(restore_ethics_core(CORE_CODES, OFFSET)
