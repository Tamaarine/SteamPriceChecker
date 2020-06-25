import pyautogui
import keyboard

punching = False

while True:

    if keyboard.is_pressed("."):
        punching = True
    if keyboard.is_pressed("/"):
        punching = False

    if punching:
        pyautogui.click()