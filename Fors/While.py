from tkinter import *
import tkinter as tk
import time
# a = entry
# #Vars
# S = 0
# M = 0
# H = 0
# for i in range(a):
#     S += 1
#     time.sleep(0.01)
#     #Convert 60 seconds to 1 minute
#     if(S==60):
#         M += 1
#         S = 0 
#     if(M==60):
#     #convert 60 minute ro 1 hour
#         H += 1
#         M = 0 
#     if(M==0 and H==0):     
#         print(S,'Sec')
#     elif(M!=0 and H==0):
#         print(M,'Min',S,'Sec')
#     else:
#         print(H,'Hour',M,'Min',S,'Sec')


window =Tk()
window.title("Жёский таймер")
window.minsize(300,250)
window.resizable(False, False)

S = 0
M = 0
H = 0


entry = tk.Entry(window)

input = entry.get()

def simplelogic():
     for i in range(input):
      S += 1
     time.sleep(0.01)
     #Convert 60 seconds to 1 minute
     if(S==60):
         M += 1
         S = 0 
     if(M==60):
     #convert 60 minute ro 1 hour
         H += 1
         M = 0 

def printtime():
    if(M==0 and H==0):     
      return S
    elif(M!=0 and H==0):
      return M,S
    else:
      return H,M,S

label = tk.Label(window, text=printtime)

label.pack()
entry.pack()



window.mainloop()
