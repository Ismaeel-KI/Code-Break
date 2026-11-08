# helper.py
import tkinter as tk

BG, PANEL, LINE, TX, MUT, BAD, WARN = "#0a0f18", "#121b2a", "#2b3f57", "#dbe9f5", "#7d97ad", "#ff5470", "#f5c04a"

# Shared font defaults used across the project.
F = ("TkDefaultFont", 10)
FB = ("TkDefaultFont", 10, "bold")
FS = ("TkDefaultFont", 10)
FS2 = ("TkDefaultFont", 11)
FM = ("TkDefaultFont", 12)
FH = ("TkDefaultFont", 16, "bold")
FT = ("TkDefaultFont", 24, "bold")
FBIG = ("TkDefaultFont", 20, "bold")


def btn(parent, text, command, *args, background=PANEL, foreground=TX, font=None, bg=None, fg=None, **options):
    if bg is not None:
        background = bg
    if fg is not None:
        foreground = fg
    if font is None:
        font = FB

    widget = tk.Button(
        parent,
        text=text,
        command=command,
        bg=background,
        fg=foreground,
        font=font,
        padx=14,
        pady=7,
        cursor="hand2",
        relief="flat",
        **options,
    )
    return widget


def mkentry(parent, width, *args, font=None, background=BG, foreground=TX, border_color=LINE, focus_color=None, bg=None, fg=None, **options):
    if bg is not None:
        background = bg
    if fg is not None:
        foreground = fg
    if font is None:
        font = FBIG
    if focus_color is None:
        focus_color = border_color
    return tk.Entry(
        parent,
        width=width,
        font=font,
        bg=background,
        fg=foreground,
        insertbackground=foreground,
        relief="flat",
        justify="center",
        highlightthickness=1,
        highlightbackground=border_color,
        highlightcolor=focus_color,
        **options,
    )


def lbl(parent, text, *args, foreground=TX, font=None, wrap=900, background=BG, bg=None, fg=None, **options):
    if len(args) >= 1:
        foreground = args[0]
    if len(args) >= 2:
        font = args[1]
    if len(args) >= 3:
        wrap = args[2]
    if bg is not None:
        background = bg
    if fg is not None:
        foreground = fg
    if font is None:
        font = F
    return tk.Label(
        parent,
        text=text,
        bg=background,
        fg=foreground,
        font=font,
        wraplength=wrap,
        justify="center",
        **options,
    )