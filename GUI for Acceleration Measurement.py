from tkinter import *
from tkinter import filedialog
from tkinter import messagebox #import messagebox library
from bluepy import btle
import time



def Start():
    get_g = g_entry.get()

    if (float(get_g) > 10.0):
        messagebox.showwarning(title='WARNING!',message='MAX g is 10')
        return

    r_dir = x.get()
    m_time = M_time_entry.get()
    s_f = '1'

    T_B_R_L = y.get()
    
    
    if r_dir == 0:
        r_dir = str(-1)
    else:
        r_dir = str(1)

    
    
    BLE(get_g, r_dir, m_time, s_f)
    time.sleep(2)

    print('Starting')
    Current_time = time.time()
    Start_time = time.time()
    Print_time = Start_time

    while Current_time - Start_time <= float(m_time) and stop.get() == False:
        root.update()

        Current_time = time.time()

        if Current_time - Print_time > 1:
            print(Current_time - Start_time)
            Print_time = time.time()
       # print(path)
       # print(get_g)
        #print(type(get_g))
       # print(m_time)
       # Save(path, T_B_R_L)

        
        
    if stop.get():
        print(Current_time - Start_time) 
        print('Stoped')
        stop.set(False)
        get_g = r_dir = m_time = s_f = '0'
        BLE_Stop(s_f)
    else:
        print(Current_time - Start_time)
        print('Done')

def Reset():
    g_entry.delete(0, END)
    M_time_entry.delete(0,END)
    

def Stop():
    stop.set(True)
    

def BLE(get_g, r_dir, m_time, s_f):

    try:
        #Have to match with Peripheral
        MAC = "a8:61:0a:24:66:2e"
        BLE_UUID_MOTOR_INSTRUCTIONS_SERVICE =       "9e661242-e694-4262-b393-61744b474383"
        #BLE_UUID_GET_G =                            "73cce820-35ee-47f2-bca7-31105f673e20"
        #BLE_UUID_ROTATION_DIRECTION =               "aae6924e-fdd1-40d7-9e71-b026bcec5cc9"
        #BLE_UUID_MEASUREMENT_TIME =                 "80077d16-c5c6-48c4-8c10-7da0b6fe3e6f"
        #BLE_UUID_START_FINISH =                     "40e0f2d5-2327-4930-83ca-c2ca729ca1bb"
        #BLE_UUID_STATUS =                           "5720e451-6f72-49f1-8721-079d7e4bb497"

        get_g_byte = get_g.encode()
        r_dir_byte = r_dir.encode()
        m_time_byte = m_time.encode()
        s_f_byte = s_f.encode()

        Odrive_Arduino = btle.Peripheral(MAC)
        Motor_Instructions_Service = Odrive_Arduino.getServiceByUUID(BLE_UUID_MOTOR_INSTRUCTIONS_SERVICE)
        Motor_Instructions_Characteristics = Motor_Instructions_Service.getCharacteristics()
        #print(Motor_Instructions_Characteristics)
        #print(type(Motor_Instructions_Characteristics))

        Get_g_Characteristic = Motor_Instructions_Characteristics[0]
        #print(Get_g_Characteristic)
        Rotation_Direction_Characteristic = Motor_Instructions_Characteristics[1]
        #print(Rotation_Direction_Characteristic)
        Measurment_Time_Characteristic = Motor_Instructions_Characteristics[2]
        #print(Measurment_Time_Characteristic)
        Start_Finish_Characteristic = Motor_Instructions_Characteristics[3]
        #print(Start_Finish_Characteristic)
        Status_Characteristic = Motor_Instructions_Characteristics[4]

        Status = Status_Characteristic.read().decode()
        print(Status)

        if Status == 'Ready':
            #print(get_g_byte)
            Get_g_Characteristic.write(get_g_byte, True)
            #print(get_g_byte)
            print(f'Get_g =  {Get_g_Characteristic.read()}')
            #print(get_g_byte)
            #time.sleep(0.2)
            Rotation_Direction_Characteristic.write(r_dir_byte, True)
            #print(r_dir_byte)
            print(f'Rotation_Direction = {Rotation_Direction_Characteristic.read()}')
            #time.sleep(0.2)
            Measurment_Time_Characteristic.write(m_time_byte, True)
            print(f'Measurment_Time = {Measurment_Time_Characteristic.read()}')
            #time.sleep(0.2)
            #print(s_f)
            Start_Finish_Characteristic.write(s_f_byte, True)
            #print(s_f)
            print(f'Start_Finish = {Start_Finish_Characteristic.read()}')
            
            Odrive_Arduino.disconnect()
            print('-----Bye-----')

    except KeyboardInterrupt:
        s_f = '0'.encode()
        Start_Finish_Characteristic.write(s_f, True)
        Odrive_Arduino.disconnect()

