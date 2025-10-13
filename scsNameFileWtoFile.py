# scs_06_07_2020_02_22_16_808331_PM

from tkinter import *
import datetime, time
global input01, input02, valueB001, inputA003, varS

app = Tk()
app.title('Name Any File')
app.geometry('770x500')

labelA001 = Label(app, text='General File Name', relief=SUNKEN)
labelA001.pack(side=TOP, anchor=N, fill=X, expand=NO)

input01 = StringVar()
inputA001 = Entry(app, textvariable=input01)
inputA001.pack(side=TOP, anchor=N, fill=X, expand=NO)
    
def function001():
    
    dt = datetime.datetime.now()
    hour = str(dt.strftime('%I'))
    min = str(dt.strftime('%M'))
    sec = str(dt.strftime('%S'))
    msec = str(dt.strftime('%f'))
    amPms = str(dt.strftime('%p'))
    mnth = str(dt.strftime('%m'))
    day = str(dt.strftime('%d'))
    year = str(dt.strftime('%Y'))
    
    timeTogether = str(mnth + '_' + day + '_' + year + '_' + hour + '_' + min + '_' + sec + '_' + msec + '_' + amPms)
    
    varA = input01.get()
    varI = input02.get()
    varG = 0
    varH = varA + '_' + timeTogether
    inputA003.insert(END, varH)

    word = "szNaming_Files_File_"
    dthm = datetime.datetime.now()
    m = str(dthm.strftime("%m"))
    dy = str(dthm.strftime("%d"))
    y = str(dthm.strftime("%Y"))
    h = str(dthm.strftime("%I"))
    mins = str(dthm.strftime("%M"))
    amPm = str(dthm.strftime("%p"))
    sec = str(dthm.strftime("%S"))
    dash = "-"
    d = str(m + dash + dy + dash + y + dash + h + dash + mins + dash + sec + dash + amPm)
    z = word + d + ".txt"
    newLine = "\n"
    file = open(z, "w")
    file.write(varA)
    file.write("_")
    file.write(timeTogether)
    file.close()
    
    return

def function002():
    var = 0
    varI = input02.get()
    for var in range(0, varI):
        var += 1
        function001()
    return

input02 = IntVar()
inputB001 = Entry(app, width=8, textvariable=input02)
inputB001.pack(side=TOP, anchor=N, expand=NO)

labelB001 = Label(app, text='How many file names.')
labelB001.pack(side=TOP, anchor=N, fill=X, expand=NO)
valueB001 = StringVar()

for valueA001, status in [('Check and uncheck, for your filenames.', NORMAL)]:
    setattr(valueB001, valueA001, IntVar())
    Checkbutton(app, text=valueA001, state=status, variable=getattr(valueB001, valueA001), command=function002).pack(side=TOP, anchor=N, fill=X, expand=NO)

labelA001 = Label(app, text='CTRL-C to copy, CTRL-V to paste filename', relief=SUNKEN)
labelA001.pack(side=TOP, anchor=N, fill=X, expand=NO)

inputA003 = Listbox(app)
scrollbarA003 = Scrollbar(inputA003, command=inputA003.yview)
inputA003.configure(yscrollcommand=scrollbarA003.set)
    
inputA003.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)
scrollbarA003.pack(side=RIGHT, anchor=S, fill=Y)

app.mainloop()
