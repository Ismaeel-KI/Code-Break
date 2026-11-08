import math, os, random, string, time
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

from helper import (
    BG, PANEL, LINE, TX, MUT, BAD, WARN,
    F, FB, FS, FS2, FM, FH, FT, FBIG,
    btn, lbl, mkentry,
)
from settings import (
    GROUPS,
    FINAL_CODE,
    FINAL_CODE_CLUE,
    PAIRS,
    PUZZLE_TEXT,
)

ACC = PUZZLE_TEXT["accent"]

Node_weight = {"S": 1, "A": 8, "B": 9, "C": 9, "D": 9, "E": 1, "F": 3, "G": 4, "H": 8, "I": 6, "J": 4, "K": 7, "L": 5, "M": 2, "N": 7, "O": 3, "Q": 6, "Z": 8}

Node_pos = {"S": (38, 210), "A": (115, 75), "B": (115, 210), "C": (115, 345), "D": (205, 45), "E": (205, 175), "F": (205, 340), "G": (305, 55), "H": (305, 175),
     "I": (305, 335), "J": (420, 95), "K": (420, 280), "L": (165, 115), "M": (165, 275), "N": (260, 110), "O": (260, 275), "Q": (510, 190), "Z": (650, 210)}

Node_link = [("S","A",1),("A","D",1),("E","A",1),("F","A",1),("B","S",1),("B","C",1),("D","B",1),("B","E",2),("F","B",1),("C","S",2),("C","E",2),("C","F",1),
     ("D","E",1),("D","G",1),("D","H",1),("D","I",1),("G","E",1),("G","F",1),("F","H",2),("F","I",2),("G","H",1),("G","J",1),("G","K",1),("H","I",2),
     ("H","K",2),("I","J",1),("K","Z",1),("S","L",1),("L","A",2),("L","B",1),("L","D",1),("L","E",1),("B","M",1),("M","C",1),("M","F",2),("M","I",1),
     ("E","N",1),("N","G",2),("N","H",1),("N","J",1),("N","K",1),("F","O",1),("O","H",1),("O","I",2),("O","K",1),("J","Q",2),("K","Q",1),("H","Q",1),
     ("I","Q",1),("Q","Z",2),("J","Z",1)]

HINTS_H1 = ["Of the last pair, one is a mirage: it lets you in and never lets you out.",
            "Of the second trio, the one standing in the middle is left out in the cold.",
            "Count in the alphabet: first, fourth, seventh, sixth, eighth, eleventh. Then leave."]

def adj(a, b):
    return any((l[0] == a and l[1] == b) or (l[2] == 2 and l[0] == b and l[1] == a) for l in Node_link)

def route_valid(p):
    if len(p) != 8 or p[0] != "S" or p[-1] != "Z" or len(set(p)) != 8:
        return False
    has = lambda n: n in p
    same = any(Node_weight[p[i]] % 2 == Node_weight[p[i - 1]] % 2 for i in range(1, 8))
    return (has("A") != has("C")) and sum(map(has, "DEF")) == 2 and not (has("G") and has("I")) and not same and sum(Node_weight[n] for n in p) == 48


class Page(tk.Frame):
    """Base page: content sits in a centred body; tracks time spent here and pops hint bubbles (bottom-right)."""
    def __init__(self, app, pid, hints=()):
        super().__init__(app.root, bg=BG)
        self.app, self.pid, self.hints, self.shown = app, pid, list(hints), set()
        self.acc, self.since = 0.0, None
        self.body = tk.Frame(self, bg=BG)
        self.body.place(relx=.5, rely=.5, anchor="center")
        self.tray = tk.Frame(self, bg=BG)
        self.place(x=0, y=0, relwidth=1, relheight=1)

    def elapsed(self): 
        return self.acc + (time.time() - self.since if self.since else 0.0)

    def enter(self):
        self.since = time.time()
        self.tray.place(relx=1, rely=1, x=-14, y=-14, anchor="se")
        self.tray.lift()

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


