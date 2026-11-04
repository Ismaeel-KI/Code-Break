#!/usr/bin/env python3
"""Escape-room puzzle console. Run:  python <this file>   (needs Python 3.8+ with tkinter)"""
import math, os, random, string, time
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

# ======================= SETTINGS YOU MAY EDIT =======================
# The 2 characters each puzzle reveals on the home page:
PAIRS = {
    "easy1": "LT",
    "easy2": "EZ",
    "medium1": "RA",
    "medium2": "PV",
    "hard1": "D7",
    "hard2": "L7",
}
# The order the pairs must be typed into the final code (list every puzzle id once; reorder freely):
KEY_ORDER = ["medium1", "medium2", "hard2", "easy1", "hard1", "easy2"]
# True = invent new random pairs every launch (they are printed in the console window); False = use PAIRS above.
RANDOM_CODE_EACH_RUN = False
# Where the puzzle files live (shown to the team on the Medium 1, Medium 2 and Hard 2 pages). Edit if yours are elsewhere:
def desktop():
    home = os.path.expanduser("~")
    return next((p for p in (os.path.join(home, "Desktop"), os.path.join(home, "OneDrive", "Desktop")) if os.path.isdir(p)), home)
DB_PATH = os.path.join(desktop(), "system_logs.db")
DEAD_CODE_PATH = os.path.join(desktop(), "life_support.py")
# Answers that depend on your audio file / database:
EASY2_MESSAGE = 'THE CAPTAIN SEALED MODULE NINE'      # plaintext the team must decrypt (capital letters and spaces)
EASY2_SHIFT = 9                                      # Caesar rotation used to encrypt it
MEDIUM1_ANSWER = 'AIRLOCK'                              # what the team finds in the Medium 1 audio
MEDIUM2_ANSWER = 'O2-LEAK-310'                           # the key the team finds in the database
# Clue shown on the home page above the final code:
FINAL_CODE_CLUE = "You need a lock before you find the key!"
# ======================================================================

