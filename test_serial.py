import serial
import time
import math

TIME_COUNTER = 1


def save_data(file_name, time, current, x_mems="", y_mems="", z_mems=""):
    # y = str(time) + ', ' + str(current) + ', ' + str(x_mems) + ', ' + str(y_mems) + ', ' + str(z_mems)
    data_to_save = "At time: " + str(time) + ', The current is: ' + str(current) 
    file_name.write(data_to_save)
    #print(data_to_save)


def send_pin_num_to_light(number_str):
    """
    sends to the arduino what 'leg' to put voltage
    :param number: gets the  
    :return: 
    """    
    # number_str = str(number)
    serial_arduino_nano.write(str.encode(number_str + '\n'))


def get_data():
    # line = 0 
    # if serial_arduino_nano.in_waiting > 0:
    #     a = 4
    line = serial_arduino_nano.readline().decode()
    return line

if __name__ == '__main__':
    serial_arduino_nano = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
    serial_arduino_nano.reset_input_buffer()
    new_file = open('noe_home_try7.txt', 'w')

    counter = 0
    while True:
        if(counter>0):
            time.sleep(1)
        for i in range(6):
            serial_arduino_nano.reset_input_buffer()
            start_time = time.time()
            while (time.time() - start_time) < TIME_COUNTER:
                num_to_send = str(i+1)
                send_pin_num_to_light(num_to_send)
                line = get_data()
                print('i = '+ str(i) +', current is ' + line)
                print(15*'*')
                save_data(new_file, time.time() - start_time, line)




    # f = False
    # while True:
        # for i in range(1):
        # while not f:
            # serial_arduino_nano.reset_input_buffer() # Cleans all the data that might be inside buffer. 
            # new_file = open('noe_home_try7.txt', 'w')
            # start_time = time.time()
            # if i>0: # If it's not the first call, this is the stop between 2 callings (for the arduino)
            #     send_pin_num_to_light(555) 
            # send_pin_num_to_light(1)
            # # while (time.time() - start_time) < TIME_COUNTER: #We keep sending data on same leg for a duration of TIME_COUNTER  
            #     # time.sleep(0.5)      
            # line = get_data()
            #     # if str(line) != 'None':
            # print(line)

    
    