class Home(Page):
    def __init__(self, app):
        super().__init__(app, "home")

        b = self.body

        lbl(b, PUZZLE_TEXT['title'], ACC, FH).pack()

        self.team = lbl(b, "", MUT, FB)
        self.team.pack(pady=(4, 0))
        self.timer = lbl(b, "", ACC, FB)
        self.timer.pack()

        lbl(b, "Pick a puzzle. Solve it to reveal 2 characters of the final code. Once every puzzle is solved, enter all 12 characters below.", MUT, wrap=900).pack(pady=(8, 16))

        g = tk.Frame(b, bg=BG)
        g.pack()

        self.cards = []
        for i, (gid, name, pts) in enumerate(GROUPS):

            g.columnconfigure(i, weight=1, uniform="c")

            card = tk.Frame(g, bg=PANEL, highlightthickness=2, highlightbackground=LINE, cursor="hand2")
            card.grid(row=0, column=i, padx=5, sticky="nsew")

            ws = [lbl(card, name, ACC, FB, bg=PANEL), lbl(card, PUZZLE_TEXT["labels"][i], MUT, FS, 130, bg=PANEL),
                  lbl(card, "·  ·", TX, FBIG, bg=PANEL), lbl(card, f"{pts} pts", MUT, FS, bg=PANEL)]
            for w in ws: 
                w.pack(padx=10, pady=(12, 2) if w is ws[0] else 2)

            ws[3].pack_configure(pady=(2, 12))
            for w in [card] + ws:
                 w.bind("<Button-1>", lambda e, gid=gid: app.open_group(gid))

            self.cards.append((card, ws[2], ws[3]))

        lbl(b, "FINAL CODE", ACC, FB).pack(pady=(26, 6))
        lbl(b, FINAL_CODE_CLUE, WARN, FS).pack(pady=(0, 8))
        
        row = tk.Frame(b, bg=BG)
        row.pack()

        self.slots = []
        for k in range(12):
            h = tk.Frame(row, bg=BG)
            h.pack(side="left", padx=(20 if k and k % 2 == 0 else 3, 3))

            en = tk.Entry(h, width=2, font=FBIG, justify="center", bg=BG, fg=TX, insertbackground=TX, relief="flat", bd=0, highlightthickness=0)
            en.pack()

            tk.Frame(h, height=3, bg=ACC).pack(fill="x")

            en.bind("<KeyRelease>", lambda e, k=k: self.key(k, e))
            en.bind("<FocusIn>", lambda e, en=en: en.select_range(0, "end"))

            self.slots.append(en)

        btn(b, "SUBMIT FINAL CODE", self.submit).pack(pady=(22, 6))

        self.msg = lbl(b, "", BAD)
        self.msg.pack()

    def key(self, i, e):
        en = self.slots[i]
        if e.keysym in ("BackSpace", "Delete"):
            if not en.get() and i > 0: 
                self.slots[i - 1].focus_set()
            return

        if e.keysym in ("Tab", "ISO_Left_Tab", "Shift_L", "Shift_R", "Left", "Right", "Return", "Control_L", "Control_R"): 
            return

        v = en.get().upper()
        if v:
            en.delete(0, "end")
            en.insert(0, v[-1])
            if i < 11: 
                self.slots[i + 1].focus_set()

    def submit(self):
        left = len(GROUPS) - len(self.app.done)
        if left: 
            return self.msg.config(text=f"{left} puzzle{'s' if left > 1 else ''} still unsolved. Finish every puzzle before submitting the final code.")
        if "".join(s.get().strip().upper() for s in self.slots) == FINAL_CODE:
            self.app.results("key")
        else:
            self.msg.config(text="That code is not right. Check the characters and their order.")

    def set_team(self, n): 
        self.team.config(text=f"TEAM: {n}")

    def set_clock(self, rem):
        rem = max(0, int(rem))
        self.timer.config(text=f"TIME LEFT {rem // 60:02d}:{rem % 60:02d}")

    def refresh(self):
        self.msg.config(text="")
        for i, (gid, _, pts) in enumerate(GROUPS):
            card, l3, l4 = self.cards[i]
            done = gid in self.app.done

            l3.config(text="  ".join(PAIRS[gid].upper()) if done else "·  ·")
            l4.config(text="SOLVED" if done else f"{pts} pts", fg=ACC if done else MUT)
            card.config(highlightbackground=ACC if done else LINE, cursor="arrow" if done else "hand2")


