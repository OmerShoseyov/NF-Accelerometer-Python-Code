import serial
import time
import csv
import pyautogui
import keyboard  # This requires the `keyboard` module (install with `pip install keyboard`)

# Specify the COM port and the baud rate
Arduino_Port = 'COM5'
TEC_and_Tc_Arduino = serial.Serial(Arduino_Port, 115200, timeout=0.1)  # Arduino Serial port configuration

line_from_arduino = ''
data_to_send = ''
send_setpoint = [10, 15, 20]  # Setpoint values
go = 0
flag = 0
setpoint_index = 0
start_time = None  # Initialize start_time to None
valid_data_received = False  # To check when valid data starts arriving

# Define expected range for T1, T2, T3 values (modify these based on your application)
T1_RANGE = (0, 100)  # Example: 0 to 100°C
T2_RANGE = (0, 100)
T3_RANGE = (0, 100)

time.sleep(2)

# Initial check if any data is available and clear the buffer
if TEC_and_Tc_Arduino.inWaiting() > 0:
    line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
    print(f"Initial read: {line_from_arduino}")
    data_to_send = '0 1\n'
    TEC_and_Tc_Arduino.write(data_to_send.encode())
    data_to_send = '1 10\n'
    TEC_and_Tc_Arduino.write(data_to_send.encode())

    for i in range(15):
        line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
        print(i, line_from_arduino)
        time.sleep(0.1)

    time.sleep(0.5)
    line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
    print(line_from_arduino)

    go = 1
    flag = 1  # Ensure the flag is set so the loop runs

def is_valid_temperature(value, value_range):
    """Helper function to check if a value is within an expected range."""
    try:
        temp = float(value)
        return value_range[0] <= temp <= value_range[1]
    except ValueError:
        return False

if go == 1:
    ###################################################
    what_to_do = 2  # Set your what_to_do mode here (0, 1, or 2)

    if what_to_do == 0:
        data_to_send = '0 1\n'
        TEC_and_Tc_Arduino.write(data_to_send.encode())
        flag = 1

    if what_to_do == 1:
        # Open the CSV file for what_to_do == 1
        with open('what_to_do_1_log.csv', mode='w', newline='') as file1:
            writer_1 = csv.writer(file1)
            writer_1.writerow(['Time (ms)', 'Setpoint', 'T1', 'T2', 'T3'])

            data_to_send = '1 ' + str(send_setpoint[setpoint_index]) + '\n'
            TEC_and_Tc_Arduino.write(data_to_send.encode())
            if start_time is None:  # Only set start_time once
                start_time = time.time()  # Start the time tracker

            while flag == 1:
                current_time = time.time()
                elapsed_time_ms = int((current_time - start_time) * 1000)  # Time in milliseconds since the first valid data start

                if not valid_data_received:
                    # Ignore initial invalid data
                    if TEC_and_Tc_Arduino.inWaiting() > 0:
                        line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
                        print(f"Initial data: {line_from_arduino}")  # Debugging output
                        parts = line_from_arduino.split('\t')
                        if (len(parts) == 3 and
                            all(is_valid_temperature(parts[i], [T1_RANGE, T2_RANGE, T3_RANGE][i]) for i in range(3))):
                            t1, t2, t3 = parts
                            valid_data_received = True
                            print("Valid data received, starting continuous logging.")
                        else:
                            print(f"Invalid data format or out of range: {line_from_arduino}")  # Improved handling of unexpected data
                            data_to_send = '1 ' + str(send_setpoint[setpoint_index]) + '\n'
                            TEC_and_Tc_Arduino.write(data_to_send.encode())
                    continue  # Skip to the next loop iteration

                # Continuously read and log incoming data from Arduino
                if TEC_and_Tc_Arduino.inWaiting() > 0:
                    line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
                    print(f"Received: {line_from_arduino}")
                    parts = line_from_arduino.split('\t')
                    if (len(parts) == 3 and
                        all(is_valid_temperature(parts[i], [T1_RANGE, T2_RANGE, T3_RANGE][i]) for i in range(3))):
                        t1, t2, t3 = parts
                        writer_1.writerow([elapsed_time_ms, send_setpoint[setpoint_index], t1, t2, t3])
                    else:
                        print(f"Invalid data format or out of range: {line_from_arduino}")

                # Send the next setpoint every 5 seconds
                if current_time - start_time >= 5 * (setpoint_index + 1):
                    setpoint_index += 1
                    time.sleep(0.1)
                    if setpoint_index >= len(send_setpoint):
                        print("All setpoints sent. Stopping...")
                        flag = 0
                        break

                    data_to_send = '1 ' + str(send_setpoint[setpoint_index]) + '\n'
                    TEC_and_Tc_Arduino.write(data_to_send.encode())
                    valid_data_received = False  # Reset to ensure next set of data is validated

                time.sleep(0.01)

    if what_to_do == 2:
        # Open the CSV file for what_to_do == 2
        with open('what_to_do_2_log.csv', mode='w', newline='') as file2:
            writer_2 = csv.writer(file2)
            writer_2.writerow(['Time (ms)', 'T2', 'T3'])

            data_to_send = '2 1\n'
            TEC_and_Tc_Arduino.write(data_to_send.encode())
            start_time = None  # Reset start_time for what_to_do == 2

            while flag == 1:
                current_time = time.time()
                if start_time is None:  # Set start_time on the first valid data
                    start_time = current_time

                elapsed_time_ms = int((current_time - start_time) * 1000)  # Time in milliseconds since the first valid data start

                if not valid_data_received:
                    # Ignore initial invalid data
                    if TEC_and_Tc_Arduino.inWaiting() > 0:
                        line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
                        print(f"Initial data: {line_from_arduino}")  # Debugging output
                        parts = line_from_arduino.split('\t')
                        if (len(parts) == 2 and
                            is_valid_temperature(parts[0], T2_RANGE) and is_valid_temperature(parts[1], T3_RANGE)):
                            t2, t3 = parts
                            valid_data_received = True
                            start_time = current_time  # Reset start_time to make the first valid data's time 0
                            elapsed_time_ms = 0  # Ensure the first valid data's time is 0 ms
                            print("Valid data received, starting continuous logging.")
                        else:
                            print(f"Invalid data format or out of range: {line_from_arduino}")  # Improved handling of unexpected data
                    continue  # Skip to the next loop iteration

                # Continuously read and log incoming data from Arduino
                if TEC_and_Tc_Arduino.inWaiting() > 0:
                    line_from_arduino = TEC_and_Tc_Arduino.readline().decode().strip()
                    print(f"Received: {line_from_arduino}")
                    parts = line_from_arduino.split('\t')
                    if (len(parts) == 2 and
                        is_valid_temperature(parts[0], T2_RANGE) and is_valid_temperature(parts[1], T3_RANGE)):
                        t2, t3 = parts
                        writer_2.writerow([elapsed_time_ms, t2, t3])
                    else:
                        print(f"Invalid data format or out of range: {line_from_arduino}")

                # Check for 'q' key press to stop the script
                if keyboard.is_pressed('q'):
                    print("Q key pressed. Stopping...")
                    flag = 0
                    break

                time.sleep(0.01)

# Close the serial connection
data_to_send = '0 1\n'
TEC_and_Tc_Arduino.write(data_to_send.encode())
TEC_and_Tc_Arduino.close()