S = {'slug': 'helios9',
 'title': 'HELIOS-9',
 'tag': 'THE SPACE STATION  //  48 hours of silence',
 'accent': '#ff8a4c',
 'premise': 'The station Helios-9 has lost power and its crew went silent 48 hours ago. You are the rescue crew with one oxygen reserve '
            'and limited time. Solve every puzzle, collect the twelve-character restart code and bring the main reactor back online.',
 'win': 'REACTOR ONLINE',
 'lose': 'OXYGEN DEPLETED',
 'labels': ["Captain's Terminal", 'Final Transmission', 'Static Source', 'Crew Logs', 'Reactor Power Route', 'Life Support'],
 'e1_intro': "Vault 0101 // The captain's terminal is locked. Its keypad displays ASCII codes but only accepts letters. Translate all 10 "
             'codes into capital letters to unlock it.',
 'e1_h1': "The terminal's oxygen counter is ticking. Try A-65, B-66, etc...",
 'e1_h2': 'Ohh my God, how long will you take for this?? Your oxygen reserve is not infinite. Look for a table, you figure out which one '
          'but search for a table.',
 'e2_intro': "Ghost Signal // The crew's last transmission was scrambled with an old cipher before it was sent. Decode the full message "
             'and type it below.',
 'e2_h1': 'The crew used a basic scramble: every letter was pushed the same number of places along the alphabet. Shift them back, one step '
          'at a time.',
 'e2_h2': 'The cipher is named after an emperor, even out here... do you know someone who has a salad named after them??',
 'm1_intro': 'Ghost Signal // You will find what you are searching for in the Audio file in the desktop. The crew hid their last word '
             'inside the radio static. Enter it below.',
 'm1_h1': 'You are using the wrong sense of yours! Space is silent anyway... you probably should search for sonic',
 'm1_h2': 'The crew wrapped their last word in layers. You should probably add a Steganography layer',
 'm2_intro': 'Data Graveyard // You will have to search for the data within a bulk of data. You will find what you are searching for in '
             "the database located in {db}. Helios-9's crew logged every system event aboard the station. Exactly one record marks the "
             'very first system that failed. The event happened between 2026-10-16 18:00:00 and 2026-10-17 00:00:00. Enter the '
             'personal_key stored on that record below.',
 'm2_h1': "The flight engineer always noticed things first: it is probably John Doe's personal key.",
 'm2_h2': "Among John Doe's records in that time range, look for the one whose detail column says: coolant pressure dropped to zero",
 'h1_intro': "Helios-9's power grid is in pieces. Several relay modules were added after the crew went silent; some are decoys, some are "
             'one-way, and the old schematic cannot be trusted. Route power from the emergency battery to the main reactor before the '
             'oxygen runs out.',
 'h1_s': 'EMERGENCY BATTERY',
 'h1_z': 'MAIN REACTOR',
 'h1_rules': ['THE BATTERY AND THE REACTOR ARE NOT NEGOTIABLE.',
              'THE EIGHTH FOOTPRINT MUST BE THE LAST.',
              'THE MIRROR PAIR CANNOT COEXIST.',
              'THREE WATCHERS SHARE A FREQUENCY; TWO MAY ANSWER, NEVER ONE OR THREE.',
              'THE GREEN-EYED PAIR MUST NEVER SHARE A TRACE.',
              'AFTER EACH STEP, THE SIGNAL MUST CHANGE ITS PARITY.',
              "THE SUM OF THE TRACE IS THE ONLY THING THE REACTOR'S IGNITION CHECK ACCEPTS: 48."],
 'h2_intro': 'Dead Code // The life-support program crashed and took the air with it. You should probably fix the python program located '
             'in {dead}. Run it once it works and enter what it prints.',
 'h2_h1': 'What is taking so long? Every minute costs oxygen. Check for the indentations, colons, brackets, etc... ',
 'h2_h2': "i don't know how to help you man, Mission Control is out of range. You are on your own!",
 'h2_answer': 'AIRFLOW'}

TOTAL = 45 * 60
ACC = S["accent"]
BG, PANEL, LINE, TX, MUT, BAD, WARN = "#0a0f18", "#121b2a", "#2b3f57", "#dbe9f5", "#7d97ad", "#ff5470", "#f5c04a"
GROUPS = [("easy1", "EASY 1", 100), ("easy2", "EASY 2", 100), ("medium1", "MEDIUM 1", 200),
          ("medium2", "MEDIUM 2", 200), ("hard1", "HARD 1", 300), ("hard2", "HARD 2", 300)]