class Start(Page):
    def __init__(self, app):
        super().__init__(app, "start")

        c = self.body

        lbl(c, PUZZLE_TEXT["title"], ACC, FT).pack()
        lbl(c, PUZZLE_TEXT["tag"], MUT).pack(pady=(2, 18))
        lbl(c, PUZZLE_TEXT["premise"], TX, wrap=760).pack(pady=6)
        lbl(c, "Six puzzles. Twelve characters. 45 minutes. Every solved puzzle reveals 2 characters of the final code.", MUT, FS, wrap=760).pack(pady=6)
        lbl(c, "TEAM NAME", ACC, FB).pack(pady=(20, 4))

        self.e = mkentry(c, 26)
        self.e.pack(ipady=6) 
        self.e.bind("<Return>", lambda e: self.go()) 
        self.e.focus_set()
        self.msg = lbl(c, "", BAD)
        self.msg.pack(pady=4)

        btn(c, "START THE CLOCK", self.go).pack(pady=6)

    def go(self):
        n = self.e.get().strip()
        if not n: 
            return self.msg.config(text="Enter a team name first.")

        self.app.start(n)


class TextPage(Page):
    def __init__(self, app, pid, title, body, hints, check, extra=None, width=18):
        super().__init__(app, pid, hints); c = self.body

        self.check = check

        lbl(c, PUZZLE_TEXT["title"], MUT, FS).pack()
        lbl(c, title, ACC, FH).pack(pady=(10, 8))
        lbl(c, body).pack(pady=6)

        if extra:
            lbl(c, extra, ACC, FM, 860, bg=PANEL, padx=20, pady=18, highlightbackground=LINE, highlightthickness=1).pack(pady=14, fill="x")
        row = tk.Frame(c, bg=BG)
        row.pack(pady=10)
        self.entry = mkentry(row, width)
        self.entry.pack(side="left", ipady=6)
        self.entry.bind("<Return>", lambda e: self.submit())

        btn(row, "SUBMIT", self.submit).pack(side="left", padx=10)

        self.msg = lbl(c, "") 
        self.msg.pack()

        btn(c, "< BACK TO HOME", lambda: app.show("home"), bg=PANEL, fg=TX).pack(pady=18)

    def submit(self):
        if self.check(self.entry.get()): 
            self.app.complete(self.pid)
        else: 
            self.msg.config(text="Incorrect. Try again.", fg=BAD)

