# TODO: this file is broken. Repair it, run it with python, and read what it prints.
# Elevator controller 7 -- tampered with by the rival firm
FLOOR_CODES = [87, 82, 83, 73, 79, 82, 82, 85]
OFFSET = 3
SETTINGS = {"mode": "repair", "retries": 3

def unlock_elevator(codes, offset)
    out = []
    for c in codes:
        if c > offset:
        out.append(chr(c - offset))
    return "".join(out)

if SETTINGS["retries"] > 0
    print(unlock_elevator(FLOOR_CODES, OFFSET)