if RANDOM_CODE_EACH_RUN:
    PAIRS = {g[0]: "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=2)) for g in GROUPS}
    print("Pairs this run:", PAIRS, "| final code:", "".join(PAIRS[k] for k in KEY_ORDER))
if sorted(KEY_ORDER) != sorted(g[0] for g in GROUPS) or any(len(PAIRS.get(g[0], "")) != 2 for g in GROUPS):
    raise SystemExit("Settings error: KEY_ORDER must list each puzzle once, and every puzzle needs exactly 2 characters in PAIRS.")
FINAL_CODE = "".join(PAIRS[k] for k in KEY_ORDER).upper()

# ---------------------------------------------------------------- puzzle files
FILES = {"db": DB_PATH, "dead": DEAD_CODE_PATH}

def check_files():
    for p in FILES.values():
        if not os.path.exists(p): print(f"Warning: puzzle file not found: {p}")

def caesar(text, k):
    return "".join(chr((ord(c) - 65 + k) % 26 + 65) if c.isalpha() else c for c in text)

# ---------------------------------------------------------------- hard 1 graph data
D = {"S": 1, "A": 8, "B": 9, "C": 9, "D": 9, "E": 1, "F": 3, "G": 4, "H": 8, "I": 6, "J": 4, "K": 7, "L": 5, "M": 2, "N": 7, "O": 3, "Q": 6, "Z": 8}
P = {"S": (38, 210), "A": (115, 75), "B": (115, 210), "C": (115, 345), "D": (205, 45), "E": (205, 175), "F": (205, 340), "G": (305, 55), "H": (305, 175),
     "I": (305, 335), "J": (420, 95), "K": (420, 280), "L": (165, 115), "M": (165, 275), "N": (260, 110), "O": (260, 275), "Q": (510, 190), "Z": (650, 210)}
L = [("S","A",1),("A","D",1),("E","A",1),("F","A",1),("B","S",1),("B","C",1),("D","B",1),("B","E",2),("F","B",1),("C","S",2),("C","E",2),("C","F",1),
     ("D","E",1),("D","G",1),("D","H",1),("D","I",1),("G","E",1),("G","F",1),("F","H",2),("F","I",2),("G","H",1),("G","J",1),("G","K",1),("H","I",2),
     ("H","K",2),("I","J",1),("K","Z",1),("S","L",1),("L","A",2),("L","B",1),("L","D",1),("L","E",1),("B","M",1),("M","C",1),("M","F",2),("M","I",1),
     ("E","N",1),("N","G",2),("N","H",1),("N","J",1),("N","K",1),("F","O",1),("O","H",1),("O","I",2),("O","K",1),("J","Q",2),("K","Q",1),("H","Q",1),
     ("I","Q",1),("Q","Z",2),("J","Z",1)]
HINTS_H1 = ["Of the last pair, one is a mirage: it lets you in and never lets you out.",
            "Of the second trio, the one standing in the middle is left out in the cold.",
            "Count in the alphabet: first, fourth, seventh, sixth, eighth, eleventh. Then leave."]

def adj(a, b):
    return any((l[0] == a and l[1] == b) or (l[2] == 2 and l[0] == b and l[1] == a) for l in L)

def route_valid(p):
    if len(p) != 8 or p[0] != "S" or p[-1] != "Z" or len(set(p)) != 8:
        return False
    has = lambda n: n in p
    same = any(D[p[i]] % 2 == D[p[i - 1]] % 2 for i in range(1, 8))
    return (has("A") != has("C")) and sum(map(has, "DEF")) == 2 and not (has("G") and has("I")) and not same and sum(D[n] for n in p) == 48

def norm(s): return " ".join(s.upper().split())

# ---------------------------------------------------------------- UI helpers
def btn(parent, text, cmd, bg=None, fg=None):
    b = tk.Label(parent, text=text, bg=bg or ACC, fg=fg or BG, font=FB, padx=14, pady=7, cursor="hand2")
    b.bind("<Button-1>", lambda e: cmd())
    return b

def mkentry(parent, width, font=None):
    return tk.Entry(parent, width=width, font=font or FM, bg=PANEL, fg=TX, insertbackground=TX, relief="flat", justify="center",
                    highlightthickness=1, highlightbackground=LINE, highlightcolor=ACC)

def lbl(parent, text, fg=TX, font=None, wrap=900, **kw):
    return tk.Label(parent, text=text, bg=kw.pop("bg", BG), fg=fg, font=font or F, wraplength=wrap, justify="center", **kw)

class Page(tk.Frame):
    """Base page: content sits in a centred body; tracks time spent here and pops hint bubbles (bottom-right)."""
    def __init__(self, app, pid, hints=()):
        super().__init__(app.root, bg=BG)
        self.app, self.pid, self.hints, self.shown = app, pid, list(hints), set()
        self.acc, self.since = 0.0, None
        self.body = tk.Frame(self, bg=BG); self.body.place(relx=.5, rely=.5, anchor="center")
        self.tray = tk.Frame(self, bg=BG)
        self.place(x=0, y=0, relwidth=1, relheight=1)
    def elapsed(self): return self.acc + (time.time() - self.since if self.since else 0.0)
    def enter(self):
        self.since = time.time()
        self.tray.place(relx=1, rely=1, x=-14, y=-14, anchor="se"); self.tray.lift()
    def leave(self):
        if self.since:
            self.acc += time.time() - self.since
            self.since = None
    def tick(self):
        for sec, text in self.hints:
            if self.elapsed() >= sec and sec not in self.shown:
                self.shown.add(sec); self.bubble(text)
    def bubble(self, text):
        b = tk.Label(self.tray, text=text, bg=PANEL, fg=WARN, bd=1, relief="solid", wraplength=320, justify="left", padx=12, pady=9, font=FS, cursor="hand2")
        b.pack(anchor="e", pady=3); b.bind("<Button-1>", lambda e: b.destroy()); self.tray.lift()

class Start(Page):
    def __init__(self, app):
        super().__init__(app, "start"); c = self.body
        lbl(c, S["title"], ACC, FT).pack()
        lbl(c, S["tag"], MUT).pack(pady=(2, 18))
        lbl(c, S["premise"], TX, wrap=760).pack(pady=6)
        lbl(c, "Six puzzles. Twelve characters. 45 minutes. Every solved puzzle reveals 2 characters of the final code.", MUT, FS, wrap=760).pack(pady=6)
        lbl(c, "TEAM NAME", ACC, FB).pack(pady=(20, 4))
        self.e = mkentry(c, 26); self.e.pack(ipady=6); self.e.bind("<Return>", lambda e: self.go()); self.e.focus_set()
        self.msg = lbl(c, "", BAD); self.msg.pack(pady=4)
        btn(c, "START THE CLOCK", self.go).pack(pady=6)
    def go(self):
        n = self.e.get().strip()
        if not n: return self.msg.config(text="Enter a team name first.")
        self.app.start(n)

class Home(Page):
    def __init__(self, app):
        super().__init__(app, "home"); b = self.body
        lbl(b, S["title"], ACC, FH).pack()
        self.team = lbl(b, "", MUT, FB); self.team.pack(pady=(4, 0))
        self.timer = lbl(b, "", ACC, FB); self.timer.pack()
        lbl(b, "Pick a puzzle. Solve it to reveal 2 characters of the final code. Once every puzzle is solved, enter all 12 characters below.", MUT, wrap=900).pack(pady=(8, 16))
        g = tk.Frame(b, bg=BG); g.pack()
        self.cards = []
        for i, (gid, name, pts) in enumerate(GROUPS):
            g.columnconfigure(i, weight=1, uniform="c")
            card = tk.Frame(g, bg=PANEL, highlightthickness=2, highlightbackground=LINE, cursor="hand2")
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            ws = [lbl(card, name, ACC, FB, bg=PANEL), lbl(card, S["labels"][i], MUT, FS, 130, bg=PANEL),
                  lbl(card, "·  ·", TX, FBIG, bg=PANEL), lbl(card, f"{pts} pts", MUT, FS, bg=PANEL)]
            for w in ws: w.pack(padx=10, pady=(12, 2) if w is ws[0] else 2)
            ws[3].pack_configure(pady=(2, 12))
            for w in [card] + ws: w.bind("<Button-1>", lambda e, gid=gid: app.open_group(gid))
            self.cards.append((card, ws[2], ws[3]))
        lbl(b, "FINAL CODE", ACC, FB).pack(pady=(26, 6))
        lbl(b, FINAL_CODE_CLUE, WARN, FS).pack(pady=(0, 8))
        row = tk.Frame(b, bg=BG); row.pack()
        self.slots = []
        for k in range(12):
            h = tk.Frame(row, bg=BG); h.pack(side="left", padx=(20 if k and k % 2 == 0 else 3, 3))
            en = tk.Entry(h, width=2, font=FBIG, justify="center", bg=BG, fg=TX, insertbackground=TX, relief="flat", bd=0, highlightthickness=0)
            en.pack(); tk.Frame(h, height=3, bg=ACC).pack(fill="x")
            en.bind("<KeyRelease>", lambda e, k=k: self.key(k, e)); en.bind("<FocusIn>", lambda e, en=en: en.select_range(0, "end"))
            self.slots.append(en)
        btn(b, "SUBMIT FINAL CODE", self.submit).pack(pady=(22, 6))
        self.msg = lbl(b, "", BAD); self.msg.pack()
    def key(self, i, e):
        en = self.slots[i]
        if e.keysym in ("BackSpace", "Delete"):
            if not en.get() and i > 0: self.slots[i - 1].focus_set()
            return
        if e.keysym in ("Tab", "ISO_Left_Tab", "Shift_L", "Shift_R", "Left", "Right", "Return", "Control_L", "Control_R"): return
        v = en.get().upper()
        if v:
            en.delete(0, "end"); en.insert(0, v[-1])
            if i < 11: self.slots[i + 1].focus_set()
    def submit(self):
        left = len(GROUPS) - len(self.app.done)
        if left: return self.msg.config(text=f"{left} puzzle{'s' if left > 1 else ''} still unsolved. Finish every puzzle before submitting the final code.")
        if "".join(s.get().strip().upper() for s in self.slots) == FINAL_CODE: self.app.results("key")
        else: self.msg.config(text="That code is not right. Check the characters and their order.")
    def set_team(self, n): self.team.config(text=f"TEAM: {n}")
    def set_clock(self, rem):
        rem = max(0, int(rem)); self.timer.config(text=f"TIME LEFT {rem // 60:02d}:{rem % 60:02d}")
    def refresh(self):
        self.msg.config(text="")
        for i, (gid, _, pts) in enumerate(GROUPS):
            card, l3, l4 = self.cards[i]; done = gid in self.app.done
            l3.config(text="  ".join(PAIRS[gid].upper()) if done else "·  ·")
            l4.config(text="SOLVED" if done else f"{pts} pts", fg=ACC if done else MUT)
            card.config(highlightbackground=ACC if done else LINE, cursor="arrow" if done else "hand2")

class TextPage(Page):
    def __init__(self, app, pid, title, body, hints, check, extra=None, width=18):
        super().__init__(app, pid, hints); c = self.body
        self.check = check
        lbl(c, S["title"], MUT, FS).pack()
        lbl(c, title, ACC, FH).pack(pady=(10, 8))
        lbl(c, body).pack(pady=6)
        if extra:
            lbl(c, extra, ACC, FM, 860, bg=PANEL, padx=20, pady=18, highlightbackground=LINE, highlightthickness=1).pack(pady=14, fill="x")
        row = tk.Frame(c, bg=BG); row.pack(pady=10)
        self.entry = mkentry(row, width); self.entry.pack(side="left", ipady=6); self.entry.bind("<Return>", lambda e: self.submit())
        btn(row, "SUBMIT", self.submit).pack(side="left", padx=10)
        self.msg = lbl(c, ""); self.msg.pack()
        btn(c, "< BACK TO HOME", lambda: app.show("home"), bg=PANEL, fg=TX).pack(pady=18)
    def submit(self):
        if self.check(self.entry.get()): self.app.complete(self.pid)
        else: self.msg.config(text="Incorrect. Try again.", fg=BAD)

class Hard1(Page):
    SC, R, BLACK = 0.92, 20, "#000000"
    def __init__(self, app):
        super().__init__(app, "hard1")   # no timed bubbles here; hints unlock silently
        self.path, self.hn = [], 0
        left = tk.Frame(self.body, bg=BG); left.grid(row=0, column=0, sticky="n", padx=(0, 16))
        right = tk.Frame(self.body, bg=BG); right.grid(row=0, column=1, sticky="n", padx=(16, 0))
        lbl(left, "HARD 1 · BLACKOUT", ACC, FH).pack()
        lbl(left, S["h1_intro"], MUT, FS, 640).pack(pady=(2, 8))
        self.cv = tk.Canvas(left, width=640, height=360, bg=PANEL, highlightthickness=1, highlightbackground=LINE); self.cv.pack()
        self.E, self.N = {}, {}
        pt = lambda k: (P[k][0] * self.SC, P[k][1] * self.SC + 6)
        for a, b, t in L:
            (x1, y1), (x2, y2) = pt(a), pt(b); n = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / n, (y2 - y1) / n; R = self.R
            self.E[(a, b)] = self.cv.create_line(x1 + ux * (R + 1), y1 + uy * (R + 1), x2 - ux * (R + 2), y2 - uy * (R + 2), fill=LINE, width=2,
                                                 arrow="last" if t == 1 else "none", arrowshape=(10, 12, 4))
        for k in P:
            x, y = pt(k); tag = "n_" + k
            c = self.cv.create_oval(x - self.R, y - self.R, x + self.R, y + self.R, outline=MUT, fill=BG, width=2, tags=tag)
            t1 = self.cv.create_text(x, y - 5, text=k, fill=TX, font=FB, tags=tag)
            t2 = self.cv.create_text(x, y + 9, text=str(D[k]), fill=ACC, font=FS2, tags=tag)
            self.cv.tag_bind(tag, "<Button-1>", lambda e, k=k: self.click(k)); self.N[k] = (c, t1, t2)
        lbl(left, f"S = {S['h1_s']}   ·   Z = {S['h1_z']}", ACC, FS, 640).pack(pady=(8, 0))
        lbl(left, "Arrows indicate one-way flow; unmarked links permit passage in either direction. The extra relay stations were added after the incident "
                  "and do not necessarily belong to the surviving trace. Begin at S. Reach Z without repeating a node. Click the last node to retreat.", MUT, FS, 640).pack(pady=4)
        self.route = lbl(left, "ROUTE: —", ACC, FB, 640); self.route.pack()
        lbl(right, "RECOVERED DOCTRINE // FRAGMENTS", ACC, FB, 400).pack()
        lbl(right, "\n".join("○ " + r for r in S["h1_rules"]), TX, FS, 400).pack(pady=6)
        lbl(right, "No fragment is written in operational language. Interpret them before committing.", MUT, FS, 400).pack()
        row = tk.Frame(right, bg=BG); row.pack(pady=(12, 0))
        btn(row, "SUBMIT ROUTE", self.submit).pack(side="left", padx=6)
        btn(row, "RESET", self.reset, bg=PANEL, fg=TX).pack(side="left")
        self.hint_btn = btn(row, "HINT (LOCKED)", self.hint, bg=PANEL, fg=MUT); self.hint_btn.pack(side="left", padx=6)
        self.msg = lbl(right, "", ACC, wrap=400); self.msg.pack(pady=6)
        self.hints_box = lbl(right, "", WARN, FS, 400); self.hints_box.pack()
        btn(right, "< BACK TO HOME", lambda: app.show("home"), bg=PANEL, fg=TX).pack(pady=14)
        self.redraw()
    def say(self, t, bad=False): self.msg.config(text=t, fg=BAD if bad else ACC)
    def eid(self, a, b): return self.E.get((a, b)) or self.E.get((b, a))
    def click(self, k):
        self.say("")
        if not self.path:
            if k != "S": return self.say("Every infiltration begins at S.", True)
            self.path = ["S"]
        else:
            last = self.path[-1]
            if k == last:
                if len(self.path) > 1: self.path.pop()
            elif k in self.path: return self.say("Node already visited.", True)
            elif last == "Z": return self.say("Route already reached Z.", True)
            elif not adj(last, k): return self.say(f"No open link from {last} to {k}.", True)
            else: self.path.append(k)
        self.redraw()
    def redraw(self):
        for it in self.E.values(): self.cv.itemconfig(it, fill=LINE, width=2)
        for c, t1, t2 in self.N.values():
            self.cv.itemconfig(c, outline=MUT, fill=BG, width=2); self.cv.itemconfig(t1, fill=TX); self.cv.itemconfig(t2, fill=ACC)
        for i, k in enumerate(self.path):   # selected nodes: bright fill, letter and weight in black
            c, t1, t2 = self.N[k]; last = i == len(self.path) - 1
            self.cv.itemconfig(c, fill=ACC, outline=TX if last else ACC, width=4 if last else 3)
            self.cv.itemconfig(t1, fill=self.BLACK); self.cv.itemconfig(t2, fill=self.BLACK)
            if i: self.cv.itemconfig(self.eid(self.path[i - 1], k), fill=ACC, width=4)
        self.route.config(text="ROUTE: " + ("-".join(self.path) or "—"))
    def reset(self): self.path = []; self.say(""); self.redraw()
    def submit(self):
        if not route_valid(self.path): return self.say("ACCESS DENIED: the trace conflicts with one or more recovered fragments.", True)
        self.app.complete("hard1")
    def ready(self): return self.hn < 3 and self.elapsed() >= 600 + 180 * self.hn
    def hint(self):
        if self.ready():
            self.hints_box.config(text=self.hints_box.cget("text") + f"Hint {self.hn + 1}: {HINTS_H1[self.hn]}\n"); self.hn += 1; self.tick()
    def tick(self):
        r = self.ready()
        self.hint_btn.config(text="NO MORE HINTS" if self.hn >= 3 else (f"HINT {self.hn + 1}/3" if r else "HINT (LOCKED)"), bg=ACC if r else PANEL, fg=BG if r else MUT)

class Results(Page):
    def build(self, reason):
        for w in self.body.winfo_children(): w.destroy()
        ok = reason == "key"
        lbl(self.body, S["win"] if ok else S["lose"], ACC if ok else BAD, FT).pack()
        lbl(self.body, f"TEAM: {self.app.team}", TX, FH).pack(pady=(6, 16))
        t = tk.Frame(self.body, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=20, pady=14); t.pack()
        for c, h in enumerate(("PUZZLE", "STATUS", "TIME", "SCORE")): tk.Label(t, text=h, bg=PANEL, fg=MUT, font=FB, width=14).grid(row=0, column=c)
        total = 0.0
        for r, (gid, name, _) in enumerate(GROUPS, 1):
            d = self.app.done.get(gid)
            vals = (name, "SOLVED" if d else "NOT SOLVED", f"{int(d[0]) // 60:02d}:{int(d[0]) % 60:02d}" if d else "—", f"{d[1]:.2f}" if d else "0.00")
            total += d[1] if d else 0
            for c, v in enumerate(vals): tk.Label(t, text=v, bg=PANEL, fg=TX if d else MUT, font=F, width=14).grid(row=r, column=c, pady=2)
        lbl(self.body, f"TOTAL SCORE: {total:.2f}", ACC, FH).pack(pady=18)
        self.locked, self.remaining = True, 60
        self.warn = lbl(self.body, "IMPORTANT: DO NOT CLOSE THIS PROGRAM.\nYour scores are being used to evaluate the winner and the runner-up.\n"
                                   "Keep this screen open until the timer below reaches zero.", WARN, FB, 760)
        self.warn.pack(pady=(4, 8))
        self.count = lbl(self.body, "", BAD, FH); self.count.pack()
        self.close_btn = btn(self.body, "CLOSE", self.app.root.destroy)
        self.countdown()
    def countdown(self):
        if self.remaining > 0:
            self.count.config(text=f"PLEASE WAIT {self.remaining // 60:02d}:{self.remaining % 60:02d}")
            self.remaining -= 1; self.after(1000, self.countdown)
        else:
            self.locked = False
            self.warn.config(text="Thank you for waiting. You may now close the program.", fg=ACC)
            self.count.config(text=""); self.close_btn.pack(pady=10)

class App:
    def __init__(self):
        global F, FB, FS, FS2, FM, FH, FT, FBIG
        self.root = tk.Tk(); self.root.title(S["title"]); self.root.geometry("1150x780"); self.root.minsize(1120, 720); self.root.configure(bg=BG)
        fams = set(tkfont.families(self.root))
        fam = next((f for f in ("Consolas", "Menlo", "DejaVu Sans Mono", "Courier New") if f in fams), "Courier")
        F, FB, FS, FS2 = (fam, 11), (fam, 11, "bold"), (fam, 10), (fam, 8)
        FM, FH, FT, FBIG = (fam, 18, "bold"), (fam, 20, "bold"), (fam, 30, "bold"), (fam, 22, "bold")
        check_files()
        self.team, self.t0, self.done, self.cur, self.over = "", None, {}, None, False
        fmt = lambda s: s.format(**FILES)
        H = lambda a, b: [(120, fmt(a)), (300, fmt(b))]
        letters = "".join(random.choices(string.ascii_uppercase, k=10))
        lab = S["labels"]
        self.pages = {"start": Start(self), "home": Home(self),
            "easy1": TextPage(self, "easy1", f"EASY 1 · {lab[0].upper()}", fmt(S["e1_intro"]), H(S["e1_h1"], S["e1_h2"]),
                              lambda a: a.upper().replace(" ", "") == letters, extra="   ".join(str(ord(c)) for c in letters), width=14),
            "easy2": TextPage(self, "easy2", f"EASY 2 · {lab[1].upper()}", fmt(S["e2_intro"]), H(S["e2_h1"], S["e2_h2"]),
                              lambda a: norm(a) == norm(EASY2_MESSAGE), extra=caesar(EASY2_MESSAGE.upper(), EASY2_SHIFT), width=40),
            "medium1": TextPage(self, "medium1", f"MEDIUM 1 · {lab[2].upper()}", fmt(S["m1_intro"]), H(S["m1_h1"], S["m1_h2"]),
                                lambda a: norm(a) == norm(MEDIUM1_ANSWER), width=22),
            "medium2": TextPage(self, "medium2", f"MEDIUM 2 · {lab[3].upper()}", fmt(S["m2_intro"]), H(S["m2_h1"], S["m2_h2"]),
                                lambda a: a.strip().upper() == MEDIUM2_ANSWER.strip().upper(), width=22),
            "hard1": Hard1(self),
            "hard2": TextPage(self, "hard2", "HARD 2 · DEAD CODE", fmt(S["h2_intro"]), H(S["h2_h1"], S["h2_h2"]),
                              lambda a: norm(a) == S["h2_answer"], width=22),
            "results": Results(self, "results")}
        self.show("start")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(500, self.loop)
    def on_close(self):
        if self.over and self.pages["results"].locked:
            messagebox.showwarning("Please wait", "Please do not close the program yet.\nYour scores are being used to evaluate the winner and the runner-up.")
        else:
            self.root.destroy()
    def show(self, name):
        if self.cur: self.cur.leave()
        self.cur = self.pages[name]; self.cur.lift(); self.cur.enter(); self.cur.tick()
    def start(self, name):
        self.team, self.t0 = name, time.time(); self.pages["home"].set_team(name); self.pages["home"].refresh(); self.show("home")
    def open_group(self, gid):
        if gid not in self.done and not self.over: self.show(gid)
    def complete(self, pid):
        if self.over: return
        pts = next(g[2] for g in GROUPS if g[0] == pid)
        self.show("home")
        secs = self.pages[pid].elapsed()
        self.done[pid] = (secs, pts / max(secs / 60.0, 1.0))
        self.pages["home"].refresh()
    def results(self, reason):
        if self.over: return
        self.over = True; self.pages["results"].build(reason); self.show("results")
    def loop(self):
        if self.t0 and not self.over:
            rem = TOTAL - (time.time() - self.t0); self.pages["home"].set_clock(rem)
            if rem <= 0: self.results("time")
            elif self.cur: self.cur.tick()
        self.root.after(500, self.loop)

if __name__ == "__main__":
    App().root.mainloop()