class Hard1(Page):
    SC, R, BLACK = 0.92, 20, "#000000"
    def __init__(self, app):
        super().__init__(app, "hard1")   # no timed bubbles here; hints unlock silently

        self.path, self.hn = [], 0

        left = tk.Frame(self.body, bg=BG)
        left.grid(row=0, column=0, sticky="n", padx=(0, 16))
        right = tk.Frame(self.body, bg=BG)
        right.grid(row=0, column=1, sticky="n", padx=(16, 0))

        lbl(left, "HARD 1 · BLACKOUT", ACC, FH).pack()
        lbl(left, PUZZLE_TEXT["h1_intro"], MUT, FS, 640).pack(pady=(2, 8))

        self.cv = tk.Canvas(left, width=640, height=360, bg=PANEL, highlightthickness=1, highlightbackground=LINE)
        self.cv.pack()
        self.E, self.N = {}, {}

        pt = lambda k: (Node_pos[k][0] * self.SC, Node_pos[k][1] * self.SC + 6)
        for a, b, t in Node_link:
            (x1, y1), (x2, y2) = pt(a), pt(b)
            n = math.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / n, (y2 - y1) / n

            R = self.R
            self.E[(a, b)] = self.cv.create_line(x1 + ux * (R + 1), y1 + uy * (R + 1), x2 - ux * (R + 2), y2 - uy * (R + 2), fill=LINE, width=2, arrow="last" if t == 1 else "none", arrowshape=(10, 12, 4))

        for k in Node_pos:
            x, y = pt(k)
            tag = "n_" + k
            c = self.cv.create_oval(x - self.R, y - self.R, x + self.R, y + self.R, outline=MUT, fill=BG, width=2, tags=tag)
            t1 = self.cv.create_text(x, y - 5, text=k, fill=TX, font=FB, tags=tag)
            t2 = self.cv.create_text(x, y + 9, text=str(Node_weight[k]), fill=ACC, font=FS2, tags=tag)
            self.cv.tag_bind(tag, "<Button-1>", lambda e, k=k: self.click(k))
            self.N[k] = (c, t1, t2)

        lbl(left, f"S = {PUZZLE_TEXT['h1_s']}   ·   Z = {PUZZLE_TEXT['h1_z']}", ACC, FS, 640).pack(pady=(8, 0))
        lbl(left, "Arrows indicate one-way flow; unmarked links permit passage in either direction. The extra relay stations were added after the incident "
                  "and do not necessarily belong to the surviving trace. Begin at S. Reach Z without repeating a node. Click the last node to retreat.", MUT, FS, 640).pack(pady=4)

        self.route = lbl(left, "ROUTE: —", ACC, FB, 640)
        self.route.pack()

        lbl(right, "RECOVERED DOCTRINE // FRAGMENTS", ACC, FB, 400).pack()
        lbl(right, "\n".join("○ " + r for r in PUZZLE_TEXT["h1_rules"]), TX, FS, 400).pack(pady=6)
        lbl(right, "No fragment is written in operational language. Interpret them before committing.", MUT, FS, 400).pack()

        row = tk.Frame(right, bg=BG); row.pack(pady=(12, 0))
        btn(row, "SUBMIT ROUTE", self.submit).pack(side="left", padx=6)
        btn(row, "RESET", self.reset, bg=PANEL, fg=TX).pack(side="left")

        self.hint_btn = btn(row, "HINT (LOCKED)", self.hint, bg=PANEL, fg=MUT)
        self.hint_btn.pack(side="left", padx=6)
        self.msg = lbl(right, "", ACC, wrap=400)
        self.msg.pack(pady=6)
        self.hints_box = lbl(right, "", WARN, FS, 400)
        self.hints_box.pack()

        btn(right, "< BACK TO HOME", lambda: app.show("home"), bg=PANEL, fg=TX).pack(pady=14)
        self.redraw()

    def say(self, t, bad=False): 
        self.msg.config(text=t, fg=BAD if bad else ACC)

    def eid(self, a, b): 
        return self.E.get((a, b)) or self.E.get((b, a))

    def click(self, k):
        self.say("")
        if not self.path:
            if k != "S": 
                return self.say("Every infiltration begins at S.", True)
            self.path = ["S"]
        else:
            last = self.path[-1]
            if k == last:
                if len(self.path) > 1: 
                    self.path.pop()
            elif k in self.path: 
                return self.say("Node already visited.", True)
            elif last == "Z": 
                return self.say("Route already reached Z.", True)
            elif not adj(last, k): 
                return self.say(f"No open link from {last} to {k}.", True)
            else: 
                self.path.append(k)
        self.redraw()

    def redraw(self):
        for it in self.E.values(): 
            self.cv.itemconfig(it, fill=LINE, width=2)

        for c, t1, t2 in self.N.values():
            self.cv.itemconfig(c, outline=MUT, fill=BG, width=2)
            self.cv.itemconfig(t1, fill=TX)
            self.cv.itemconfig(t2, fill=ACC)

        for i, k in enumerate(self.path):   # selected nodes: bright fill, letter and weight in black
            c, t1, t2 = self.N[k]
            last = i == len(self.path) - 1

            self.cv.itemconfig(c, fill=ACC, outline=TX if last else ACC, width=4 if last else 3)
            self.cv.itemconfig(t1, fill=self.BLACK)
            self.cv.itemconfig(t2, fill=self.BLACK)

            if i: 
                self.cv.itemconfig(self.eid(self.path[i - 1], k), fill=ACC, width=4)

        self.route.config(text="ROUTE: " + ("-".join(self.path) or "—"))

    def reset(self): 
        self.path = []
        self.say("")
        self.redraw()

    def submit(self):
        if not route_valid(self.path): 
            return self.say("ACCESS DENIED: the trace conflicts with one or more recovered fragments.", True)
        self.app.complete("hard1")

    def ready(self): 
        return self.hn < 3 and self.elapsed() >= 600 + 180 * self.hn

    def hint(self):
        if self.ready():
            self.hints_box.config(text=self.hints_box.cget("text") + f"Hint {self.hn + 1}: {HINTS_H1[self.hn]}\n")
            self.hn += 1 
            self.tick()

    def tick(self):
        r = self.ready()
        self.hint_btn.config(text="NO MORE HINTS" if self.hn >= 3 else (f"HINT {self.hn + 1}/3" if r else "HINT (LOCKED)"), bg=ACC if r else PANEL, fg=BG if r else MUT)


