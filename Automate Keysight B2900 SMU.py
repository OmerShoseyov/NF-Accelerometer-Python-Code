import pyautogui 
import time
import serial
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox #import messagebox library

Arduino_Port = 'COM4'
arduino_triger = serial.Serial(Arduino_Port, 115200, timeout=0.1) # Arduino Serial port configuration
Counter = 0 
s = 1
t = b = r = l = 0

def Start():
    global x
    triger = 0
    cnt = 0
    index = 1
    Path = change_to_backslash(path)
    junctions = Junctions()
    Counter = len(junctions)
    count.set(str(index) + '/' + str(Counter))
    root.update()

    start = time.time()

    while stop.get() == False:
        root.update()
        status_text.set('  Running  ')
        status_led.configure(bg='green2')
        count.set(str(index) + '/' + str(Counter))
         
        stop.set(False)
        get_g = g_entry.get()
        Chip_name = Chip_entry.get()
        volt = volt_entry.get()
        it_iv = type_off_m.get()
        #T_B_R_L = side.get()
        file_name = Chip_name + '_' + get_g + 'g_' + volt + 'V_' 
        # print(file_name)
        # print(Path)
        # time.sleep(0.5)
        if (float(get_g) > 10.0):
            messagebox.showwarning(title='WARNING!',message='MAX g is 10')
            Stop()
            

        if arduino_triger.inWaiting() > 0:
            #print('in3')
            triger = arduino_triger.readline().decode() 
            triger = int(triger)
            cnt = 1
            
        
        if triger == 1:
            if cnt == 1:
                #print('in1')
                ###Start Measurement###
                #x, y = pyautogui.locateCenterOnScreen('Start Measurement.PNG', confidence=0.75) # x = 225 y = 97
                #print(x, y)
                pyautogui.moveTo(225, 97)
                pyautogui.click()  
                print(time.time() - start)
                ###Move to plot window###
                x, y = pyautogui.locateCenterOnScreen('Graph.PNG', confidence=0.75)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                cnt = 0
                print(index)
                print(time.time() - start)

        if triger == 0:
            if cnt == 1:
                #print('in0')
                if it_iv == 0:
                    ###Stop Measurement###
                    #x, y = pyautogui.locateCenterOnScreen('Stop Measurement.PNG', confidence=0.75) # x = 225 y = 97
                    #print(x, y)
                    pyautogui.moveTo(225, 97)
                    pyautogui.click() 

                print(time.time() - start)

                ###Save Measurement###
                x, y = pyautogui.locateCenterOnScreen('Table.PNG', confidence=0.75)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                pyautogui.move(0, 100) #move 100 pixels down relative to current position
                pyautogui.rightClick()
                pyautogui.move(94, 63)
                pyautogui.click()
                pyautogui.write(Path + '\\' + file_name + junctions[index - 1])
                pyautogui.press('enter')

                index += 1
                
                ###Move to plot window###
                x, y = pyautogui.locateCenterOnScreen('Graph.PNG', confidence=0.75)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                cnt = 0

        if index > Counter:
            stop.set(True)
        
        root.update()
             
    print('stop')
    if stop.get():
        stop.set(False)
        status_text.set('  Waiting  ')
        status_led.configure(bg='red')
        root.update()
 

def tbrl_to_string(tbrl):

    if   tbrl == 0: return 'T'
    elif tbrl == 1: return 'B'
    elif tbrl == 2: return 'R'
    elif tbrl == 3: return 'L'

def Save_Directory():
    global path
    global s
    global last_path

    if s == 1:
        current_path = r'C:\Users\accel\OneDrive\Desktop\Omer'
        s += 1
        last_path = 'aa'
    else:
        current_path = last_path
        
    path = filedialog.askdirectory(initialdir=current_path, title="Select file")
    last_path = path
    save_str.set(path)
    return path 

