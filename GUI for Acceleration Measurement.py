from tkinter import *
from tkinter import filedialog
from tkinter import messagebox #import messagebox library
from bluepy import btle
import time
import serial
import csv

global first_measurement
first_measurement = 1
Counter = 3
i = 1
mems_arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
measurement_arduino = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.5)

def Start():
    cnt = 0 
    status_text.set('  Running  ')
    status_led.configure(bg='green2')
    count.set(str(cnt) + '/' + str(Counter))
    root.update()
    send_pin_num_to_light('0')
    get_g, r_dir, time_from_user, dwell_t, rise_t, fall_t, T_B_R_L, Chip_name = get_data_from_user()
    #path = Save_Directory()
    s_f = '1'
    stop.set(False)

    while cnt < Counter and stop.get() == False:     
        count.set(str(cnt + 1) + '/' + str(Counter))
        root.update()
        if cnt == 0:
            r_dir = '1'
        if cnt == 1:
            r_dir = '-1'
        if cnt == 2:
            r_dir = '1'
        if cnt == 3:
            r_dir = '-1'
        if cnt == 4:
            r_dir = '1'
        if cnt == 5:
            r_dir = '-1'
            
        BLE(get_g, r_dir, time_from_user, dwell_t, rise_t, fall_t, s_f)
        time.sleep(2)
        csv_file = create_files(path, cnt, r_dir, get_g, T_B_R_L, Chip_name)
        print('Starting')

        send_g_range(get_g)
        Print_time = Current_time = Start_time = time.time()    
        while Current_time - Start_time <= (float(time_from_user) + 2.0*float(dwell_t) + float(fall_t)) and stop.get() == False:
            root.update()
            Current_time = time.time()
            # if Current_time - Print_time > 1: # This 1 should be a parameter? 
            #     print(Current_time - Start_time)
            #     Print_time = time.time()
            switch_mux_selector(Current_time-Start_time, cnt, csv_file)
        cnt += 1 
        stop_IMU()
        time.sleep(0.5)             
        root.update()
         
        if stop.get():
            print(Current_time - Start_time) 
            #print('Stopped')
            stop.set(False)
            get_g = r_dir = time_from_user = s_f = '0'
            stop_IMU()
            send_pin_num_to_light('0')
            BLE_Stop(s_f)
        else:
            print(Current_time - Start_time)
            print(cnt)
            send_pin_num_to_light('0')


    if cnt == Counter:
        print('Done')
        send_pin_num_to_light('0')
        stop.set(False)
        status_text.set('  Waiting  ')
        status_led.configure(bg='red')
        count.set(str(0) + '/' + str(Counter))
        root.update()
    else:
        print('Stopped')
        status_text.set('  Waiting  ')
        status_led.configure(bg='red')
        root.update()

def get_data_from_user():
    stop.set(False)
    get_g = g_entry.get()
    Chip_name = Chip_entry.get()
    if (float(get_g) > 10.0):
        messagebox.showwarning(title='WARNING!',message='MAX g is 10')
        return
    r_dir = x.get()
    time_from_user = M_time_entry.get()
    dwell_t = Dwell_time_entry.get()
    rise_t = Rise_time_entry.get()
    fall_t = Fall_time_entry.get()
    s_f = '1'
    T_B_R_L = y.get()
    if r_dir == 0:
        r_dir = str(-1)
    else:
        r_dir = str(1)
    return get_g, r_dir, time_from_user, dwell_t, rise_t, fall_t, T_B_R_L, Chip_name

def create_files(path, cnt, r_dir, get_g, T_B_R_L, Chip_name):
    dir = 'CCW' if r_dir =='1' else "CW"
    filename = Chip_name + '_' + tbrl_to_string(T_B_R_L) + '_' + str(cnt + 1) + '_' + get_g + 'g_' + 'dir'+ dir  
    #txt_file = open(path+'/'+filename+ '.txt', 'w')
    csv_file = open(path+'/'+filename+ '.csv', 'w')
    return csv_file #,txt_file


def switch_mux_selector(current_time, i, csv_file):
    measurement_arduino.reset_input_buffer()
    num_to_send = str(i+1)
    send_pin_num_to_light(num_to_send)


    # line = get_data()
    # print('i = '+ str(i) +', current is ' + line)
    # print(15*'*')
    [xmems, ymems, zmems] = get_IMU_data().split()
    #save_data(txt_file, current_time, xmems, ymems, zmems)
    save_csv_data(csv_file,current_time, xmems, ymems, zmems)


def Reset():
    g_entry.delete(0, END)
    M_time_entry.delete(0,END)
    Dwell_time_entry.delete(0,END)
    Rise_time_entry.delete(0,END)
    Fall_time_entry.delete(0,END)
    Chip_entry.delete(0,END)
    

def Stop():
    stop.set(True)
    

def BLE(get_g, r_dir, m_time, dwt, rt, ft, s_f):

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
        dwt_byte = dwt.encode()
        rt_byte = rt.encode()
        ft_byte = ft.encode()
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
        Dwell_Time_Characteristic = Motor_Instructions_Characteristics[3]
        Rise_Time_Characteristic = Motor_Instructions_Characteristics[4]
        Fall_Time_Characteristic = Motor_Instructions_Characteristics[5]
        Start_Finish_Characteristic = Motor_Instructions_Characteristics[6]
        #print(Start_Finish_Characteristic)
        Status_Characteristic = Motor_Instructions_Characteristics[7]

        Status = Status_Characteristic.read().decode()
        print(Status)
        time.sleep(0.05)

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
            Dwell_Time_Characteristic.write(dwt_byte, True)
            print(f'Dwell_Time = {Dwell_Time_Characteristic.read()}')
            Rise_Time_Characteristic.write(rt_byte, True)
            print(f'Rise_Time = {Rise_Time_Characteristic.read()}')
            Fall_Time_Characteristic.write(ft_byte, True)
            print(f'Fall_Time = {Fall_Time_Characteristic.read()}')
            Start_Finish_Characteristic.write(s_f_byte, True)
            #print(s_f)
            time.sleep(0.05)
            print(f'Start_Finish = {Start_Finish_Characteristic.read()}')
            
            Odrive_Arduino.disconnect()
            time.sleep(0.05)
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
        Start_Finish_Characteristic = Motor_Instructions_Characteristics[6]
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

