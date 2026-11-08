#!/usr/bin/env python3
"""Escape-room puzzle console. Run:  python <this file>   (needs Python 3.8+ with tkinter)"""
import math, os, random, string, time
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

from pages import Page, Start, Home, TextPage, Hard1, Results
from helper import btn, lbl, mkentry, BG, PANEL, LINE, TX, MUT, BAD, WARN
from settings import (
    DB_PATH,
    DEAD_CODE_PATH,
    EASY2_MESSAGE,
    EASY2_SHIFT,
    GROUPS,
    MEDIUM1_ANSWER,
    MEDIUM2_ANSWER,
    PUZZLE_TEXT,
)

# ======================================================================
TOTAL = 45 * 60
ACC = PUZZLE_TEXT["accent"]

# ---------------------------------------------------------------- puzzle files
FILES = {"db": DB_PATH, "dead": DEAD_CODE_PATH}

def check_files():
    for p in FILES.values():
        if not os.path.exists(p): 
            print(f"Warning: puzzle file not found: {p}")

def caesar(text, k):
    return "".join(chr((ord(c) - 65 + k) % 26 + 65) if c.isalpha() else c for c in text)

# ---------------------------------------------------------------- hard 1 graph data

def norm(s):
    return " ".join(s.upper().split())


class App:
    def __init__(self):
        global F, FB, FS, FS2, FM, FH, FT, FBIG

        self.root = tk.Tk()
        self.root.title(PUZZLE_TEXT["title"])
        self.root.geometry("1150x780")
        self.root.minsize(1120, 720)
        self.root.configure(bg=BG)

        check_files()

        self.team, self.t0, self.done, self.cur, self.over = "", None, {}, None, False
        
        self.easy1_letters = "".join(random.choices(string.ascii_uppercase, k=10))
        self.pages = self.build_pages()

        self.show("start")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(500, self.loop)
    
    def format_text(self, text):
            return text.format(**FILES)

    def make_hints(self, first, second):
        return [
            (120, self.format_text(first)),
            (300, self.format_text(second)),
        ]

    def is_easy1_answer(self, answer):
        return answer.upper().replace(" ", "") == self.easy1_letters

    def is_easy2_answer(self, answer):
        return norm(answer) == norm(EASY2_MESSAGE)

    def is_medium1_answer(self, answer):
        return norm(answer) == norm(MEDIUM1_ANSWER)

    def is_medium2_answer(self, answer):
        return answer.strip().upper() == MEDIUM2_ANSWER.strip().upper()

    def is_hard2_answer(self, answer):
        return norm(answer) == PUZZLE_TEXT["h2_answer"]

    def build_pages(self):
        labels = PUZZLE_TEXT["labels"]

        return {
            "start": Start(self),
            "home": Home(self),
            "easy1": TextPage(
                self,
                "easy1",
                f"EASY 1 · {labels[0].upper()}",
                self.format_text(PUZZLE_TEXT["e1_intro"]),
                self.make_hints(PUZZLE_TEXT["e1_h1"], PUZZLE_TEXT["e1_h2"]),
                self.is_easy1_answer,
                extra="   ".join(str(ord(char)) for char in self.easy1_letters),
                width=14,
            ),
            "easy2": TextPage(
                self,
                "easy2",
                f"EASY 2 · {labels[1].upper()}",
                self.format_text(PUZZLE_TEXT["e2_intro"]),
                self.make_hints(PUZZLE_TEXT["e2_h1"], PUZZLE_TEXT["e2_h2"]),
                self.is_easy2_answer,
                extra=caesar(EASY2_MESSAGE.upper(), EASY2_SHIFT),
                width=40,
            ),
            "medium1": TextPage(
                self,
                "medium1",
                f"MEDIUM 1 · {labels[2].upper()}",
                self.format_text(PUZZLE_TEXT["m1_intro"]),
                self.make_hints(PUZZLE_TEXT["m1_h1"], PUZZLE_TEXT["m1_h2"]),
                self.is_medium1_answer,
                width=22,
            ),
            "medium2": TextPage(
                self,
                "medium2",
                f"MEDIUM 2 · {labels[3].upper()}",
                self.format_text(PUZZLE_TEXT["m2_intro"]),
                self.make_hints(PUZZLE_TEXT["m2_h1"], PUZZLE_TEXT["m2_h2"]),
                self.is_medium2_answer,
                width=22,
            ),
            "hard1": Hard1(self),
            "hard2": TextPage(
                self,
                "hard2",
                "HARD 2 · DEAD CODE",
                self.format_text(PUZZLE_TEXT["h2_intro"]),
                self.make_hints(PUZZLE_TEXT["h2_h1"], PUZZLE_TEXT["h2_h2"]),
                self.is_hard2_answer,
                width=22,
            ),
            "results": Results(self, "results"),
        }

    def on_close(self):
        if self.over and self.pages["results"].locked:
            messagebox.showwarning("Please wait", "Please do not close the program yet.\nYour scores are being used to evaluate the winner and the runner-up.")
        else:
            self.root.destroy()
    def show(self, name):
        if self.cur: 
            self.cur.leave()
        self.cur = self.pages[name]
        self.cur.lift()
        self.cur.enter()
        self.cur.tick()

    def start(self, name):
        self.team, self.t0 = name, time.time()
        self.pages["home"].set_team(name)
        self.pages["home"].refresh()
        self.show("home")

    def open_group(self, gid):
        if gid not in self.done and not self.over: 
            self.show(gid)

    def complete(self, pid):
        if self.over: 
            return
        pts = next(g[2] for g in GROUPS if g[0] == pid)
        self.show("home")
        secs = self.pages[pid].elapsed()
        self.done[pid] = (secs, pts / max(secs / 60.0, 1.0))
        self.pages["home"].refresh()

    def results(self, reason):
        if self.over: 
            return
        self.over = True
        self.pages["results"].build(reason)
        self.show("results")

    def loop(self):
        if self.t0 and not self.over:
            rem = TOTAL - (time.time() - self.t0)
            self.pages["home"].set_clock(rem)
            if rem <= 0: 
                self.results("time")
            elif self.cur: 
                self.cur.tick()
                
        self.root.after(500, self.loop)

if __name__ == "__main__":
    App().root.mainloop()
