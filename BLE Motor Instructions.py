from bluepy import btle
import time



#Have to match with Peripheral
MAC = "a8:61:0a:24:66:2e"
BLE_UUID_MOTOR_INSTRUCTIONS_SERVICE =       "9e661242-e694-4262-b393-61744b474383"
BLE_UUID_GET_G =                            "73cce820-35ee-47f2-bca7-31105f673e20"
BLE_UUID_ROTATION_DIRECTION =               "aae6924e-fdd1-40d7-9e71-b026bcec5cc9"
BLE_UUID_MEASUREMENT_TIME =                 "80077d16-c5c6-48c4-8c10-7da0b6fe3e6f"
BLE_UUID_START_FINISH =                     "40e0f2d5-2327-4930-83ca-c2ca729ca1bb"
BLE_UUID_STATUS =                           "5720e451-6f72-49f1-8721-079d7e4bb497"

try:
    while True:
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
            get_g, r_dir, m_time = [x for x in input('Enter = Wanted g, Rotation Direction, Measurement Duration ').split()]

            get_g_byte = get_g.encode()
            r_dir_byte = r_dir.encode()
            m_time_byte = m_time.encode()
            s_f = '1'.encode()
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
            Start_Finish_Characteristic.write(s_f, True)
            #print(s_f)
            print(f'Start_Finish = {Start_Finish_Characteristic.read()}')
            #time.sleep(0.2)

            Odrive_Arduino.disconnect()
            print('-----Bye-----')

        time.sleep(5)
except KeyboardInterrupt:
    s_f = '0'.encode()
    Start_Finish_Characteristic.write(s_f, True)
    Odrive_Arduino.disconnect()

    


