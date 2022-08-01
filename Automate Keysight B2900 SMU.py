import pyautogui 
import time
import serial

######Constants######
file_name = 'test4'
Path = r'C:\Users\accel\OneDrive\Desktop\Omer\Test'
Arduino_Port = 'COM4'


arduino_triger = serial.Serial(Arduino_Port, 115200, timeout=0.1) # Arduino Serial port configuration
triger = 0

#relevant_region = pyautogui.locateOnScreen('relevant region.PNG', confidence=0.8) 
cnt = 0
index = 1

try:
    while True:
        
        if arduino_triger.inWaiting() > 0:
            #print('in3')
            triger = arduino_triger.readline().decode() 
            triger = int(triger)
            cnt = 1
        
        if triger == 1:
            if cnt == 1:
                #print('in1')
                ###Start Measurement###
                x, y = pyautogui.locateCenterOnScreen('Start Measurement.PNG', confidence=0.8)
                #print(x, y)
                pyautogui.moveTo(x, y)
                pyautogui.click()  

                ###Move to plot window###
                x, y = pyautogui.locateCenterOnScreen('Graph.PNG', confidence=0.8)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                cnt = 0

        if triger == 0:
            if cnt == 1:
                #print('in0')
                ###Stop Measurement###
                x, y = pyautogui.locateCenterOnScreen('Stop Measurement.PNG', confidence=0.8)
                #print(x, y)
                pyautogui.moveTo(x, y)
                pyautogui.click() 

                ###Save Measurement###
                x, y = pyautogui.locateCenterOnScreen('Table.PNG', confidence=0.8)
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
                x, y = pyautogui.locateCenterOnScreen('Graph.PNG', confidence=0.8)
                pyautogui.moveTo(x, y)
                pyautogui.click() 
                cnt = 0

except KeyboardInterrupt:
    print('out')  
         
