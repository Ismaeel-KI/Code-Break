# TODO: this file is broken. Repair it, run it with python, and read what it prints.
# Evidence recovery script -- broken by the intruder
EVIDENCE_CODES = [86, 73, 87, 88, 83, 86, 73, 72]
OFFSET = 4
SETTINGS = {"mode": "repair", "retries": 3

def restore_evidence(codes, offset)
    out = []
    for c in codes:
        if c > offset:
        out.append(chr(c - offset))
    return "".join(out)

if SETTINGS["retries"] > 0
    print(restore_evidence(EVIDENCE_CODES, OFFSET)