def Junctions():
    junctions = []

    for i in range(len(names_T)):
        if vars_T[i].get() == 1:
            junctions.append(names_T[i])

    for i in range(len(names_T)):
        if vars_B[i].get() == 1:
            junctions.append(names_B[i])

    for i in range(len(names_T)):
        if vars_R[i].get() == 1:
            junctions.append(names_R[i])
    
    for i in range(len(names_T)):
        if vars_L[i].get() == 1:
            junctions.append(names_L[i])

    return junctions

def Reset():
    global t, b, r, l
    g_entry.delete(0, END)
    Chip_entry.delete(0,END)
    volt_entry.delete(0,END)
    for i in range(len(names_T)):
        vars_T[i].set(0)
        vars_B[i].set(0)
        vars_R[i].set(0)
        vars_L[i].set(0)
        t = b = r = l = 0

    root.update()
   

def Stop():
    stop.set(True)

def change_to_backslash(input):
     return input.replace(r'/', '\\')

def T():
    global t
    if t == 0:
        for i in range(len(names_T)):
            vars_T[i].set(1)
            t = 1
    else:
        for i in range(len(names_T)):
            vars_T[i].set(0)
            t = 0

    root.update()

def B():
    global b
    if b == 0:
        for i in range(len(names_B)):
            vars_B[i].set(1)
            b = 1
    else:
        for i in range(len(names_B)):
            vars_B[i].set(0)
            b = 0

    root.update()

def R():
    global r
    if r == 0:
        for i in range(len(names_R)):
            vars_R[i].set(1)
            r = 1
    else:
        for i in range(len(names_R)):
            vars_R[i].set(0)
            r = 0

    root.update()

def L():
    global l
    if l == 0:
        for i in range(len(names_L)):
            vars_L[i].set(1)
            l = 1
    else:
        for i in range(len(names_L)):
            vars_L[i].set(0)
            l = 0

    root.update()

root = Tk()
root.title('Acceleration Measurement')
#root.configure(background = 'light blue')
#root.geometry('700x700')
root.resizable(False, False)

x = IntVar()
type_off_m = IntVar()
save_str = StringVar()
stop = BooleanVar()
stop.set(False)
start = BooleanVar()
start.set(False)
status_text = StringVar()
status_text.set('  Waiting  ')
count = StringVar()
count.set(str(0) + '/' + str(Counter))
vars_T = []
vars_B = []
vars_R = []
vars_L = []

direction = ['CW', 'CCW']
IT_IV = ['I(t)', 'I(V)']
names_T = ["T_1", "T_2", "T_3", "T_4", "T_5", "T_6"]
names_B = ["B_1", "B_2", "B_3", "B_4", "B_5", "B_6"]
names_R = ["R_1", "R_2", "R_3", "R_4", "R_5", "R_6"]
names_L = ["L_1", "L_2", "L_3", "L_4", "L_5", "L_6"]


""" Rocket_Image = PhotoImage('Rocket.png')
CW_Image = PhotoImage(file='/home/pi/NF-Accelerometer Code/NF-Accelerometer-Python-Code/CW.png')
CCW_Image = PhotoImage(file='/home/pi/NF-Accelerometer Code/NF-Accelerometer-Python-Code/CCW.png')
DirectionImages = [CW_Image,CCW_Image] """

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

f1 = Frame(root, bd=5, relief=RAISED)
f2 = Frame(root, bd=5)
f3 = Frame(root, bd=5)
f4 = Frame(root, bd=5)
f5 = Frame(root, bd=5)
f6 = Frame(root, bd=5)
f7 = Frame(root, bd=5)
f8 = Frame(root, bd=5)
f9 = Frame(root, bd=5)
f10 = Frame(root, bd=5, relief=RAISED)
f11 = Frame(root, bd=5, relief=RAISED)
f12 = Frame(root, bd=5)
f13 = Frame(root, bd=5, relief=RAISED)
f14 = Frame(f13, bd=5)
f15 = Frame(f13, bd=5)
f16 = Frame(f13, bd=5)
f17 = Frame(f13, bd=5)
f18 = Frame(root, bd=5)


