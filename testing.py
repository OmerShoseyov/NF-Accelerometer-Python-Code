""" import pyautogui 
import time

print(pyautogui.size())
pyautogui.moveTo(224, 98)
while True:
    print(pyautogui.position())
    time.sleep(0.5)   """    

file_name = 'test'
Path = r'C:\Users\accel\OneDrive\Desktop\Omer\Test'
index = 1
print(Path + '\\' + file_name + '_' + str(index))   