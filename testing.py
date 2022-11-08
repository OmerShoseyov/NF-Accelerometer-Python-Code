
import pyautogui 

x, y = pyautogui.locateCenterOnScreen('Start Measurement.PNG', confidence=0.75)
print(x, y)