def BLE_Stop(s_f):

    try:
        #Have to match with Peripheral
        MAC = "a8:61:0a:24:66:2e"
        BLE_UUID_MOTOR_INSTRUCTIONS_SERVICE =       "9e661242-e694-4262-b393-61744b474383"
        #BLE_UUID_GET_G =                            "73cce820-35ee-47f2-bca7-31105f673e20"
        #BLE_UUID_ROTATION_DIRECTION =               "aae6924e-fdd1-40d7-9e71-b026bcec5cc9"
        #BLE_UUID_MEASUREMENT_TIME =                 "80077d16-c5c6-48c4-8c10-7da0b6fe3e6f"
        #BLE_UUID_START_FINISH =                     "40e0f2d5-2327-4930-83ca-c2ca729ca1bb"
        #BLE_UUID_STATUS =                           "5720e451-6f72-49f1-8721-079d7e4bb497"


        s_f_byte = s_f.encode()

        Odrive_Arduino = btle.Peripheral(MAC)
        Motor_Instructions_Service = Odrive_Arduino.getServiceByUUID(BLE_UUID_MOTOR_INSTRUCTIONS_SERVICE)
        Motor_Instructions_Characteristics = Motor_Instructions_Service.getCharacteristics()
        #print(Motor_Instructions_Characteristics)
        #print(type(Motor_Instructions_Characteristics))

        #Get_g_Characteristic = Motor_Instructions_Characteristics[0]
        #print(Get_g_Characteristic)
        #Rotation_Direction_Characteristic = Motor_Instructions_Characteristics[1]
        #print(Rotation_Direction_Characteristic)
        #Measurment_Time_Characteristic = Motor_Instructions_Characteristics[2]
        #print(Measurment_Time_Characteristic)
        Start_Finish_Characteristic = Motor_Instructions_Characteristics[3]
        #print(Start_Finish_Characteristic)
        #Status_Characteristic = Motor_Instructions_Characteristics[4]

        #Status = Status_Characteristic.read().decode()
        #print(Status)

        
            #print(get_g_byte)
            #Get_g_Characteristic.write(get_g_byte, True)
            #print(get_g_byte)
            #print(f'Get_g =  {Get_g_Characteristic.read()}')
            #print(get_g_byte)
            #time.sleep(0.2)
            #Rotation_Direction_Characteristic.write(r_dir_byte, True)
            #print(r_dir_byte)
            #print(f'Rotation_Direction = {Rotation_Direction_Characteristic.read()}')
            #time.sleep(0.2)
            #Measurment_Time_Characteristic.write(m_time_byte, True)
            #print(f'Measurment_Time = {Measurment_Time_Characteristic.read()}')
            #time.sleep(0.2)
            #print(s_f)
        Start_Finish_Characteristic.write(s_f_byte, True)
            #print(s_f)
        print(f'Start_Finish = {Start_Finish_Characteristic.read()}')
            
        Odrive_Arduino.disconnect()
        print('-----Bye-----')

    except KeyboardInterrupt:
        s_f = '0'.encode()
        Start_Finish_Characteristic.write(s_f, True)
        Odrive_Arduino.disconnect()

def Save_Directory():
    global path
    path = filedialog.askdirectory(initialdir="/home/pi/Acceleration Measurements", title="Select file")
    save_str.set(path)
    #print(path) 
  

def Save(path, tbrl):

    if tbrl == 0:
        tbrl = 'T'
    elif tbrl == 1:
        tbrl = 'B'
    elif tbrl == 2:
        tbrl = 'R'
    elif tbrl == 3:
        tbrl = 'L'

    print(tbrl)
    

root = Tk()
root.title('Acceleration Measurement')
#root.configure(background = 'light blue')
#root.geometry('700x700')
root.resizable(False, False)

x = IntVar()
y = IntVar()
save_str = StringVar()
stop = BooleanVar()
stop.set(False)

direction = ['CW', 'CCW']
TBRL = ['T', 'B', 'R', 'L']

Rocket_Image = PhotoImage('Rocket.png')
CW_Image = PhotoImage(file='CW.png')
CCW_Image = PhotoImage(file='CCW.png')
DirectionImages = [CW_Image,CCW_Image]

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

f1 = Frame(root, bd=5, relief=RAISED)
f2 = Frame(root, bd=5)
f3 = Frame(root, bd=5)
f4 = Frame(root, bd=5)
f5 = Frame(root, bd=5)
f6 = Frame(root, bd=5)
f7 = Frame(root, bd=5)

f1.grid(row=0, columnspan=2, sticky=N)
f2.grid(row=1, column=0, sticky=NW)
f3.grid(row=2, column=0, sticky=NW)
f4.grid(row=1, column=1, rowspan=2, sticky=NW)
f5.grid(row=3, column=0, columnspan=2, sticky=EW)
f6.grid(row=4, column=0, columnspan=2, sticky=EW)
f7.grid(row=5, column=0, columnspan=2, sticky=EW)

#### frame 1
headr = Label(f1, text='Acceleration Measurement', font=("Ariel 30 bold underline")).pack()

#### frame 2
g_label = Label(f2, text='Desired g:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
g_entry = Entry(f2, width=4, font=("Ariel 18"), justify="right")
g_entry.pack(side=LEFT, padx=2, pady=5)
g_units_label = Label(f2, text='g [m/s^2]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 3
M_time_label = Label(f3, text='Measurement Duration:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
M_time_entry = Entry(f3, width=4, font=("Ariel 18"), justify="right")
M_time_entry.pack(side=LEFT, padx=2, pady=5)
M_time_units_label = Label(f3, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 4
Rotation_direction_label = Label(f4, text='Rotation Direction:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)

for index in range(len(direction)):
    radiobutton = Radiobutton(f4,
                              text=direction[index], #adds text to radio buttons
                              variable=x, #groups radiobuttons together if they share the same variable
                              value=index, #assigns each radiobutton a different value
                              padx = 2, #adds padding on x-axis
                              font=("Ariel 18 bold"),
                              image = DirectionImages[index], #adds image to radiobutton
                              compound = 'left', #adds image & text (left-side)
                              indicatoron=0, #eliminate circle indicators
                              width = 200, #sets width of radio buttons
                              #command=order #set command of radiobutton to function
                              )
    radiobutton.pack(anchor=CENTER, padx=2, pady=5)



#### frame 5
Which_is_connected_label = Label(f5, text='Which side is connected:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)

for index in range(len(TBRL)):
    radiobutton = Radiobutton(f5,
                              text=TBRL[index], #adds text to radio buttons
                              variable=y, #groups radiobuttons together if they share the same variable
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



root.mainloop()