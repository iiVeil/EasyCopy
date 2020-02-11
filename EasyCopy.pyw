import tkinter
from tkinter import messagebox
import time
import json
import os
import sys
import clipboard
import psutil
import keyboard
import win32ui

App = tkinter.Tk()
App.withdraw()
num = 0 
PROCNAME = "EasyCopy.exe"
for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        num += 1
        if num > 1:
            messagebox.showinfo("Error", "EasyCopy is already running! Use ALT+SHIFT+V to show it!")
            sys.exit()

showing = True

if not os.path.exists("bin"):
    os.mkdir("bin")
if not os.path.exists("bin/json"):
    os.mkdir("bin/json")
if not os.path.exists("bin/json/texts.dat"):
    f = open("bin/json/texts.dat","w+")
    f.write("{}")
    f.close()
if not os.path.exists("bin/json/hotkeys.dat"):
    f = open("bin/json/hotkeys.dat","w+")
    f.write("[]")
    f.close()

if not os.path.exists("bin/json/cache.dat"):
    f = open("bin/json/cache..dat","w+")
    f.write("[]")
    f.close()

def exit():
    respwin.destroy()
    sys.exit()

def copy_text(text):
    clipboard.copy(text)

respwin = tkinter.Tk()

respwin.protocol("WM_DELETE_WINDOW", exit)

def delete_text():
    time.sleep(.5)
    global check_boxes
    temp = []
    for item in check_boxes.values():
        temp.append(item.get())
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = temp.index(1, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError:
            break
    pins = json.load(open("bin/json/texts.dat","r"))
    pins = [value for value in pins.values()]
    seclist = []
    for item in indexPosList:
        seclist.append(pins[item])
    for item in seclist:
        pins.remove(item)
    new_dict = {}
    for item in pins:
       name = item['text']
       new_dict[name] = item
    f = open("bin/json/texts.dat","w")
    f.write(json.dumps(new_dict))
    f.close()
    widget.deleteButtons()
    widget.createButtons()
check_boxes= {}

def create_text():
        di = json.load(open("bin/json/texts.dat", "r"))
        text = entry.get("1.0",tkinter.END)
        text = text[:-1]
        if len(entry.get("1.0", tkinter.END)) <= 1:
            messagebox.showerror("Error", "No text inputted!")
        elif len(entry.get("1.0", tkinter.END)) > 150:
            messagebox.showerror("Error", "Limit of 150 characters broken!")
        elif text in di:
            messagebox.showerror("Error", "You already have a pin for this text!")
        else:
            global check_boxes
            di[text] = {"text": text}
            f = open("bin/json/texts.dat", "w")
            f.write(json.dumps(di))
            f.close()
            widget.createButtons()
            check_boxes[text] = tkinter.IntVar(respwin)
        widget.deleteButtons()
        widget.createButtons()

class ScrollFrame(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)
        self.canvas = tkinter.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tkinter.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas
        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")
        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.onFrameConfigure(None)         
                                            #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.
    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.
class Example(tkinter.Frame):
    def deleteButtons(self):
        self.scrollFrame.destroy()
        self.scrollFrame = ScrollFrame(self)
        self.createButtons()
        tkinter.Button(self.scrollFrame.viewPort, text="DELETE SELECTED", command=delete_text, borderwidth="1", relief="solid").grid(row=0, column=1)
        tkinter.Button(self.scrollFrame.viewPort, text=f'REFRESH PINS', borderwidth="1", command=self.createButtons,relief="solid", wraplength=200).grid(row=0, column=0)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
    def createButtons(self):
        row = 1
        with open("bin/json/texts.dat", "r") as f:
            texts = json.load(f)
        global check_boxes
        check_boxes = {}
        for text in texts:
            check_boxes[text] = tkinter.IntVar(respwin)
            tkinter.Label(self.scrollFrame.viewPort, text=f'{texts[text]["text"]}', fg=f'black', borderwidth="1", relief="solid", wraplength=200).grid(row=row, column=0, sticky=tkinter.W)
            tkinter.Button(self.scrollFrame.viewPort, text="COPY", command= lambda text=text: copy_text(text), borderwidth="1", relief="solid").grid(row=row, column=1, sticky=tkinter.E)
            tkinter.Checkbutton(self.scrollFrame.viewPort, variable = check_boxes[text]).grid(row=row, column=3, sticky=tkinter.E)
            row += 1
    def toggle(self):
        global showing
        if showing:
            respwin.update()
            respwin.withdraw()
            showing = False
        else:
            respwin.update()
            respwin.deiconify()
            showing = True
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
        # Now add some controls to the scrollframe. 
        self.deleteButtons()
        self.createButtons()
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        keyboard.add_hotkey('alt+shift+v', self.toggle)


widget = Example(respwin)
widget.grid(row=0, column=0)
b = tkinter.Button(respwin, text="Create EasyCopy!", command=create_text)
b.grid(row=5, column=0)
entry = tkinter.Text(respwin, height=3, width=50)
entry.grid(row=2, column=0, columnspan=60)
respwin.title("EasyCopy")
tkinter.Label(respwin, text="HOTKEY TO HIDE AND SHOW WINDOW IS ALT+SHIFT+V").grid(row=6)
respwin.wm_iconbitmap(default="prog.ico")
respwin.resizable(False, False)
respwin.mainloop()