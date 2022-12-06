import os
import cv2
import numpy as np
import json
import urllib
import requests
import customtkinter
from tkinter import *
from PIL import Image

from data.n import n
from data.c import c


class HcaptchaImagesDownloader:
    def __init__(self, host, sitekey):
        self.host = host
        self.sitekey = sitekey
        self.counter = 1
        self.directory = os.getcwd()
        self.questions = self.get_questions()
        self.currentquestion = None

    def download_images(self):
        self.c = c(self.host, self.sitekey)
        self.c['type'] = 'hsl'

        self.res = self.get_captcha()

        question = self.res['requester_question']['en'].replace(
            'Please click each image containing a ', '').replace('Please click each image containing an ', '').replace('Please click each image containing ', '')

        self.currentquestion = question
        
        if question not in self.questions:
            self.questions.append(question)
            self.write_question(question)

        urls = []

        urls.extend(self.res['requester_question_example'])

        for captcha in self.res['tasklist']:
            url = captcha['datapoint_uri']
            urls.append(url)

        for url in urls:
            print(f'Image {self.counter} [{url[:40].replace("https://", "")}...] | Q: {question}')
            res = requests.get(url, stream=True).raw
            image = np.asarray(bytearray(res.read()), dtype='uint8')
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (128, 128))
            self.panel(image)

    def get_captcha(self):
        data = {
            "sitekey": self.sitekey,
            "v": "b1129b9",
            "host": self.host,
            "n": n(self.c["req"]),
            'motiondata': '{"st":1628923867722,"mm":[[203,16,1628923874730],[155,42,1628923874753],[137,53,1628923874770],[122,62,1628923874793],[120,62,1628923875020],[107,62,1628923875042],[100,61,1628923875058],[93,60,1628923875074],[89,59,1628923875090],[88,59,1628923875106],[87,59,1628923875131],[87,59,1628923875155],[84,56,1628923875171],[76,51,1628923875187],[70,47,1628923875203],[65,44,1628923875219],[63,42,1628923875235],[62,41,1628923875251],[61,41,1628923875307],[58,39,1628923875324],[54,38,1628923875340],[49,36,1628923875363],[44,36,1628923875380],[41,35,1628923875396],[40,35,1628923875412],[38,35,1628923875428],[38,35,1628923875444],[37,35,1628923875460],[37,35,1628923875476],[37,35,1628923875492]],"mm-mp":13.05084745762712,"md":[[37,35,1628923875529]],"md-mp":0,"mu":[[37,35,1628923875586]],"mu-mp":0,"v":1,"topLevel":{"st":1628923867123,"sc":{"availWidth":1680,"availHeight":932,"width":1680,"height":1050,"colorDepth":30,"pixelDepth":30,"availLeft":0,"availTop":23},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"webkitTemporaryStorage":{},"webkitPersistentStorage":{},"hardwareConcurrency":12,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36","platform":"MacIntel","product":"Gecko","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36","language":"en-US","languages":["en-US","en"],"onLine":true,"webdriver":false,"serial":{},"scheduling":{},"xr":{},"mediaCapabilities":{},"permissions":{},"locks":{},"usb":{},"mediaSession":{},"clipboard":{},"credentials":{},"keyboard":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"wakeLock":{},"deviceMemory":8,"hid":{},"presentation":{},"userAgentData":{},"bluetooth":{},"managed":{},"plugins":["internal-pdf-viewer","mhjfbmdgcfjbbpaeojofohoefgiehjai","internal-nacl-plugin"]},"dr":"https://discord.com/","inv":false,"exec":false,"wn":[[1463,731,2,1628923867124],[733,731,2,1628923871704]],"wn-mp":4580,"xy":[[0,0,1,1628923867125]],"xy-mp":0,"mm":[[1108,233,1628923867644],[1110,230,1628923867660],[1125,212,1628923867678],[1140,195,1628923867694],[1158,173,1628923867711],[1179,152,1628923867727],[1199,133,1628923867744],[1221,114,1628923867768],[1257,90,1628923867795],[1272,82,1628923867811],[1287,76,1628923867827],[1299,71,1628923867844],[1309,68,1628923867861],[1315,66,1628923867877],[1326,64,1628923867894],[1331,62,1628923867911],[1336,60,1628923867927],[1339,58,1628923867944],[1343,56,1628923867961],[1345,54,1628923867978],[1347,53,1628923867994],[1348,52,1628923868011],[1350,51,1628923868028],[1354,49,1628923868045],[1366,44,1628923868077],[1374,41,1628923868094],[1388,36,1628923868110],[1399,31,1628923868127],[1413,25,1628923868144],[1424,18,1628923868161],[1436,10,1628923868178],[1445,3,1628923868195],[995,502,1628923871369],[722,324,1628923874673],[625,356,1628923874689],[523,397,1628923874705],[457,425,1628923874721]],"mm-mp":164.7674418604651},"session":[],"widgetList":["0a1l5c3yudk4"],"widgetId":"0a1l5c3yudk4","href":"https://discord.com/register","prev":{"escaped":false,"passed":false,"expiredChallenge":false,"expiredResponse":false}}',
            "hl": "en",
            "c": json.dumps(self.c)
        }
        cookies = {"hc_accessibility": "VdfzG99DjOoLGlqlwSuIjToEryE7Xcx0z4lPWbLBLLCqCfpG9z2X5J+BwkOMrjbNFUKB60TAPpTsW7pzcBQIu0vztY6DQDLzZqpvKUKjyx9RxILDx8wCXq/z1OLjRPib7Cu4t+b4gEaoTbGD240IIXCRN33czAf3d4nr4HxcUsedKNT/cMp4xDo93HBxiSHYMBg3HvE4M3frwKUlSEDrSVG5Bg5FqxlokBLSIhWuQ2SAmiwiOwGLpvknsZHClqPnaI6KA3iyhMrDOO/f8fFxTpGiik3xqlfpKzc783UKVR8Epwbhdeq7bfhNKQMnZkG4Ac9j5PFHgA1GePaKIETUuxVyABISiA4lEg5B0HuEGJUd5Rxl2qlv/AvFAtyqwYU8XUgMIML35IMUXtr4CVeihSLhqeV5+IBOHakiD54vu0IwuEi/BjYh+jkcks4=1qyF568EcE9myCKI"}
        return requests.post(f"https://hcaptcha.com/getcaptcha?s={self.sitekey}", cookies=cookies, data=urllib.parse.urlencode(data), headers={
            "Host": "hcaptcha.com",
            "Connection": "keep-alive",
            "sec-ch-ua": 'Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92',
            "Accept": "application/json",
            "sec-ch-ua-mobile": "?0",
            "Content-length": str(len(data)),
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Content-type": "application/x-www-form-urlencoded",
            "Origin": "https://newassets.hcaptcha.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://newassets.hcaptcha.com/",
            "Accept-Language": "en-US,en;q=0.9"

        }, timeout=4).json()


    def panel(self, img):
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.root = customtkinter.CTk()
        
        self.root.title('hCaptcha')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 950
        window_height = 800
    
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(str(window_height) + 'x' + str(window_width) +
                        '+' + str(x_coordinate) + '+' + str(y_coordinate))
        # self.root.resizable(False, False)

        # set grid layout 1x2
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        navigation_frame = customtkinter.CTkFrame(self.root, corner_radius=0)
        navigation_frame.grid(row=0, column=0, sticky="nsew")
        navigation_frame.grid_rowconfigure(4, weight=1)
        navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="  hCap Img Scraper", image=logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        home_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=home_image, anchor="w", command=self.home_button_event)
        home_button.grid(row=1, column=0, sticky="ew")

        devframe_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Authors",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=add_user_image, anchor="w", command=self.devframe_button_event)
        devframe_button.grid(row=2, column=0, sticky="ew")

        exit_button = customtkinter.CTkButton(navigation_frame, text="EXIT", command = self.root.quit)
        exit_button.grid(row=5, column=0, sticky="ew")

        appearance_mode_menu = customtkinter.CTkOptionMenu(navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")



        # create home frame
        home_frame = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        home_frame.grid_columnconfigure(0, weight=1)


        image = customtkinter.CTkImage(Image.fromarray(img), size=(150, 150))
        
        customtkinter.CTkLabel(home_frame, text="", image=image).place(relx = 0.95, rely = 0.5, anchor = "e")
    
        customtkinter.CTkButton(home_frame, text="N/A", command = lambda:self.root.destroy()).place(relx = 1, rely = 0, anchor = "ne")
        

        xrow = 0
        for button in self.questions:
            if button == self.currentquestion:
                customtkinter.CTkButton(home_frame, text=button, command=lambda button=button: [
                        self.save_image(button, img), self.root.destroy()]).place(relx = 0.95, rely = 0.6, anchor = "e")
            else:
                customtkinter.CTkButton(home_frame, text=button, command=lambda button=button: [
                        self.save_image(button, img), self.root.destroy()]).grid(sticky="W", row=xrow,column=0,padx=10,pady=0.5)
                xrow += 1



        # create second frame
        second_frame = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        second_frame_label = customtkinter.CTkLabel(second_frame, text="Authors", font=customtkinter.CTkFont(size=15, weight="bold"))
        second_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # select default frame
        self.select_frame_by_name(home_button, devframe_button, home_frame, second_frame, "home")
        
        
        self.root.mainloop()
          
                

    def select_frame_by_name(self, home_button=None, devframe_button=None, home_frame=None, second_frame=None, name="home"):
        # set button color for selected button
        home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        devframe_button.configure(fg_color=("gray75", "gray25") if name == "devframe" else "transparent")
        
        # show selected frame
        if name == "home": home_frame.grid(row=0, column=1, sticky="nsew")
        else: home_frame.grid_forget()
        
        if name == "devframe": second_frame.grid(row=0, column=1, sticky="nsew")
        else: second_frame.grid_forget()

    def home_button_event(self): self.select_frame_by_name("home")
    def devframe_button_event(self): self.select_frame_by_name("devframe")
    def change_appearance_mode_event(self, new_appearance_mode): customtkinter.set_appearance_mode(new_appearance_mode)


    def save_image(self, button, image):
        folder = os.path.join(self.directory, 'images', button)
        if not os.path.isdir(folder):
            os.mkdir(folder)

        cv2.imwrite(os.path.join(folder, 'image_' +
                    str(self.counter) + '.png'), image)
        self.counter += 1

    def get_questions(self):
        with open('questions.txt', 'r') as f:
            return f.read().splitlines()

    def write_question(self, question):
        question += '\n'
        with open('questions.txt', 'a+') as f:
            f.seek(0)

            if question in f.read().splitlines():
                return

            f.write(question)


if __name__ == '__main__':
    capdl = HcaptchaImagesDownloader(
        'discord.com', '4c672d35-0701-42b2-88c3-78380b0db560')
    while True:
        capdl.download_images()
