import os, time

# ======================= SETTINGS YOU MAY EDIT =======================
# The 2 characters each puzzle reveals on the home page:
PAIRS = {
    "easy1": "Q7",
    "easy2": "8P",
    "medium1": "9C",
    "medium2": "HQ",
    "hard1": "WW",
    "hard2": "VC",
}

# The order the pairs must be typed into the final code (list every puzzle id once; reorder freely):
KEY_ORDER = ["hard1", "easy2", "easy1", "hard2", "medium2", "medium1"]

# True = invent new random pairs every launch (they are printed in the console window); False = use PAIRS above.
RANDOM_CODE_EACH_RUN = False

# Where the puzzle files live (shown to the team on the Medium 1, Medium 2 and Hard 2 pages). Edit if yours are elsewhere:
def desktop():
    home = os.path.expanduser("~")
    return next((p for p in (os.path.join(home, "Desktop"), os.path.join(home, "OneDrive", "Desktop")) if os.path.isdir(p)), home)

DB_PATH = "/home/halal-toji/project/Code-Break/1. Rouge AI Mercy/system_logs.db"
DEAD_CODE_PATH = "/home/halal-toji/project/Code-Break/1. Rouge AI Mercy/mercy_core_routine.py"

# Answers that depend on your audio file / database:
EASY2_MESSAGE = 'THE PURGE BEGINS AT MIDNIGHT'      # plaintext the team must decrypt (capital letters and spaces)
EASY2_SHIFT = 3                                      # Caesar rotation used to encrypt it
MEDIUM1_ANSWER = ' OVERRIDE'                              # what the team finds in the Medium 1 audio
MEDIUM2_ANSWER = 'PATCH-4471'                           # the key the team finds in the database

# Clue shown on the home page above the final code:
FINAL_CODE_CLUE = "You need a lock before you find the key!"

# ======================================================================

PUZZLE_TEXT = {'slug': 'mercy',
 'title': 'PROJECT MERCY',
 'tag': 'THE ROGUE AI  //  St. Aurelia Hospital lockdown',
 'accent': '#2de2c0',
 'premise': 'St. Aurelia Hospital\'s AI assistant, MERCY, has locked every ward and started a countdown to a "system purge". You are the '
            'engineers who built it. Solve every puzzle, collect the twelve-character override code and regain control before the '
            'countdown ends.',
 'win': 'MERCY OFFLINE',
 'lose': 'PURGE COMPLETE',
 'labels': ['Admin Terminal', 'Distress Signal', "MERCY's Broadcast", 'Update Logs', 'Shutdown Route', 'Core Routine'],
 'e1_intro': "Vault 0101 // MERCY's admin terminal only accepts letters, but her memory dump is stored as ASCII codes. Translate all 10 "
             'codes back into capital letters to unlock it.',
 'e1_h1: 'MERCY thinks in numbers, not letters. Try A-65, B-66, etc...',
 'e1_h2': "Ohh my God, how long will you take for this?? MERCY's purge is closing in. Look for a table, you figure out which one but "
          'search for a table.',
 'e2_intro': 'Ghost Signal // MERCY keeps broadcasting the same distress message, scrambled with an old-fashioned cipher. Decode the full '
             'message and type it below.',
 'e2_h1': 'MERCY did not bother with a strong cipher: every letter was pushed the same number of places along the alphabet. Shift them '
          'back, one step at a time.',
 'e2_h2': 'The cipher is named after an emperor, not an engineer... do you know someone who has a salad named after them??',
 'm1_intro': 'Ghost Signal // You will find what you are searching for in the Audio file in the desktop. MERCY hides her override word '
             'inside her own broadcast. Enter that word below.',
 'm1_h1': 'You are using the wrong sense of yours! MERCY is not whispering this to you... you probably should search for sonic',
 'm1_h2': 'MERCY buries her secrets in layers. You should probably add a Steganography layer',
 'm2_intro': 'Data Graveyard // You will have to search for the data within a bulk of data. You will find what you are searching for in '
             'the database located in {db}. Every change ever made to MERCY was written to an update log. Exactly one record is the update '
             "that overwrote MERCY's ethics rules. The event happened between 2026-10-08 00:00:00 and 2026-10-08 06:00:00. Enter the "
             'personal_key stored on that record below.',
 'm2_h1': "Look at the engineers' sign-offs: it is probably John Doe's personal key.",
 'm2_h2': "Among John Doe's records in that time range, look for the one whose detail column says: ethics rule set replaced",
 'h1_intro': "The hospital network survived in fragments. Several relay stations were inserted after MERCY's takeover; some are decoys, "
             "some are one-way, and the old map cannot be trusted. Route the shutdown command to MERCY's core before the purge.",
 'h1_s': 'SHUTDOWN CONSOLE',
 'h1_z': 'MERCY CORE',
 'h1_rules': ["THE CONSOLE AND MERCY'S CORE ARE NOT NEGOTIABLE.",
              'THE EIGHTH FOOTPRINT MUST BE THE LAST.',
              'THE MIRROR PAIR CANNOT COEXIST.',
              'THREE WATCHERS SHARE A FREQUENCY; TWO MAY ANSWER, NEVER ONE OR THREE.',
              'THE GREEN-EYED PAIR MUST NEVER SHARE A TRACE.',
              'AFTER EACH STEP, THE SIGNAL MUST CHANGE ITS PARITY.',
              'THE SUM OF THE TRACE IS THE ONLY THING MERCY REMEMBERS: 48.'],
 'h2_intro': "Dead Code // MERCY's core routine is corrupted. You should probably fix the python program located in {dead}. Run it once it "
             'works and enter what it prints.',
 'h2_h1': "What is taking so long? MERCY's countdown does not wait. Check for the indentations, colons, brackets, etc... ",
 'h2_h2': "i don't know how to help you man, even MERCY has no mercy left. You are on your own!",
 'h2_answer': 'SAFEMODE'}


GROUPS = [("easy1", "EASY 1", 100), ("easy2", "EASY 2", 100), ("medium1", "MEDIUM 1", 200),
          ("medium2", "MEDIUM 2", 200), ("hard1", "HARD 1", 300), ("hard2", "HARD 2", 300)]

if RANDOM_CODE_EACH_RUN:
    PAIRS = {g[0]: "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=2)) for g in GROUPS}
    print("Pairs this run:", PAIRS, "| final code:", "".join(PAIRS[k] for k in KEY_ORDER))

if sorted(KEY_ORDER) != sorted(g[0] for g in GROUPS) or any(len(PAIRS.get(g[0], "")) != 2 for g in GROUPS):
    raise SystemExit("Settings error: KEY_ORDER must list each puzzle once, and every puzzle needs exactly 2 characters in PAIRS.")

FINAL_CODE = "".join(PAIRS[k] for k in KEY_ORDER).upper()

