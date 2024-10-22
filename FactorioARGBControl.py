import win32gui
import win32con
import win32api
import time
import pyautogui
import pygame

xSearch = 'XSmall.png'
bottomBar = 'BottomBar.png'
threat_button = 'Breathing.png'
no_threat_button = 'Spectrum.png'
confidence_level = 0.7  # 70% match confidence
search_region = None
no_threat_click_position = None
threat_click_position = None
hwnd = None

def initMasterPlus():
    # Initialize the mixer module
    pygame.mixer.init()
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

def initFactorio():
    global search_region
    while not search_region:
        try:
            # Search for the image within the specified region with confidence
            search_region = pyautogui.locateOnScreen(bottomBar, confidence=0.9)

            if search_region:
                left = int(search_region.left)
                top = int(search_region.top)
                pygame.mixer.music.play()
                # print(f"Toolbar found at: {search_region}")
                # print(f"Left {left}")
                # print(f"Top {top}")
                # Optional: Move the mouse to the center of the found image
                #pyautogui.moveTo(pyautogui.center(location))
                
        except pyautogui.ImageNotFoundException:
            pass
            #print("ImageNotFoundException: The specified image could not be found.") 
        
        time.sleep(1)

    top = top - 100
    width = 150
    height = 150
    search_region = (left, top, width, height)
    pygame.mixer.music.load("trumpet.mp3")
    pygame.mixer.music.play()

def get_window_handle(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print(f"Window '{window_title}' not found.")
    return hwnd

def click_on_background_window(hwnd, pos):
    # Post a click message to the window without bringing it to the front
    # print("pos[0]" + str(int(pos[0])) + " pos[1]:" + str(int(pos[1])))
    lParam = win32api.MAKELONG(pos[0], pos[1])
    #win32gui.SetForegroundWindow(hwnd)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

def monitorFactorio():
    dangerMode = False
    noThreatTime = 0
    waitTime = 3
    while True:
        try:
            # Search for the image on the screen
            spot = pyautogui.locateOnScreen(xSearch, region=search_region, confidence=confidence_level) #region=search_region, 

            noThreatTime = -1
            if not dangerMode:
                #detectTime = time.time()
                dangerMode = True
                # print("Dangermode True")
                click_on_background_window(hwnd, threat_click_position)  # Replace with your desired coordinates
                pass
                # print("Clicking on danger position")
            #print(f"Image found at: {location}")
            # Optional: Move the mouse to the center of the found image
            #pyautogui.moveTo(pyautogui.center(location))
                
        except pyautogui.ImageNotFoundException:
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

if __name__ == "__main__":
    initMasterPlus()
    initFactorio()
    monitorFactorio()