class Results(Page):
    def build(self, reason):
        for w in self.body.winfo_children(): 
            w.destroy()
        ok = reason == "key"

        lbl(self.body, PUZZLE_TEXT["win"] if ok else PUZZLE_TEXT["lose"], ACC if ok else BAD, FT).pack()
        lbl(self.body, f"TEAM: {self.app.team}", TX, FH).pack(pady=(6, 16))

        t = tk.Frame(self.body, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=20, pady=14); t.pack()

        for c, h in enumerate(("PUZZLE", "STATUS", "TIME", "SCORE")): 
            tk.Label(t, text=h, bg=PANEL, fg=MUT, font=FB, width=14).grid(row=0, column=c)

        total = 0.0
        for r, (gid, name, _) in enumerate(GROUPS, 1):
            d = self.app.done.get(gid)
            vals = (name, "SOLVED" if d else "NOT SOLVED", f"{int(d[0]) // 60:02d}:{int(d[0]) % 60:02d}" if d else "—", f"{d[1]:.2f}" if d else "0.00")
            total += d[1] if d else 0
            for c, v in enumerate(vals):
                tk.Label(t, text=v, bg=PANEL, fg=TX if d else MUT, font=F, width=14).grid(row=r, column=c, pady=2)

        lbl(self.body, f"TOTAL SCORE: {total:.2f}", ACC, FH).pack(pady=18)

        self.locked, self.remaining = True, 60
        self.warn = lbl(self.body, "IMPORTANT: DO NOT CLOSE THIS PROGRAM.\nYour scores are being used to evaluate the winner and the runner-up.\n"
                                   "Keep this screen open until the timer below reaches zero.", WARN, FB, 760)
        self.warn.pack(pady=(4, 8))
        self.count = lbl(self.body, "", BAD, FH)
        self.count.pack()
        self.close_btn = btn(self.body, "CLOSE", self.app.root.destroy)
        self.countdown()
        
    def countdown(self):
        if self.remaining > 0:
            self.count.config(text=f"PLEASE WAIT {self.remaining // 60:02d}:{self.remaining % 60:02d}")
            self.remaining -= 1
            self.after(1000, self.countdown)

        else:
            self.locked = False
            self.warn.config(text="Thank you for waiting. You may now close the program.", fg=ACC)
            self.count.config(text="")
            self.close_btn.pack(pady=10)
