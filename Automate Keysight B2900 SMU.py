import pyautogui 
import time
import serial
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox #import messagebox library

Arduino_Port = 'COM5'
arduino_triger = serial.Serial(Arduino_Port, 115200, timeout=0.1) # Arduino Serial port configuration

def Start():
    root.update()
    global x
    triger = 0
    cnt = 0
    index = 1
    Path = change_to_backslash(path)
    while stop.get() == False:
        root.update()
        status_text.set('  Running  ')
        status_led.configure(bg='green2')
         
        stop.set(False)
        get_g = g_entry.get()
        Chip_name = Chip_entry.get()
        volt = volt_entry.get()
        T_B_R_L = side.get()
        file_name = Chip_name + '_' + get_g + 'g_' + volt + 'V_' + tbrl_to_string(T_B_R_L) 
        # print(file_name)
        # print(Path)
        # time.sleep(0.5)
        if (float(get_g) > 10.0):
            messagebox.showwarning(title='WARNING!',message='MAX g is 10')
            return

        if arduino_triger.inWaiting() > 0:
            #print('in3')
            triger = arduino_triger.readline().decode() 
            triger = int(triger)
            cnt = 1
        
        if triger == 1:
            if cnt == 1:
                #print('in1')
                ###Start Measurement###
                x, y = pyautogui.locateCenterOnScreen('Start Measurement.PNG', confidence=0.75)
                #print(x, y)
                pyautogui.moveTo(x, y)
                pyautogui.click()  

                ###Move to plot window###
                x, y = pyautogui.locateCenterOnScreen('Graph.PNG', confidence=0.75)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                cnt = 0
                print(index)

        if triger == 0:
            if cnt == 1:
                #print('in0')
                ###Stop Measurement###
                x, y = pyautogui.locateCenterOnScreen('Stop Measurement.PNG', confidence=0.75)
                #print(x, y)
                pyautogui.moveTo(x, y)
                pyautogui.click() 

                ###Save Measurement###
                x, y = pyautogui.locateCenterOnScreen('Table.PNG', confidence=0.75)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                pyautogui.move(0, 100) #move 100 pixels down relative to current position
                pyautogui.rightClick()
                pyautogui.move(94, 63)
                pyautogui.click()
                pyautogui.write(Path + '\\' + file_name + '_' + str(index))
                pyautogui.press('enter')

                index += 1
                
                ###Move to plot window###
                x, y = pyautogui.locateCenterOnScreen('Graph.PNG', confidence=0.75)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                cnt = 0

        if index > 6:
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
    path = filedialog.askdirectory(initialdir=r'C:\Users\accel\OneDrive\Desktop\Omer\Measurements', title="Select file")
    save_str.set(path)
    return path 

def Reset():
    g_entry.delete(0, END)
    Chip_entry.delete(0,END)
    volt_entry.delete(0,END)
    

def Stop():
    stop.set(True)

def change_to_backslash(input):
     return input.replace(r'/', '\\')


root = Tk()
root.title('Acceleration Measurement')
#root.configure(background = 'light blue')
#root.geometry('700x700')
root.resizable(False, False)


side = IntVar()
save_str = StringVar()
status_text = StringVar()
status_text.set('  Waiting  ')
stop = BooleanVar()
stop.set(False)

direction = ['CW', 'CCW']
TBRL = ['T', 'B', 'R', 'L']

# Rocket_Image = PhotoImage('Rocket.png')
# CW_Image = PhotoImage(file='CW.png')
# CCW_Image = PhotoImage(file='CCW.png')
# DirectionImages = [CW_Image,CCW_Image]

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

f1 = Frame(root, bd=5, relief=RAISED)
f2 = Frame(root, bd=5)
f3 = Frame(root, bd=5)
f4 = Frame(root, bd=5)
f5 = Frame(root, bd=5)
f6 = Frame(root, bd=5)
f7 = Frame(root, bd=5)
f8 = Frame(root, bd=5, relief=RAISED)

f1.grid(row=0, columnspan=2, sticky=N)
f2.grid(row=1, column=0, sticky=NW)
f3.grid(row=2, column=0, sticky=NW)
f4.grid(row=1, column=1, rowspan=2, sticky=NW)
f5.grid(row=3, column=0, columnspan=2, sticky=EW)
f6.grid(row=4, column=0, columnspan=2, sticky=EW)
f7.grid(row=5, column=0, columnspan=2, sticky=EW)
f8.grid(row=2, column=1)

#### frame 1
headr = Label(f1, text='Acceleration Measurement', font=("Ariel 30 bold underline")).pack()

#### frame 2
g_label = Label(f2, text='g:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
g_entry = Entry(f2, width=4, font=("Ariel 18"), justify="right")
g_entry.pack(side=LEFT, padx=2, pady=5)
g_units_label = Label(f2, text='g [m/s^2]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 3
Chip_label = Label(f3, text='Chip Serial Number:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
Chip_entry = Entry(f3, width=10, font=("Ariel 18"), justify="left")
Chip_entry.pack(side=LEFT, padx=2, pady=5)
#M_time_units_label = Label(f3, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 4
volt_label = Label(f4, text='volt:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
volt_entry = Entry(f4, width=4, font=("Ariel 18"), justify="right")
volt_entry.pack(side=LEFT, padx=2, pady=5)
volt_label = Label(f4, text='[V]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

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



#### frame 5
Which_is_connected_label = Label(f5, text='Which side is connected:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)

for index in range(len(TBRL)):
    radiobutton = Radiobutton(f5,
                              text=TBRL[index], #adds text to radio buttons
                              variable=side, #groups radiobuttons together if they share the same variable
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



#### frame 6
save_button = Button(f6, text="Where to save?", font=("Ariel 18 bold"), width=12, command=Save_Directory).pack(side=LEFT)
save_label = Label(f6, text="",
              font=('Arial 18'),
              #fg='#00FF00',
              bg='white',
              relief=SUNKEN,
              bd=5,
              padx=2,
              pady=2,
              width=35,
              #image=photo,
              #compound='bottom',
              textvariabl=save_str,
              ).pack(side=LEFT)


#### frame 7
start_button = Button(f7, text="Start", font=("Ariel 18 bold"), width=12, height=2, command=Start, activebackground='green').grid(row=0, column=0, padx=2, sticky=W)#pack(side=LEFT)
reset_button = Button(f7, text="Reset", font=("Ariel 18 bold"), width=12, height=2, command=Reset, activebackground='yellow').grid(row=0, column=1, padx=2, sticky=EW)#pack(side=TOP)
stop_button = Button(f7, text="Stop", font=("Ariel 18 bold"), width=12, height=2, command=Stop, activebackground='red').grid(row=0, column=2, padx=2,sticky=E)#pack(side=RIGHT)

#### frame 8
status_led = Label(f8, textvariable=status_text, font=("Ariel 40 bold"), bg='red')
status_led.pack(anchor=E)

root.mainloop()
