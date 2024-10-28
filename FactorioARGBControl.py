from re import search
import win32gui
import win32con
import win32api
import time
import pyautogui
import pygame
import keyboard
from PIL import Image

xSearch = 'XSmall.png'
threat_button = 'Breathing.png'
no_threat_button = 'Spectrum.png'
confidence_level = 0.7  # 70% match confidence
search_region = None
no_threat_click_position = None
threat_click_position = None
hwnd = None

def initMasterPlus():
    # Load the audio file
    pygame.mixer.music.load("bell.mp3")

    window_title = "Cooler Master MasterPlus <Ver: 195.0340.0411>"  # Replace with the actual window title
    #window_title = "Book1 - Excel"  # Replace with the actual window title
    global hwnd
    hwnd = get_window_handle(window_title)

    global no_threat_click_position
    global threat_click_position

    while not no_threat_click_position or not threat_click_position:
        try:
            # Search for the image within the specified region with confidence
            no_threat_click_position = pyautogui.center(pyautogui.locateOnScreen(no_threat_button, confidence=0.9))
            threat_click_position = pyautogui.center(pyautogui.locateOnScreen(threat_button, confidence=0.9))
                
        except pyautogui.ImageNotFoundException:
            pass
            #print("ImageNotFoundException: The specified image could not be found.") 
        
        time.sleep(1)
    
    pygame.mixer.music.play()

def get_window_handle(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print(f"Window '{window_title}' not found.")
    return hwnd

def click_on_background_window(hwnd, pos):
    # Post a click message to the window without bringing it to the front
    # print("pos[0]" + str(int(pos[0])) + " pos[1]:" + str(int(pos[1])))
    try:
        lParam = win32api.MAKELONG(pos[0], pos[1])
        #win32gui.SetForegroundWindow(hwnd)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    except TypeError:
        print("Coolermaster Window Not Found")

def monitorFactorio():
    dangerMode = False
    noThreatTime = 0
    waitTime = 3
    while True:
        try:
            # Search for the image on the screen
            spot = pyautogui.locateOnScreen(xSearch, region=search_region, confidence=confidence_level) #region=search_region, 
            print("Threat Detected")
            noThreatTime = -1
            if not dangerMode:
                #detectTime = time.time()
                dangerMode = True
                #print("Danger Detected")
                click_on_background_window(hwnd, threat_click_position)  # Replace with your desired coordinates
                pass
                
        except pyautogui.ImageNotFoundException:
            print("No Threat Detected")
            # print("Threat Image not found")
            if noThreatTime == -1:
                noThreatTime = time.time()
                # print("Threat timer started")
            else:
                if dangerMode:
                    # print ("Dangermode True after threat timer started")
                    if time.time() - noThreatTime > waitTime:
                        dangerMode = False
                        click_on_background_window(hwnd, no_threat_click_position)
                        # print("Clicking on safe position")

        time.sleep(0.3)

def update_danger_position():
    global search_region, confidence_level
    search_region = None
    while not search_region:
        try:
            search_region = pyautogui.locateOnScreen(xSearch, confidence=confidence_level)

            if search_region:
                left = int(search_region.left)
                top = int(search_region.top)
                #pygame.mixer.music.play()
                
        except pyautogui.ImageNotFoundException:
            pass
            #print("ImageNotFoundException: The specified image could not be found.") 
        
        time.sleep(1)

    with Image.open(xSearch) as img:
        width, height = img.size

    search_region = (left, top, width, height)
    pygame.mixer.music.load("trumpet.mp3")
    pygame.mixer.music.play()

def detect_key_combination():
    print("Listening for Control + Shift + R...")
    # Detects when the keys Control + Shift + R are pressed together
    keyboard.add_hotkey('ctrl+shift+r', update_danger_position)

if __name__ == "__main__":
    pygame.mixer.init()         # Initialize the mixer module
    detect_key_combination()    # Start listening for ctrl+shift+r to reassign the x position
    #initMasterPlus()           # Find and ready the coolermaster software for control
    # update_danger_position()  # Look for the X for the first time, could do this by default, but could also only do it on command to be more performant.
    monitorFactorio()           # begin the main monitoring loop