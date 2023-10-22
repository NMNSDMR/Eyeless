from tkinter import *
from random import choice
import time

frm = []
btn = []
xBtn = 16
yBtn = 16
playTime = 0
mines = xBtn * yBtn * 10 // 64
imgMark = '\u2661'
imgMine = '\u2665'
playArea = []
nMoves = 0
mrk = 0
tk = Tk()
tk.title('Achtung, Minen!')
tk.geometry(str(44 * xBtn) + 'x' + str(44 * yBtn + 10))

def play(n):
    global xBtn, yBtn, mines, nMoves, mrk, playTime
    if len(playArea) < xBtn * yBtn:
        return ()
    nMoves += 1
    if nMoves == 1:
        playTime = time.time()
        i = 0
        while i < mines:
            j = choice(range(0, xBtn * yBtn))
            if j != n and playArea[j] != -1:
                playArea[j] = -1
                i += 1
        for i in range(0, xBtn * yBtn):
            if playArea[i] != -1:
                k = 0
                if i not in range(0, xBtn * yBtn, xBtn):
                    if playArea[i - 1] == -1:
                        k += 1
                    if i > xBtn - 1:
                        if playArea[i - xBtn - 1] == -1:
                            k += 1
                    if i < xBtn * yBtn - xBtn:
                        if playArea[i + xBtn - 1] == -1:
                            k += 1
                if i not in range(-1, xBtn * yBtn, xBtn):
                    if playArea[i + 1] == -1:
                        k += 1
                    if i > xBtn - 1:
                        if playArea[i - xBtn + 1] == -1:
                            k += 1
                    if i < xBtn * yBtn - xBtn:
                        if playArea[i + xBtn + 1] == -1:
                            k += 1
                if i > xBtn - 1:
                    if playArea[i - xBtn] == -1:
                        k += 1
                if i < xBtn * yBtn - xBtn:
                    if playArea[i + xBtn] == -1:
                        k += 1
                playArea[i] = k
    if btn[n].cget('text') == imgMark:
        mrk -= 1
        tk.title('Achtung, ' + str(mines - mrk) + ' Minen!')
    btn[n].config(text=playArea[n], state=DISABLED, bg='black', fg='white')
    if playArea[n] == 0:
        btn[n].config(text=' ')
    elif playArea[n] == -1:
        btn[n].config(text=imgMine)
        if nMoves <= (xBtn * yBtn - mines) or mines >= mrk:
            nMoves = 32000
            chainReaction(0)
            tk.title('Your game is over.')
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:
        tk.title('You win! ' + str(int(time.time() - playTime)) + ' сек')
        winner(0)

def chainReaction(j):
    if j <= len(playArea):
        for i in range(j, xBtn * yBtn):
            if playArea[i] == -1 and btn[i].cget('text') == ' ':
                btn[i].config(text=imgMine)
                btn[i].flash()
                tk.bell()
                tk.after(50, chainReaction, i + 1)
                break

def winner(j):
    if j <= len(playArea):
        for i in range(j, xBtn * yBtn):
            if playArea[i] == 0:
                btn[i].config(state=NORMAL, text='☺', fg='white')
                btn[i].flash()
                tk.bell()
                btn[i].config(text=' ', state=DISABLED)
                tk.after(50, winner, i + 1)
                break

def marker(n):
    global mrk, mines, playTime
    if btn[n].cget('state') != 'disabled':
        if btn[n].cget('text') == imgMark:
            btn[n].config(text=' ')
            mrk -= 1
        else:
            btn[n].config(text=imgMark, fg='white')
            mrk += 1
        tk.title('Achtung, ' + str(mines - mrk) + ' Minen!')
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:
        tk.title('You win! ' + str(int(time.time() - playTime)) + ' сек')
        winner(0)

def newGame():
    global xBtn, yBtn, mines, nMoves, mrk
    mines = xBtn * yBtn * 10 // 64
    nMoves = 0
    mrk = 0
    playArea.clear()
    if len(btn) != 0:
        for i in range(0, len(btn)):
            btn[i].destroy()
        btn.clear()
        for i in range(0, len(frm)):
            frm[i].destroy()
        frm.clear()
    playground()
    tk.title('Achtung, ' + str(mines - mrk) + ' Minen!')

def set5x5():
    global xBtn, yBtn
    xBtn = 5
    yBtn = 5
    newGame()

def set8x8():
    global xBtn, yBtn
    xBtn = 8
    yBtn = 8
    newGame()

def set10x14():
    global xBtn, yBtn
    xBtn = 10
    yBtn = 14
    newGame()

def set16x16():
    global xBtn, yBtn
    xBtn = 16
    yBtn = 16
    newGame()

def set32x32():
    global xBtn, yBtn
    xBtn = 32
    yBtn = 32
    newGame()

def playground():
    global xBtn, yBtn
    for i in range(0, yBtn):
        frm.append(Frame())
        frm[i].pack(expand=YES, fill=BOTH)
        for j in range(0, xBtn):
            btn.append(Button(frm[i], text=' ', font=('mono', 16, 'bold'),
                              width=1, height=1, padx=0, pady=0))
    for i in range(0, xBtn * yBtn):
        if xBtn * yBtn > 256:
            btn[i].config(font=('mono', 8, 'normal'))
        btn[i].config(command=lambda n=i: play(n))
        btn[i].bind('<Button-3>', lambda event, n=i: marker(n))
        btn[i].pack(side=LEFT, expand=YES, fill=BOTH, padx=0, pady=0)
        btn[i].update()
        playArea.append(0)

frmTop = Frame()
frmTop.pack(expand=YES, fill=BOTH)
Label(frmTop, text=' Новая игра:  ', fg='white').pack(side=LEFT, expand=NO, fill=X, anchor=N)
Button(frmTop, text='5x5', font=(16),
       command=set5x5, fg='black', bg='white').pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='8x8', font=(16),
       command=set8x8, fg='black', bg='white').pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='10x14', font=(16),
       command=set10x14, fg='black', bg='white').pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='16x16', font=(16),
       command=set16x16, fg='black', bg='white').pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='32x32', font=(16),
       command=set32x32, fg='black', bg='white').pack(side=LEFT, expand=YES, fill=X, anchor=N)

mainloop()