def send_g_range(get_g):
    g_float = float(get_g)
    if g_float > 0.0 and g_float <= 2.0:
        g = '2'
        mems_arduino.write(str.encode(g + '\n'))
    elif g_float > 2.0 and g_float <= 4.0:
        g = '4'
        mems_arduino.write(str.encode(g + '\n'))
    elif g_float > 4.0 and g_float <= 8.0:
        g = '8'
        mems_arduino.write(str.encode(g + '\n'))
    else:
        g = '16'
        mems_arduino.write(str.encode(g + '\n'))
    

def get_IMU_data():
    read = mems_arduino.readline().decode()
    
    return read

def stop_IMU():
    mems_arduino.write(str.encode('0' + '\n'))

def Save_Directory():
    global path
    global i
    global last_path

    if i == 1:
        current_path = "/home/pi/Acceleration Measurements"
        i += 1
        last_path = 'aa'
    else:
        current_path = last_path

    path = filedialog.askdirectory(initialdir=current_path, title="Select file")
    last_path = path
    save_str.set(path)
    return path 
  

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

def tbrl_to_string(tbrl):

    if   tbrl == 0: return 'T'
    elif tbrl == 1: return 'B'
    elif tbrl == 2: return 'R'
    elif tbrl == 3: return 'L'
    

def save_data(txt_file, time,  x_mems="1", y_mems="1", z_mems="1"):
    # Saves the data from the accelerometer and the MEMS to 'filename'
    # data_to_save = 'time: ' + str(time) + ', current: ' + str(current) + ', x_mems: ' + str(x_mems) + ', y_mems: ' + str(y_mems) + ', z_mems: ' + str(z_mems)
    # data_to_save = str(time) + ', The current is: ' + str(current) 
    # current = str(current)
    first_data = ", time: " + str(time)  
    second_data = 'x_mems: ' + str(x_mems) + ', y_mems: ' + str(y_mems) + ', z_mems: ' + str(z_mems)
    data_to_write = second_data +first_data  + '\n'
    txt_file.write(data_to_write)

def save_csv_data(file_name, time, x_mems="1", y_mems="1", z_mems="1"):
    writer = csv.writer(file_name)
    # print(current)
    # a = current.strip()
    # int_curr = int(current)
    # fin_curr = str(current).strip('\n \r \\" ')
    writer.writerow([x_mems, y_mems, z_mems, time])


def send_pin_num_to_light(number_str):
    #sends to the arduino what 'leg' to put voltage
    measurement_arduino.write(str.encode(number_str + '\n'))


def get_data():
    line = measurement_arduino.readline().decode()
    return line




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
status_text = StringVar()
status_text.set('  Waiting  ')
count = StringVar()
count.set(str(0) + '/' + str(Counter))

direction = ['CW', 'CCW']
TBRL = ['T', 'B', 'R', 'L']

Rocket_Image = PhotoImage('Rocket.png')
CW_Image = PhotoImage(file='/home/pi/NF-Accelerometer Code/NF-Accelerometer-Python-Code/CW.png')
CCW_Image = PhotoImage(file='/home/pi/NF-Accelerometer Code/NF-Accelerometer-Python-Code/CCW.png')
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
f8 = Frame(root, bd=5)
f9 = Frame(root, bd=5)
f10 = Frame(root, bd=5, relief=RAISED)
f11 = Frame(root, bd=5, relief=RAISED)
f12 = Frame(root, bd=5)

f1.grid(row=0, columnspan=3, sticky=N)
f2.grid(row=1, column=0, sticky=NW)
f3.grid(row=2, column=0, sticky=NW)
f4.grid(row=3, column=0, sticky=NW)
f5.grid(row=4, column=0, sticky=NW)
f6.grid(row=5, column=0, sticky=NW)
f7.grid(row=5, column=1, sticky=NW)
f8.grid(row=6, column=1, columnspan=2, sticky=EW)
f9.grid(row=7, column=1, columnspan=2, sticky=EW)
f10.grid(row=1, column=1, columnspan=1)
f11.grid(row=2, column=1, columnspan=1)
f12.grid(row=4, column=1, sticky=EW)

#### frame 1
headr = Label(f1, text='Acceleration Measurement', font=("Ariel 30 bold underline")).pack()

#### frame 2
g_label = Label(f2, text='Desired g:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)
g_entry = Entry(f2, width=4, font=("Ariel 18"), justify="right")
g_entry.pack(side=LEFT, padx=2, pady=5)
g_units_label = Label(f2, text='g [m/s\u00B2]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

#### frame 3
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
Fall_time_units_label = Label(f6, text='[sec]', font=("Ariel 18")).pack(side=LEFT, padx=2, pady=5)

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
Which_is_connected_label = Label(f7, text='Which side is connected:', font=("Ariel 20 bold underline")).pack(anchor=W, padx=2, pady=5)

for index in range(len(TBRL)):
    radiobutton = Radiobutton(f7,
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


root.mainloop()