f1.grid(row=0, columnspan=3, sticky=N)
f2.grid(row=1, column=0, sticky=NW)
f3.grid(row=2, column=0, sticky=NW)
f4.grid(row=3, column=0, sticky=NW)
f5.grid(row=4, column=0, sticky=NW)
f6.grid(row=5, column=0, sticky=NW)
f7.grid(row=4, column=0, sticky=NW)
f8.grid(row=6, column=0, columnspan=2, sticky=EW)
f9.grid(row=7, column=1, columnspan=2, sticky=EW)
f10.grid(row=1, column=2, columnspan=1)
f11.grid(row=2, column=2, columnspan=1)
f12.grid(row=3, column=0, sticky=EW)
f13.grid(row=1, rowspan=4, column=1, sticky=N)
f14.grid(row=0, columnspan=2, sticky=N)
f15.grid(row=1, column=1, sticky=NE)
f16.grid(row=1, column=0, sticky=NW)
f17.grid(row=2, columnspan=2, rowspan=2, sticky=S)
f18.grid(row=2, column=0, sticky=NW)

#### frame 1
headr = Label(f1, text='Acceleration Measurement', font=("Ariel 30 bold underline")).pack()

#### frame 2
g_label = Label(f2, text='Desired g:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
g_entry = Entry(f2, width=4, font=("Ariel 18"), justify="right")
g_entry.pack(side=LEFT, padx=2, pady=5)
g_units_label = Label(f2, text='g [m/s\u00B2]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

""" #### frame 3
M_time_label = Label(f3, text='Measurement Duration:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
M_time_entry = Entry(f3, width=4, font=("Ariel 18"), justify="right")
M_time_entry.pack(side=LEFT, padx=2, pady=5)
M_time_units_label = Label(f3, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 4
Dwell_time_label = Label(f4, text='Dwell Time:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
Dwell_time_entry = Entry(f4, width=4, font=("Ariel 18"), justify="right")
Dwell_time_entry.pack(side=LEFT, padx=2, pady=5)
Dwell_time_units_label = Label(f4, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 5
Rise_time_label = Label(f5, text='Rise Time:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
Rise_time_entry = Entry(f5, width=4, font=("Ariel 18"), justify="right")
Rise_time_entry.pack(side=LEFT, padx=2, pady=5)
Rise_time_units_label = Label(f5, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 6
Fall_time_label = Label(f6, text='Fall Time:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
Fall_time_entry = Entry(f6, width=4, font=("Ariel 18"), justify="right")
Fall_time_entry.pack(side=LEFT, padx=2, pady=5)
Fall_time_units_label = Label(f6, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5) """

# #### frame 4
# Rotation_direction_label = Label(f4, text='Rotation Direction:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)

# for index in range(len(direction)):
#     radiobutton = Radiobutton(f4,
#                               text=direction[index], #adds text to radio buttons
#                               variable=x, #groups radiobuttons together if they share the same variable
#                               value=index, #assigns each radiobutton a different value
#                               padx = 2, #adds padding on x-axis
#                               font=("Ariel 18 bold"),
#                               image = DirectionImages[index], #adds image to radiobutton
#                               compound = 'left', #adds image & text (left-side)
#                               indicatoron=0, #eliminate circle indicators
#                               width = 200, #sets width of radio buttons
#                               #command=order #set command of radiobutton to function
#                               )
#     radiobutton.pack(anchor=CENTER, padx=2, pady=5)

Chip_label = Label(f12, text='Chip Serial Number:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
Chip_entry = Entry(f12, width=10, font=("Ariel 18"), justify="left")
Chip_entry.pack(side=LEFT, padx=2, pady=5)

#### frame 7
Which_is_connected_label = Label(f7, text='Type of measurement:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)

for index in range(len(IT_IV)):
    radiobutton = Radiobutton(f7,
                              text=IT_IV[index], #adds text to radio buttons
                              variable=type_off_m, #groups radiobuttons together if they share the same variable
                              value=index, #assigns each radiobutton a different value
                              padx = 2, #adds padding on x-axis
                              font=("Ariel 18 bold"),
                              #image = foodImages[index], #adds image to radiobutton
                              #compound = 'left', #adds image & text (left-side)
                              indicatoron=0, #eliminate circle indicators
                              width = 10, #sets width of radio buttons
                              #command=order #set command of radiobutton to function
                              )
    radiobutton.pack(side=LEFT, padx=2, pady=2, expand=TRUE)



#### frame 8
save_button = Button(f8, text="Where to save?", font=("Ariel 18 bold"), width=12, command=Save_Directory).pack(side=LEFT)
save_label = Label(f8, text="",
              font=('Arial 18'),
              #fg='#00FF00',
              bg='white',
              relief=SUNKEN,
              bd=5,
              padx=2,
              pady=2,
              width=50,
              anchor="e",
              #image=photo,
              #compound='bottom',
              textvariabl=save_str,
              ).pack(side=LEFT)


#### frame 9
start_button = Button(f9, text="Start", font=("Ariel 18 bold"), width=12, height=2, command=Start, activebackground='green').grid(row=0, column=0, padx=2, sticky=W)#pack(side=LEFT)
reset_button = Button(f9, text="Reset", font=("Ariel 18 bold"), width=12, height=2, command=Reset, activebackground='yellow').grid(row=0, column=1, padx=2, sticky=EW)#pack(side=TOP)
stop_button = Button(f9, text="Stop", font=("Ariel 18 bold"), width=12, height=2, command=Stop, activebackground='red').grid(row=0, column=2, padx=2,sticky=E)#pack(side=RIGHT)

#### frame 10
status_led = Label(f10, textvariable=status_text, font=("Ariel 40 bold"), bg='red')
status_led.pack(anchor=E)

#### frame 11
Count = Label(f11, textvariable=count, font=("Ariel 40 bold"))
Count.pack(fill="none", expand=True)

#### frame 13
for i, checkboxname in enumerate(names_T):
    vars_T.append(IntVar())
    check = Checkbutton(f14, text=checkboxname, variable=vars_T[i], font=('Ariel 14'))
    check.grid(row=0, column=i)#pack(side=LEFT, padx=2, pady=2, expand=TRUE, anchor="n")

for i, checkboxname in enumerate(names_B):
    vars_B.append(IntVar())
    check = Checkbutton(f17, text=checkboxname, variable=vars_B[i], font=('Ariel 14'))
    check.grid(row=1, column=i)#pack(side=LEFT, padx=2, pady=2, expand=TRUE, anchor="s")

for i, checkboxname in enumerate(names_R):
    vars_R.append(IntVar())
    check = Checkbutton(f15, text=checkboxname, variable=vars_R[i], font=('Ariel 14'))
    check.grid(row=i, column=1)#pack(side=TOP, padx=2, pady=2, expand=TRUE, anchor="w")

for i, checkboxname in enumerate(names_L):
    vars_L.append(IntVar())
    check = Checkbutton(f16, text=checkboxname, variable=vars_L[i], font=('Ariel 14'))
    check.grid(row=i, column=0)#pack(side=TOP, padx=2, pady=2, expand=TRUE, anchor="e")

T_button = Button(f14, text="T", font=("Ariel 12 bold"), width=6, height=1, command=T, activebackground='green').grid(row=1, column=0, columnspan=6)
B_button = Button(f17, text="B", font=("Ariel 12 bold"), width=6, height=1, command=B, activebackground='green').grid(row=0, column=0, columnspan=6)
R_button = Button(f15, text="R", font=("Ariel 12 bold"), width=3, height=3, command=R, activebackground='green').grid(row=0, rowspan=6, column=0)
L_button = Button(f16, text="L", font=("Ariel 12 bold"), width=3, height=3, command=L, activebackground='green').grid(row=0, rowspan=6, column=1)

#### frame 18
volt_label = Label(f18, text='Volt:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
volt_entry = Entry(f18, width=4, font=("Ariel 18"), justify="right")
volt_entry.pack(side=LEFT, padx=2, pady=5)
volt_label = Label(f18, text='[V]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

def on_closing():
     root.destroy()

while start.get() == False:
    index = 0
    junctions = Junctions()
    Counter = len(junctions)
    count.set(str(index) + '/' + str(Counter))
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.update() 


root.mainloop()
