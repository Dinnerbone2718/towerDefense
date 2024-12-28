import pygame
import sys
import os
import numpy as np
import time
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
import asyncio
from threading import Thread
import json
import pstats
import cProfile
import tkinter as tk
from tkinter import ttk
from collections import deque
import re
import ctypes

#re.sub(r'\d+', '', self.selected)
#HarmonyOS Sans SC  Size = 28

# Get the directory path of the current script*
script_dir = os.path.dirname(os.path.abspath(__file__))
prefix = f"{script_dir}/"

print(prefix)

# Initialize pygame library
pygame.init()
pygame.mixer.init()







# Set up the main display window with double buffering for smoother rendering

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

print(screensize)

screenDis = pygame.display.set_mode((1200, 900), pygame.SCALED | pygame.DOUBLEBUF)
screen = pygame.surface.Surface((1200, 900), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption('Tower Defense')
pygame.display.set_icon(pygame.image.load(f"{prefix}icon1.png"))

# Path to your service account key file
service_account_key = f"{prefix}towerdefense-ce12a-firebase-adminsdk-pz797-cafdf36b1a.json"

# Initialize the Firebase Admin SDK
#cred = credentials.Certificate(service_account_key)
#firebase_admin.initialize_app(cred, {
    #'databaseURL': 'https://towerdefense-ce12a-default-rtdb.firebaseio.com/'
#})




with open(f"{prefix}saves/savegame.json", "r") as file:
    data = json.load(file)




# Global Varibles
volume = 100
ownedmaps = data.get("maps")
cash = data.get("cash")
ownedSkins = data.get("skins")


skinsApplied = {
    "Box": 0,
    "Calico": 0 ,
    "Dumb": 0,
    "Fat": 0,
    "fishFarm": 0,
    "Gun": 0,
    "Magic": 0  ,
    "Tank": 0,    

}




class Button:
    def __init__(self, name, x, y, width, height, load=0):
        self.hover = pygame.image.load(f"{prefix}UI/{name}1.png").convert_alpha()
        self.hover = pygame.transform.scale(self.hover, (width, height))
        self.basic = pygame.image.load(f"{prefix}UI/{name}0.png").convert_alpha()
        self.basic = pygame.transform.scale(self.basic, (width, height))
        self.width = width
        self.height = height
        self.name = name
        self.load = load
        self.x = x
        self.y = y
        pass

    def update(self):

        if self.name == "loadButton":
            if os.path.exists(f"{prefix}saves/save{self.load}.json") == False:
                return

        drawX = self.x - self.basic.get_width() // 2
        drawY = self.y - self.basic.get_height() // 2
        
        if drawX < mousePos[0] < drawX + self.width and drawY < mousePos[1] < drawY + self.height:
            screen.blit(self.hover, (drawX, drawY))
            if mousePress[0] and mouseUp == True:
                self.special()
        else:
            screen.blit(self.basic, (drawX, drawY))

    def special(self):
        global inGame, ownedmaps, cash, screenDis
        if self.name == "playButton":
            menu.currentScreen = "menu"

        if self.name == "onlineButton":
            menu.currentScreen = "onlineScreen"
        

        if self.name == "backButton":
            menu.currentScreen = "title"
            pygame.mixer_music.stop()

        if self.name == "map1Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 1
        elif self.name == "map2Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 2
        elif self.name == "map3Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 3
        elif self.name == "map4Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 4
        elif self.name == "map5Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 5
        elif self.name == "map6Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 6
        elif self.name == "map7Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 7
        elif self.name == "map8Select":
            menu.currentScreen = "gameSelected"
            menu.mapDisplay = 8



        if self.name == "settingsButton":
            pygame.mixer.music.load(f"{prefix}music/SettingsSong.mp3")
            pygame.mixer.music.play(-1)  
            menu.currentScreen = "settings"
        if self.name == "toggleFullscreen":
            if screenDis.get_width() == 1200:
                screenDis = pygame.display.set_mode((screensize[0], screensize[1]), pygame.SCALED | pygame.DOUBLEBUF | pygame.FULLSCREEN) 
            else:
                screenDis = pygame.display.set_mode((1200, 900), pygame.SCALED | pygame.DOUBLEBUF)

        if self.name == "joinButton":
            removeAFK()
            client.isOnline = True

        if self.name == "loadButton":
            with open(f"{prefix}saves/save{self.load}.json", "r") as file:
                data = json.load(file)
            inGame = True
            game.loadGame(data, self.load)

        if self.name == "shopButton":
            menu.currentScreen = "shop"

        if self.name == "spinnerButton":
            menu.currentScreen = "casino"

        if self.name == "easyButton":
            menu.difficulty = 2

        if self.name == "mediumButton":
            menu.difficulty = 3

        if self.name == "hardButton":
            menu.difficulty = 1

        if self.name == "leaveServerButton":
            client.isOnline = False
            client.inGame = False
            client.host = False
            client.clientCooldown = 0
            client.selectedID = None
            client.upgradeQueue = []
            client.queue = []
            removeSelf()

        if self.name == "casinoBack":
            menu.currentScreen = "shop"

        if self.name == "skinButton":
            menu.currentScreen = "skins"

        if self.name == "next":
            if menu.currentScreen == "menu":
                menu.currentScreen = "menu2"
            else:
                menu.currentScreen = "menu"
        
        if self.name == "spinButton":
            if int(min(np.floor(cash*.01), 9999)) >= 50:
                menu.spin = True
                cash -= 5000

        if self.name == "map6buy":
            if int(min(np.floor(cash*.01), 9999)) >= 200:
                   ownedmaps.append(6)
                   cash -= 20000

        if self.name == "map7buy":
            if int(min(np.floor(cash*.01), 9999)) >= 200:
                   ownedmaps.append(7)
                   cash -= 20000
        
        if self.name == "back":
            menu.currentScreen = "menu"

        if self.name == "menuCat":
            audio.menuCat.play()

        if self.name == "playButtonInGame":
            game.newGame(menu.mapDisplay, menu.selectedGamemode)
            inGame = True
            menu.currentScreen = "menu"

class Menu:
    def __init__(self):

        self.alternateImages = {
            "Box": ["Box1"],
            "Calico": ["Calico1", "Calico2", "Calico3"],
            "Dumb": ["Dumb1"],
            "Fat": ["Fat1", "Fat2"],
            "fishFarm": ["fishFarm1"],
            "Gun": ["Gun1", "Gun2"],
            "Magic": ["Magic1"],
            "Tank": ["Tank1"]

        }

        self.indexer = {
            "Box": 0,
            "Calico": 0 ,
            "Dumb": 0,
            "Fat": 0,
            "fishFarm": 0,
            "Gun": 0,
            "Magic": 0  ,
            "Tank": 0,       
        }


        self.startImg = pygame.image.load(f"{prefix}UI/titleScreen.png").convert_alpha()
        self.startImg = pygame.transform.scale(self.startImg, (1200, 900))

        self.menuImg = pygame.image.load(f"{prefix}UI/menuScreen.png").convert_alpha()
        self.menuImg = pygame.transform.scale(self.menuImg, (1200, 900))

        self.menuImg2 = pygame.image.load(f"{prefix}UI/menuScreen2.png").convert_alpha()
        self.menuImg2 = pygame.transform.scale(self.menuImg2, (1200, 900))

        self.settingsMenu = pygame.image.load(f"{prefix}UI/settingsMenu.png").convert_alpha()
        self.settingsMenu = pygame.transform.scale(self.settingsMenu, (1200, 900))

        self.lobbyWait = pygame.image.load(f"{prefix}UI/lobbyWait.png").convert_alpha()
        self.lobbyWait = pygame.transform.scale(self.lobbyWait, (1200, 900))    

        self.shopImg = pygame.image.load(f"{prefix}UI/shop.png").convert_alpha()
        self.shopImg = pygame.transform.scale(self.shopImg, (1200, 900))  

        self.casinoImg = pygame.image.load(f"{prefix}UI/casinoBG.png").convert_alpha()
        self.casinoImg = pygame.transform.scale(self.casinoImg, (1200, 900))  

        self.skinSelectionImg = pygame.image.load(f"{prefix}UI/skinSelection.png").convert_alpha()
        self.skinSelectionImg = pygame.transform.scale(self.skinSelectionImg, (1200, 900))  

        self.volumeSlider = pygame.image.load(f"{prefix}UI/volumeSlider.png").convert_alpha()
        self.volumeSlider = pygame.transform.scale(self.volumeSlider, (80, 80))


        self.lobby0 = pygame.image.load(f"{prefix}UI/lobby0.png").convert_alpha()
        self.lobby0 = pygame.transform.scale(self.lobby0, (250, 250))

        self.lobby1 = pygame.image.load(f"{prefix}UI/lobby1.png").convert_alpha()
        self.lobby1 = pygame.transform.scale(self.lobby1, (250, 250))

        self.lobby2 = pygame.image.load(f"{prefix}UI/lobby2.png").convert_alpha()
        self.lobby2 = pygame.transform.scale(self.lobby2, (250, 250))

        self.cashImg = pygame.image.load(f"{prefix}UI/cashIcon.png").convert_alpha()
        self.cashImg = pygame.transform.scale(self.cashImg, (140, 70))

        self.selectedGamemode = "normal"


        self.gameSelectBackground = pygame.image.load(f"{prefix}UI/gameSelectBackground.png").convert_alpha()
        self.gameSelectBackground = pygame.transform.scale(self.gameSelectBackground, (1000, 700))


        self.lobbyMappings = {
            0:self.lobby0,
            1:self.lobby1,
            2:self.lobby2
        }

        self.nameLookup = {
            1:"Mellow Meadows",
            2:"Happy Hills",
            3:"Magma Marsh",
            4:"Paw Planet",
            5:"Lily Pad Lagoon",
            6:"Carnivorous Cave",
            7:"Rocky Road"


        }


        self.difficulty = 2


        self.volumeSliderX = 9999
        self.volumeSliderClickedOn = False

        self.playButton = Button("playButton", 105, 145, 190, 190)

        self.map1Select = Button("map1Select", 450, 245, 180, 180)
        self.map1Load = Button("loadButton", 450, 360, 180, 50, 1)

        self.map2Select = Button("map2Select", 700, 245, 180, 180)
        self.map2Load = Button("loadButton", 700, 360, 180, 50, 2)

        self.map3Select = Button("map3Select", 950, 245, 180, 180)
        self.map3Load = Button("loadButton", 950, 360, 180, 50, 3)

        self.map4Select = Button("map4Select", 450, 495, 180, 180)
        self.map4Load = Button("loadButton", 450, 610, 180, 50, 4)

        self.map5Select = Button("map5Select", 700, 495, 180, 180)
        self.map5Load = Button("loadButton", 700, 610, 180, 50, 5)

        self.map6Select = Button("map6Select", 450, 245, 180, 180)
        self.map6Load = Button("loadButton", 450, 360, 180, 50, 6)

        self.map7Select = Button("map7Select", 700, 245, 180, 180)
        self.map7Load = Button("loadButton", 700, 360, 180, 50, 7)

        self.backButton = Button("backButton", 465, 750, 220, 110)

        self.settingsBackButton = Button("backButton", 210, 155, 220, 110)

        self.settingsButton = Button("settingsButton", 195, 325, 370, 110)

        self.toggleFullscreenButton = Button("toggleFullscreen", 335, 450, 510, 240)

        self.onlineButton = Button("onlineButton", 255, 175, 110,110)

        self.joinButton = Button("joinButton", 200, 145, 220, 110)

        self.currentScreen = "title"

        self.onlineBackButton = Button("backButton", 200, 300, 220, 110)

        self.leaveLobby = Button("leaveServerButton", 230, 210, 260, 110)

        self.nextButton = Button("next", 950, 460, 220, 110)

        self.shopButton = Button("shopButton", 325, 185, 110, 110)

        self.map6buy = Button("map6buy", 210, 400, 220, 300)
        self.map7buy = Button("map7buy", 500, 400, 220, 300)

        self.casinoButton = Button("spinnerButton", 355, 690, 510, 240)

        self.spinButton = Button("spinButton", 210, 590, 200, 90)

        self.casinoBack = Button("casinoBack", 210, 155, 220, 110)

        self.skinButton = Button("skinButton", 270, 465, 220, 110)

        self.menuCat = Button("menuCat",1015, 700, 210,240)

        self.playInGameButton = Button("playButtonInGame", 290, 650, 190,120)

        self.back = Button("back", 1025, 165, 90, 90)

        self.easyButton = Button("easyButton", 290, 415, 110,110)
        self.mediumButton = Button("mediumButton", 290, 415, 110,110)
        self.hardButton = Button("hardButton", 290, 415, 110,110)

        self.normalMode = pygame.image.load(f"{prefix}UI/normalGamemode.png").convert_alpha()
        self.sandboxMode = pygame.image.load(f"{prefix}UI/sandboxGamemode.png").convert_alpha()
        self.moneyHealthMode = pygame.image.load(f"{prefix}UI/moneyHealthGamemode.png").convert_alpha()

        self.clock = pygame.time.Clock()

        self.mapDisplay = 0

        self.spin = False

    def draw_text(self, text, text_col, x, y, size=100, center = False):
        font = pygame.font.Font(f"{prefix}ui/8bitOperatorPlus-Regular.ttf", size)
        img = font.render(text, True, text_col)
    
        if center:
            textRect = img.get_rect(center=(x, y))
            x, y = textRect.topleft

        screen.blit(img, (x,y))


    def volumeSliderUpdate(self):
        global volume
        if self.volumeSliderX < mousePos[0] < self.volumeSliderX+80 and 795 < mousePos[1] < 795+80 and mouseUp and mousePress[0]:
            self.volumeSliderClickedOn = True
        
        if self.volumeSliderClickedOn:
            self.volumeSliderX = mousePos[0]-40

        if self.volumeSliderX+40 < 570:
            self.volumeSliderX = 570-40
            
        if self.volumeSliderX+40 > 1120:
            self.volumeSliderX = 1120-40


        volume = ((self.volumeSliderX+40-570)/550)
        
        pygame.mixer.music.set_volume(volume)  

        if not (795< mousePos[1] < 795+80) or mousePress[0] == False:
            self.volumeSliderClickedOn = False

        screen.blit(self.volumeSlider, (self.volumeSliderX, 795))

    def update(self):
        global skinsApplied
        if self.currentScreen == "title":
            screen.blit(self.startImg, (0,0))
            self.playButton.update()
            self.shopButton.update()
            self.settingsButton.update()
            self.skinButton.update()

        elif self.currentScreen == "menu2":
            screen.blit(self.menuImg2, (0,0))   
            if 6 in ownedmaps:
                self.map6Select.update()
                self.map6Load.update()
            if 7 in ownedmaps:
                self.map7Select.update()
                self.map7Load.update()

            self.nextButton.update()
            #self.onlineButton.update()

        elif self.currentScreen == "menu":
            screen.blit(self.menuImg, (0,0))       
            self.map1Select.update()     
            self.map1Load.update()
            self.map2Select.update() 
            self.map2Load.update()
            self.map3Select.update()
            self.map3Load.update()   
            self.map4Select.update()
            self.map4Load.update()
            self.map5Select.update()
            self.map5Load.update()
            self.nextButton.update()
            self.backButton.update()  



        elif self.currentScreen == "settings":
            screen.blit(self.settingsMenu, (0,0))
            self.volumeSliderUpdate()
            self.settingsBackButton.update()
            self.toggleFullscreenButton.update()
        elif self.currentScreen == "onlineScreen":
            screen.blit(self.lobbyWait, (0,0))
            screen.blit(self.lobbyMappings[client.lobbySize], (700, 300))
            if client.isOnline == False:
                self.onlineBackButton.update()
            else:
                self.leaveLobby.update()
            if not client.isOnline:
                self.joinButton.update()

        elif self.currentScreen == "shop":
            screen.blit(self.shopImg, (0,0)) 
            self.settingsBackButton.update()
            screen.blit(self.cashImg, (945,115)) 
            self.draw_text(str(int(min(np.floor(cash*.01), 9999))), "BLACK", 820, 140, 100, True)
            if 6 not in ownedmaps:
                self.map6buy.update()
            if 7 not in ownedmaps:
                self.map7buy.update()
            self.casinoButton.update()

        elif menu.currentScreen == "casino":
            screen.blit(self.casinoImg, (0,0))
            self.casinoBack.update()
            if self.spin == True:
                self.clock.tick(60)
                menuLoot.update()
            else:
                menuLoot.smallDraw()
                self.spinButton.update()

        elif menu.currentScreen == "skins":
            screen.blit(self.skinSelectionImg, (0,0))
            self.settingsBackButton.update()
            audio.menuCat.set_volume(volume)
            self.menuCat.update()
            for index, key in enumerate(self.alternateImages.keys()):
                x = (index % 5) * 200 + 120
                y = 300 + (index//5) * 200
                if x < mousePos[0] < x+160 and y < mousePos[1] < y+160 and mousePress[0] and mouseUp == True:
                    self.indexer[key] += 1
                    if self.indexer[key] > len(self.alternateImages[key]):
                        self.indexer[key] = 0

                
                if self.indexer[key] ==0:
                    screen.blit(pygame.image.load(f"{prefix}ui/{key}.png"), (x, y))
                    skinsApplied[key] = 0
                elif self.alternateImages[key][self.indexer[key]-1] in ownedSkins:
                    screen.blit(pygame.image.load(f"{prefix}ui/{self.alternateImages[key][self.indexer[key]-1]}.png"), (x, y))
                    skinsApplied[key] = self.indexer[key]
                else:
                    screen.blit(pygame.image.load(f"{prefix}ui/locked.png"), (x, y))

        elif self.currentScreen == "gameSelected":
            screen.blit(self.gameSelectBackground, (100,100))
            screen.blit(pygame.image.load(f"{prefix}UI/map{self.mapDisplay}Select0.png"),(200,160))
            self.draw_text(str(self.nameLookup[self.mapDisplay]), "BLACK", 400, 200, 70)
            self.playInGameButton.update()
            self.back.update()
            screen.blit(self.normalMode, (450, 560))
            screen.blit(self.sandboxMode, (650, 560))
            screen.blit(self.moneyHealthMode, (850, 560))

            if self.selectedGamemode == "normal":
                pygame.draw.rect(screen, "GREEN", pygame.Rect(450, 560, 180, 180), 10)
            if self.selectedGamemode == "sandbox":
                pygame.draw.rect(screen, "GREEN", pygame.Rect(650, 560, 180, 180), 10)
            if self.selectedGamemode == "cashhealth":
                pygame.draw.rect(screen, "GREEN", pygame.Rect(850, 560, 180, 180), 10)

            if 450 < mousePos[0] < 630 and 560 < mousePos[1] < 740:
                pygame.draw.rect(screen, "YELLOW", pygame.Rect(450, 560, 180, 180), 10)
                if mousePress[0] and mouseUp:
                    self.selectedGamemode = "normal"
            if 650 < mousePos[0] < 830 and 560 < mousePos[1] < 740:
                pygame.draw.rect(screen, "YELLOW", pygame.Rect(650, 560, 180, 180), 10)
                if mousePress[0] and mouseUp:
                    self.selectedGamemode = "sandbox"
            if 850 < mousePos[0] < 1030 and 560 < mousePos[1] < 740:
                pygame.draw.rect(screen, "YELLOW", pygame.Rect(850, 560, 180, 180), 10)
                if mousePress[0] and mouseUp:
                    self.selectedGamemode = "cashhealth"

            if self.difficulty == 1:
                self.easyButton.update()
                self.draw_text("Easy", "BLACK", 500, 415, 70, True)
            elif self.difficulty == 2:
                self.mediumButton.update()
                self.draw_text("Medium", "BLACK", 500, 415, 70, True)
            elif self.difficulty == 3:
                self.hardButton.update()
                self.draw_text("Hard", "BLACK", 500, 415, 70, True)



class Audio:
    def __init__(self):
        self.lootBoxTick = pygame.mixer.Sound(f"{prefix}audio/lootBoxTick.wav")
        self.lootBoxDone = pygame.mixer.Sound(f"{prefix}audio/lootBoxDone.wav")
        self.menuCat = pygame.mixer.Sound(f"{prefix}audio/menuCat.wav")

audio = Audio()

class lootBoxes:
    def __init__(self):

        self.rarityLookup = {
            "Box1": "Legendary",
            "Calico1": "Common",
            "Calico2": "Common",
            "Calico3": "Rare",
            "Dumb1": "Common",
            "Fat1": "Common",
            "Fat2": "Common",
            "fishFarm1": "Common",
            "Gun1": "Common",
            "Gun2": "Rare",
            "Magic1": "Rare",
            "Tank1": "Common",


        }



        self.skins = {}
        for images in os.listdir(f"{prefix}loot"):
            self.skins[str(images)[:-4]] = pygame.transform.scale(pygame.image.load(f"{prefix}loot/{images}"), (160, 160))
        
        self.selectionSpeed = 15
        self.shuffleCount = 0
        self.shuffledSpot = random.randint(1,9)

        self.selectedRarity = "Common"

        self.blinkingEffect = 0

        self.shuffleKeys = list(self.skins.keys())
        random.shuffle(self.shuffleKeys)

        self.currentColor = (0,0,0)
        self.targetColor = (0,0,0)

        self.counter = 0

    def update(self):
        global ownedSkins
        self.draw()
        
        audio.lootBoxDone.set_volume(volume)
        audio.lootBoxTick.set_volume(volume)
        currentColorList = list(self.currentColor)

        for i in range(3): 
            currentColorList[i] = currentColorList[i] + (self.targetColor[i] - currentColorList[i]) * 0.25

        self.currentColor = tuple(currentColorList)

        self.selectionSpeed /= 1.01
        self.shuffleCount += self.selectionSpeed
        if self.shuffleCount > 5:
            self.shuffleCount = 0
            self.shuffledSpot = (self.shuffledSpot+1)%9
            audio.lootBoxTick.play()

        if self.selectionSpeed == 0:
            self.blinkingEffect += .1
            if self.blinkingEffect > 2:
                self.blinkingEffect = 0
                self.counter +=1

        elif self.selectionSpeed < 0.05:
            self.selectionSpeed = 0
            self.shuffleCount = 0
            audio.lootBoxDone.play()

        if self.counter > 5:
            ownedSkins.append(self.selected)
            ownedSkins = list(set(ownedSkins))
            self.reset()
            menu.spin = False

    def reset(self):
        self.selectionSpeed = 15
        self.shuffleCount = 0
        self.shuffledSpot = random.randint(1,9)
        self.selectedRarity = "Common"
        self.blinkingEffect = 0
        self.shuffleKeys = list(self.skins.keys())
        random.shuffle(self.shuffleKeys)
        self.currentColor = (0,0,0)
        self.targetColor = (0,0,0)
        self.counter = 0


    def spin(self):
        self.selectionSpeed = 15
        self.shuffleCount = 0
        self.shuffledSpot = random.randint(1,9)

        self.blinkingEffect = 0

        self.shuffleKeys = list(self.skins.keys())
        random.shuffle(self.shuffleKeys)

    def draw(self):
        if self.selectedRarity == "Common":
            self.targetColor = (55, 55, 245)
        elif self.selectedRarity == "Rare":
            self.targetColor =  (140, 50, 235)
        else:
            self.targetColor = (200, 160, 0)


        screen.fill(self.currentColor)

        pygame.draw.rect(screen, "BLACK", pygame.Rect(25, 25, 1150, 850))

        for index, key in enumerate(self.shuffleKeys[:9]):
            x = index % 3
            y = index // 3
            
            if index == self.shuffledSpot:
                fadedImg = self.skins[key]
                fadedImg.set_alpha(255)
                self.selectedRarity = self.rarityLookup[key]
                if self.blinkingEffect > 1:
                    fadedImg.set_alpha(50)
                screen.blit(fadedImg, (x*200 + 300, y*200 + 160))
                self.selected = key
            else:
                fadedImg = self.skins[key]
                fadedImg.set_alpha(50)
                screen.blit(fadedImg, (x * 200 + 300, y * 200 + 160))            

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.shuffledSpot%3 * 200 + 300, self.shuffledSpot//3 * 200 + 160, 160, 160), 10)

        self.selectedBox = (self.shuffledSpot%3, self.shuffledSpot//3)

    def smallDraw(self):
        for index, key in enumerate(self.shuffleKeys[:9]):
            x = index % 3
            y = index // 3
            fadedImg = self.skins[key]
            fadedImg.set_alpha(255)
            self.selectedRarity = self.rarityLookup[key]
            screen.blit(fadedImg, (x*200 + 500, y*200 + 160))


menuLoot = lootBoxes()



menu = Menu()

class OnlineClient:
    def __init__(self):
        self.identifier = str(uuid.uuid4())
        self.isOnline = False
        self.inGame = False
        self.host = False
        self.clientCooldown = 0
        self.selectedID = None
        self.lobbySize = 0
        self.upgradeQueue = []
        self.queue = []

    def convert_int64_to_int(self, data):
        if isinstance(data, dict):
            return {key: self.convert_int64_to_int(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_int64_to_int(item) for item in data]
        elif isinstance(data, np.int64):
            return int(data)  # Convert np.int64 to int
        return data

    async def writeUserData(self, userId, host, timeVal):
        if self.isOnline:
            await asyncio.to_thread(self._writeUserDataSync, userId, host, timeVal)
        else:
            print("Cannot write data: Client is offline.")

    def _writeUserDataSync(self, userId, host, timeVal):
        ref = db.reference(f'Lobby1/{userId}')
        ref.set({
            'host': host,
            'time': timeVal,
        })
        print(f'User data written successfully for {userId}.')

    async def removeAFK(self):
        await asyncio.to_thread(self._removeAFK)

    def _removeAFK(self):
        ref = db.reference('Lobby1') 
        data = ref.get()  
        if data:  
            for key, value in data.items():
                if isinstance(value, dict) and "time" in value and time.time() - value["time"] > 4:
                    ref.child(key).delete()        

    async def getGameStart(self):
        await asyncio.to_thread(self._getGameStart)

    def _getGameStart(self):
        global inGame
        game.newGame(1)
        inGame = True
        self.inGame = True
        print("start")

    async def testStartGame(self):
        await asyncio.to_thread(self._testStartGame)

    def _testStartGame(self):
        global inGame
        ref = db.reference('Lobby1') 
        data = ref.get()
        count = 0
        if data:
            for key, value in data.items():
                if isinstance(value, dict) and "time" in value:
                    count+=1
        if count == 2:
            ref.set({
            'inGame': True})
            self.inGame = True
            game.newGame(1)
            inGame = True
            print("start")

    async def getHost(self):
        await asyncio.to_thread(self._getHost)

    def _getHost(self):
        ref = db.reference(f'Lobby1')
        data = ref.get()
        host = True
        if data:  
            for key, value in data.items():
                if isinstance(value, dict) and "time" in value:
                    if value["host"] == True and key != self.identifier:
                        host = False
        self.host = host

    async def hostUpdate(self):
        await asyncio.to_thread(self._hostUpdate)
    
    def _hostUpdate(self):
        ref = db.reference(f'Lobby1/gamestateClient')
        data = ref.get()


        if data:
            updates = {}
            if data.get('queue'):
                updates['queue'] = ""
            if data.get('upgradeQueue'):
                updates['upgradeQueue'] = ""
            
            if updates:
                print("update")
                ref.update(updates)


            # Process the queue to add towers
            for towerData in data.get("queue", []):
                tower = towerEntity.fromDict(towerData)  # Create a tower from its data
                tower_cost = towerSelect.towerCosts[towerData["name"]]   # Retrieve the tower's cost
                
                if game.money >= tower_cost:
                    game.money -= tower_cost           # Deduct money for the tower
                    #game.towersOnMap.append(tower)           # Add the tower to the list
                else:
                    print(f"Welp Thats an Issue! : {towerData}")

            for upgradeData in data.get("upgradeQueue", []):
                tower_id = upgradeData.get("towerID")
            
                upgrade_type = upgradeData.get("type") 
                # Find the tower by its ID
                tower_to_upgrade = None
                for tower in game.towersOnMap:
                    print(str(tower.id), tower_id)
                    if str(tower.id) == tower_id:
                        tower_to_upgrade = tower
                        break

                if tower_to_upgrade:
                    
                    # Dynamically select the correct upgrade price dictionary based on tower type
                    upgradePrices = getattr(towerSelect, f"towerUpgradePrices{tower_to_upgrade.name}", {})
                    
                    if upgrade_type == "left" and tower_to_upgrade.leftUpgrade < 3:
                        # Get the cost for the left upgrade
                        left_cost = upgradePrices.get(f"{tower_to_upgrade.leftUpgrade + 1}-0", float('inf'))

                        # Check if the player has enough money for the upgrade
                        if game.money >= left_cost:
                            game.money -= left_cost  # Subtract the cost from the player's money
                            tower_to_upgrade.leftUpgrade += 1  # Apply the upgrade
                            print(f"Upgraded tower {tower_id} (left upgrade). Cost: {left_cost}")

                    elif upgrade_type == "right" and tower_to_upgrade.rightUpgrade < 3:
                        # Get the cost for the right upgrade
                        right_cost = upgradePrices.get(f"0-{tower_to_upgrade.rightUpgrade + 1}", float('inf'))

                        # Check if the player has enough money for the upgrade
                        if game.money >= right_cost:
                            game.money -= right_cost  # Subtract the cost from the player's money
                            tower_to_upgrade.rightUpgrade += 1  # Apply the upgrade
                            print(f"Upgraded tower {tower_id} (right upgrade). Cost: {right_cost}")
                        else:
                            print(f"Not enough money for right upgrade on tower {tower_id}. Required: {right_cost}, Available: {game.money}")
                    tower_to_upgrade.updateImage()


        ref = db.reference(f'Lobby1/gamestateHost')
        data = ref.get()

        data_to_send = {
            'money': game.money,
            'yarn': [yarn.toDict() for yarn in game.yarnList],
            'towers': [tower.toDict() for tower in game.towersOnMap]
        }
        data_to_send = self.convert_int64_to_int(data_to_send)
        ref.set(data_to_send)

    async def clientUpdate(self):
        await asyncio.to_thread(self._clientUpdate)

    def _clientUpdate(self):
        ref = db.reference(f'Lobby1/gamestateHost')
        data = ref.get()
        
        if not data:
            print("No data found in Lobby1")
            return
        
        game.yarnList = [yarn.fromDict(yarnData) for yarnData in data.get("yarn", [])]
        game.money = data.get("money", 0)
        game.towersOnMap = [towerEntity.fromDict(towerData) for towerData in data.get("towers", [])]

        ref = db.reference(f'Lobby1/gamestateClient')
        data_to_send = {
            'queue': [self.queue[-1].toDict()] if self.queue else [],
            'upgradeQueue': [self.upgradeQueue[-1]] if self.upgradeQueue else [],
        }
        data_to_send = self.convert_int64_to_int(data_to_send)

        ref.set(data_to_send)
        self.queue = []
        self.upgradeQueue = []

    async def getLobbySize(self):
        await asyncio.to_thread(self._getLobbySize)

    def _getLobbySize(self):
        ref = db.reference('Lobby1') 
        data = ref.get()
        count = 0
        if data:
            for key, value in data.items():
                if isinstance(value, dict) and "time" in value:
                    count+=1     
                    if time.time() - value["time"] > 4:
                        ref.child(key).delete()  
        self.lobbySize = count 
        
# Utility Functions
def readUserData(userId):
    ref = db.reference(f'Lobby1/{userId}')
    data = ref.get()
    if data:
        print(f"Data for {userId}: {data}")
        return data
    else:
        print(f'No data available for user: {userId}')
        return None

    
def removeUserData(userId):
    ref = db.reference(f'Lobby1/{userId}')
    ref.delete()  # Deletes the node for the specified user
    print(f'User {userId} removed from the database successfully.')

def removeAFK():
    ref = db.reference('Lobby1') 
    data = ref.get()  
    
    if data:  
        for key, value in data.items():
            if isinstance(value, dict) and "time" in value and time.time() - value["time"] > 4:
                ref.child(key).delete()      

def removeSelf():
    ref = db.reference('Lobby1') 
    data = ref.get()  
    
    if data:  
        for key, value in data.items():
            if key == client.identifier:
                ref.child(key).delete()  
client = OnlineClient()

# Async function for online updates
async def online_update(client):
    while True:
        await asyncio.sleep(.2)  # Update interval
        if menu:
            if menu.currentScreen == "onlineScreen":
                await client.getLobbySize()
            if client.isOnline:
                currentTime = time.time()
                print("Online data updated.")
                if client.inGame == True:
                    print("In Game")
                    if client.host:
                        print("Host")
                        await client.hostUpdate()
                    else:
                        print("Client")
                        await client.clientUpdate()
                else:
                    await client.removeAFK()
                    await client.writeUserData(client.identifier, client.host, currentTime)
                    await client.getHost()
                    if client.host:
                        await client.testStartGame()
                    else:
                        await client.getGameStart()

def start_async_loop(async_func, *args):
    asyncio.run(async_func(*args))

async_thread = Thread(target=start_async_loop, args=(online_update, client), daemon=True)
async_thread.start()


credits = pygame.image.load(f"{prefix}ui/Credits.png").convert_alpha()
'''
currentAlpha = 255
while currentAlpha > 0:
    currentAlpha -= 5
    if currentAlpha < 0:
        currentAlpha = 0
    credits.set_alpha(currentAlpha)
    screen.fill("BLACK")
    screen.blit(credits, (0,0))
    pygame.display.flip()
    time.sleep(0.1)
'''

# Main game manager class to handle game state and updates
class GameManager:

    roundNormal = [

[(1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32), (1, 1.32)],

[(1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08), (1, 1.08)],

[(1, 1.58), (1, 1.58), (1, 1.58), (1, 1.58), (1, 1.58), (1, 1.58), (1, 1.58), (1, 1.58), (1, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58), (2, 1.58)],

[(1, 1.3), (1, 1.3), (1, 1.3), (1, 1.3), (1, 1.3), (1, 1.3), (1, 1.3), (1, 1.3), (1, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3), (2, 1.3)],

[(1, 2.36), (1, 2.36), (1, 2.36), (1, 2.36), (1, 2.36), (2, 2.36), (2, 2.36), (2, 2.36), (2, 2.36), (2, 2.36), (2, 2.36), (2, 2.36), (3, 2.36), (3, 2.36), (3, 2.36), (3, 2.36), (3, 2.36), (3, 2.36), (3, 2.36)],

[(1, 1.9), (1, 1.9), (1, 1.9), (1, 1.9), (2, 1.9), (2, 1.9), (2, 1.9), (2, 1.9), (2, 1.9), (2, 1.9), (2, 1.9), (3, 1.9), (3, 1.9), (3, 1.9), (3, 1.9), (3, 1.9), (3, 1.9), (3, 1.9)],

[(1, 1.84), (1, 1.84), (1, 1.84), (2, 1.84), (2, 1.84), (2, 1.84), (2, 1.84), (2, 1.84), (2, 1.84), (2, 1.84), (3, 1.84), (3, 1.84), (3, 1.84), (3, 1.84), (3, 1.84), (3, 1.84), (3, 1.84), (3, 1.84), (3, 1.84)],

[(1, 1.6), (2, 1.6), (2, 1.6), (2, 1.6), (2, 1.6), (2, 1.6), (2, 1.6), (2, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6), (3, 1.6)],

[(2, 1.5), (2, 1.5), (2, 1.5), (2, 1.5), (2, 1.5), (2, 1.5), (2, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5), (3, 1.5)],

[(2, 2.12), (2, 2.12), (2, 2.12), (3, 2.12), (3, 2.12), (3, 2.12), (3, 2.12), (3, 2.12), (3, 2.12), (3, 2.12), (3, 2.12), (4, 2.12), (4, 2.12), (4, 2.12), (4, 2.12), (4, 2.12), (4, 2.12), (4, 2.12), (4, 2.12)],

[(3, 2.08), (3, 2.08), (3, 2.08), (3, 2.08), (3, 2.08), (3, 2.08), (3, 2.08), (3, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08), (4, 2.08)],

[(3, 2.92), (3, 2.92), (3, 2.92), (3, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (4, 2.92), (5, 2.92), (5, 2.92), (5, 2.92), (5, 2.92), (5, 2.92), (5, 2.92)],

[(3, 2.74), (3, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (4, 2.74), (5, 2.74), (5, 2.74), (5, 2.74), (5, 2.74), (5, 2.74), (5, 2.74), (5, 2.74), (5, 2.74)],

[(4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (4, 2.42), (5, 2.42), (5, 2.42), (5, 2.42), (5, 2.42), (5, 2.42), (5, 2.42), (5, 2.42), (5, 2.42), (5, 2.42)],

[(4, 2.04), (4, 2.04), (4, 2.04), (4, 2.04), (4, 2.04), (4, 2.04), (4, 2.04), (4, 2.04), (4, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04), (5, 2.04)],

[(4, 1.66), (4, 1.66), (4, 1.66), (4, 1.66), (4, 1.66), (4, 1.66), (4, 1.66), (4, 1.66), (4, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66), (5, 1.66)],

[(4, 1.42), (4, 1.42), (4, 1.42), (4, 1.42), (4, 1.42), (4, 1.42), (4, 1.42), (4, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42), (5, 1.42)],

[(4, 1.2), (4, 1.2), (4, 1.2), (4, 1.2), (4, 1.2), (4, 1.2), (4, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2), (5, 1.2)],

[(4, 1.02), (4, 1.02), (4, 1.02), (4, 1.02), (4, 1.02), (4, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02), (5, 1.02)],

[(4, 1.28), (4, 1.28), (4, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (5, 1.28), (6, 1.28), (6, 1.28), (6, 1.28)],

[(5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (5, 1.58), (6, 1.58), (6, 1.58), (6, 1.58), (6, 1.58), (6, 1.58), (6, 1.58), (6, 1.58), (6, 1.58)],

[(5, 1.68), (5, 1.68), (5, 1.68), (5, 1.68), (5, 1.68), (5, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68)],

[(5, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68), (6, 1.68)],

[(6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48), (6, 1.48)],

[(6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2), (6, 1.2)],

[(6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98), (6, 0.98)],

[(6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (6, 0.92), (7, 0.92), (7, 0.92), (7, 0.92)],

[(6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (6, 0.88), (7, 0.88), (7, 0.88), (7, 0.88), (7, 0.88), (7, 0.88), (7, 0.88)],

[(6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (6, 0.78), (7, 0.78), (7, 0.78), (7, 0.78), (7, 0.78), (7, 0.78), (7, 0.78), (7, 0.78), (7, 0.78)],

[(6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (6, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72), (7, 0.72)],

[(6, 0.58), (6, 0.58), (6, 0.58), (6, 0.58), (6, 0.58), (6, 0.58), (6, 0.58), (6, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58), (7, 0.58)],

[(6, 0.52), (6, 0.52), (6, 0.52), (6, 0.52), (6, 0.52), (6, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52), (7, 0.52)],

[(6, 0.46), (6, 0.46), (6, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46), (7, 0.46)],

[(7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44), (7, 0.44)],

[(7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36), (7, 0.36)],

[(7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28), (7, 0.28)],

[(7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24), (7, 0.24)],

[(7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18), (7, 0.18)],

[(7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16), (7, 0.16)],

[(7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (7, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18), (8, 1.18)],

[(8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8), (8, 1.8)],

[(8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46), (8, 1.46)],

[(8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2), (8, 1.2)],

[(8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96)],

[(8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78), (8, 0.78)],

[(8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64), (8, 0.64)],

[(8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (8, 0.86), (9, 0.86), (9, 0.86), (9, 0.86)],

[(8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (8, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98)],

[(8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (8, 0.96), (9, 0.96), (9, 0.96), (9, 0.96), (9, 0.96), (9, 0.96), (9, 0.96), (9, 0.96), (9, 0.96)],

[(8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (8, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92), (9, 0.92)],

[(8, 0.8), (8, 0.8), (8, 0.8), (8, 0.8), (8, 0.8), (8, 0.8), (8, 0.8), (8, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8), (9, 0.8)],

[(8, 0.72), (8, 0.72), (8, 0.72), (8, 0.72), (8, 0.72), (8, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72), (9, 0.72)],

[(8, 0.84), (8, 0.84), (8, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (9, 0.84), (10, 0.84)],

[(9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (9, 1.12), (10, 1.12), (10, 1.12), (10, 1.12), (10, 1.12)],

[(9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (9, 1.1), (10, 1.1), (10, 1.1), (10, 1.1), (10, 1.1), (10, 1.1), (10, 1.1)],

[(9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (9, 1.04), (10, 1.04), (10, 1.04), (10, 1.04), (10, 1.04), (10, 1.04), (10, 1.04), (10, 1.04), (10, 1.04)],

[(9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (9, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98), (10, 0.98)],

[(9, 0.9), (9, 0.9), (9, 0.9), (9, 0.9), (9, 0.9), (9, 0.9), (9, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9), (10, 0.9)],

[(9, 0.82), (9, 0.82), (9, 0.82), (9, 0.82), (9, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82), (10, 0.82)],

[(9, 1.16), (9, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (10, 1.16), (11, 1.16), (11, 1.16)],

[(10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (11, 1.46), (11, 1.46), (11, 1.46), (11, 1.46), (11, 1.46)],

[(10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (10, 1.46), (11, 1.46), (11, 1.46), (11, 1.46), (11, 1.46), (11, 1.46), (11, 1.46), (11, 1.46)],

[(10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (10, 1.38), (11, 1.38), (11, 1.38), (11, 1.38), (11, 1.38), (11, 1.38), (11, 1.38), (11, 1.38), (11, 1.38), (11, 1.38)],

[(10, 1.3), (10, 1.3), (10, 1.3), (10, 1.3), (10, 1.3), (10, 1.3), (10, 1.3), (10, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3), (11, 1.3)],

[(10, 1.2), (10, 1.2), (10, 1.2), (10, 1.2), (10, 1.2), (10, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2), (11, 1.2)],

[(10, 1.08), (10, 1.08), (10, 1.08), (10, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08), (11, 1.08)],

[(10, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02), (11, 1.02)],

[(11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9), (11, 0.9)],

[(11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74), (11, 0.74)],

[(11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6), (11, 0.6)],

[(11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48), (11, 0.48)],

[(11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4), (11, 0.4)],

[(11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32), (11, 0.32)],

[(12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88), (12, 1.88)],

[(12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52), (12, 1.52)],

[(12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24), (12, 1.24)],

[(12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0), (12, 1.0)],

[(12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82), (12, 0.82)],

[(12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66), (12, 0.66)],

[(12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54), (12, 0.54)],

[(12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44), (12, 0.44)],

[(12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36), (12, 0.36)],

[(12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28), (12, 0.28)],

[(12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24), (12, 0.24)],

[(12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2), (12, 0.2)],

[(12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16), (12, 0.16)],

[(12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12), (12, 0.12)],


]

    def __init__(self):
        # Set up the game clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Define surfaces for game content and UI
        self.gameWindow = pygame.Surface((900, 900), pygame.SRCALPHA)
        self.gameUIWindow = pygame.Surface((300, 900), pygame.SRCALPHA)
                
        self.gameSpeed =60

        self.towersMenuSelect = []

        self.gamemode = "normal"


        self.moneyIcon = pygame.image.load(f"{prefix}ui/fishMoney.png").convert_alpha()
        self.moneyIcon = pygame.transform.scale(self.moneyIcon, (80, 40))

        self.healthIcon = pygame.image.load(f"{prefix}ui/health.png").convert_alpha()
        self.healthIcon = pygame.transform.scale(self.healthIcon, (40, 40))

        self.costIcon = pygame.image.load(f"{prefix}ui/cost.png").convert_alpha()
        self.costIcon = pygame.transform.scale(self.costIcon, (40, 40))

        self.leaveButton = pygame.image.load(f"{prefix}ui/leaveButton.png").convert_alpha()
        self.leaveButton = pygame.transform.scale(self.leaveButton, (200, 100))

        self.menuButton = pygame.image.load(f"{prefix}ui/gameMenu.png").convert_alpha()
        self.menuButton = pygame.transform.scale(self.menuButton, (100, 100))

        self.playButton = pygame.image.load(f"{prefix}ui/playButton.png").convert_alpha()
        self.playButton = pygame.transform.scale(self.playButton, (100, 100))

        self.pauseButton = pygame.image.load(f"{prefix}ui/pauseButton.png").convert_alpha()
        self.pauseButton = pygame.transform.scale(self.pauseButton, (100, 100))

        self.twoxButton = pygame.image.load(f"{prefix}ui/2xButton.png").convert_alpha()
        self.twoxButton = pygame.transform.scale(self.twoxButton, (100, 100))

        self.saveButton = pygame.image.load(f"{prefix}ui/saveButton.png").convert_alpha()
        self.saveButton = pygame.transform.scale(self.saveButton, (100, 100))

        self.dieScreen = pygame.image.load(F"{prefix}ui/gameOver.png").convert_alpha()
        self.dieScreen = pygame.transform.scale(self.dieScreen, (450, 600))

        self.hover = None

    def saveGame(self):

        try:
            saveData = {
                'money': self.money,
                "difficulty": self.difficulty,
                'index': self.roundIndex,
                'health': self.health,
                'round': self.round,
                'gamemode': self.gamemode,
                'yarn': [yarn.toDict() for yarn in game.yarnList],
                'towers': [tower.toDict() for tower in game.towersOnMap]
    
            }


            with open(f"{prefix}saves/save{self.mapNum}.json", "w") as file:
                json.dump(saveData, file)

            self.loadGame(saveData ,self.mapNum)
        except Exception as e:
            print([yarn.toDict() for yarn in game.yarnList])
            print([tower.toDict() for tower in game.towersOnMap])
            print(e)

    def loadGame(self, data, map): 
        global pause
        if map == 1:
            self.track = [(0, 200, 600, 300), (500, 0, 600, 300), (300, 0, 600, 100), (300, 0, 400, 800), (100, 700, 400, 800), (100, 500, 200, 800), (100, 500, 800, 600), (700, 500, 800, 900)]
            self.mapCords = [(0,250), (550, 250), (550,50), (350, 50), (350, 750), (150, 750), (150, 550), (750, 550), (750, 900)]        

        if map == 2:
            self.track = [(100,0,200,900), (100,0,400,100), (300, 0, 400, 800), (300, 700, 800, 800), (700, 500, 800, 800), (500, 500, 800, 600), (500, 300, 600, 600), (500, 300, 800, 400), (700, 100, 800, 400), (500, 100, 800, 200), (500, 0, 600, 200), (400, 0, 500, 700), (500, 600, 700, 700), (500, 200, 700, 300)]
            self.mapCords = [(150, 1000), (150, 50), (350, 50), (350, 750), (750, 750), (750, 550), (550, 550), (550, 350), (750, 350), (750, 150), (550, 150), (550, -50)]            

        if map == 3:
            self.track = [(0,500, 200, 600), (100, 500, 200, 800), (100, 700, 400, 800), (300, 300, 400, 800), (100, 300, 400, 400), (100, 100, 200, 400), (100, 100, 800, 200), (700, 100, 800, 400), (500, 300, 800, 400), (500, 300, 600, 800), (500, 700, 800, 800), (700, 500, 800, 800), (700, 500, 900, 600)]
            self.mapCords = [(-100, 550), (150, 550), (150, 750), (350, 750), (350, 350), (150, 350), (150, 150), (750, 150), (750, 350), (550, 350), (550, 750), (750, 750), (750, 550), (950, 550)]

        if map == 4:
            radius = 340 
            self.track = [(0, 0, 180, 900), (720, 0, 900, 900), (0, 0, 900, 180), (0, 720, 900, 900),]
            for i in range(50):
                theta = (2 * np.pi / 50) * i
                
                x1 = int(450 + radius * np.cos(theta) - 100 / 2)
                y1 = int(450 + radius * np.sin(theta) - 100 / 2)
                
                x2 = x1 + 100
                y2 = y1 + 100
                self.track.append((x1, y1, x2, y2))

            self.mapCords = [(-100, 350), (150, 350), (150, 250), (250, 250), (250, 150), (650, 150), (650, 250), (750, 250), (750, 650), (650, 650), (650, 750), (250, 750), (250, 650), (150, 650), (150, 550), (-50,  550)]

        if map == 5:
            self.track = [(0,0,50,900), (50, 170, 112,360), (50, 770, 390, 900), (250, 0, 330, 130), (310, 220, 610, 330), (250, 340, 350, 600), (260, 550, 900, 630), (510, 0, 900, 100), (800, 0, 900, 900), (270, 635, 380, 777), (530, 280, 800, 550), (570, 850, 900, 900)]
            self.makeCircle(90, 450, 450, 20, 40)
            self.makeCircle(90, 160, 450, 20, 40)
            self.makeCircle(90, 205, 240, 20, 40)
            self.makeCircle(90, 450, 130, 20, 40)
            self.makeCircle(90, 120, 80, 20, 40)
            self.makeCircle(90, 700, 180, 20, 40)
            self.makeCircle(90, 180, 680, 20, 40)
            self.makeCircle(90, 710, 740, 20, 40)
            self.makeCircle(90, 480, 800, 20, 40)

            self.mapCords = [(-100, 350),(350, 350), (350, 250), (550, 250), (550, 350), (850, 350), (850, 550), (550, 550), (550, 650), (350, 650), (350, 550), (-50, 550)]

        if map == 6:
            self.track = [(0, 400, 900, 500), (70, 650, 200, 770), (50, 800, 200, 870)]
            self.mapCords = [(-100, 350), (950, 450)]  
 
        if map == 7:
            self.track = [(300,0,400,900), (500,0,600,900), (0,300,900,400), (0,500,900,600)]
            self.mapCords = [[(-100, 350), (950, 350)], [(-30, 550), (950, 550)], [(550, -30), (550, 950)], [(350, -30), (350, 950)]]    



        self.mapNum = map
        self.map = pygame.image.load(f"{prefix}maps/map{map}.png").convert_alpha()
        self.map = pygame.transform.scale(self.map, (900, 900))


        pause = False
        self.gameSpeed = 60

        self.textTime = 0

        self.displayPrice = None

        # Allows for tower upgrades
        self.selectedTower = None

        # Initialize lists to hold towers on the map and tower selection options and contains yarn
        self.towersOnMap = []
        self.yarnList = []
        self.projectileList = []
        self.effectList = []
        self.entityList = []
        self.yarnDeleteList = []
        self.towersOnMapToRemove = []
        # Track selected tower type and mouse interactions
        self.selected = None
        self.mousePos = [0, 0]
        self.mousePress = [0, 0, 0]


        self.inGameMenu = False
        

        # Initializes Health and Money and Round
        game.roundIndex = data.get("index")
        game.health = data.get("health")
        self.round = data.get("round")
        game.money = data.get("money")
        game.difficulty = data.get("difficulty")
        game.gamemode = data.get("gamemode")

        game.yarnList = [yarn.fromDict(yarnData) for yarnData in data.get("yarn", [])]
        game.towersOnMap = [towerEntity.fromDict(towerData) for towerData in data.get("towers", [])]


        self.roundTime = 1

        # Initializes Music into the Game
        pygame.mixer.music.load(f"{prefix}music/map{map}.mp3")
        pygame.mixer.music.play(-1)  # Play indefinitely


        self.towersMenuSelect = []
        # Create a tower selection button in the UI
        for tower, position in zip(
            ["Calico", "Tank", "Fat", "Magic", "fishFarm", "Gun", "Box", "Dumb"],
            [(30, 30), (170, 30), (30, 170), (170, 170), (30, 310), (170, 310), (30, 450), (170, 450)],
        ):
            if tower in skinsApplied and skinsApplied[tower] != 0:
                towerSelect(*position, tower+str(skinsApplied[tower]))
            else:
                towerSelect(*position, tower)




    def makeCircle(self, radius, x, y, amount, size):
        for i in range(amount):
            theta = (2 * np.pi / amount) * i
            
            x1 = int(x + radius * np.cos(theta) - size / 2)
            y1 = int(y + radius * np.sin(theta) - size / 2)
            
            x2 = x1 + size
            y2 = y1 + size
            self.track.append((x1, y1, x2, y2))

    def newGame(self, map, gamemode):
        global pause
        if map == 1:
            self.track = [(0, 200, 600, 300), (500, 0, 600, 300), (300, 0, 600, 100), (300, 0, 400, 800), (100, 700, 400, 800), (100, 500, 200, 800), (100, 500, 800, 600), (700, 500, 800, 900)]
            self.mapCords = [(0,250), (550, 250), (550,50), (350, 50), (350, 750), (150, 750), (150, 550), (750, 550), (750, 900)]        

        if map == 2:
            self.track = [(100,0,200,900), (100,0,400,100), (300, 0, 400, 800), (300, 700, 800, 800), (700, 500, 800, 800), (500, 500, 800, 600), (500, 300, 600, 600), (500, 300, 800, 400), (700, 100, 800, 400), (500, 100, 800, 200), (500, 0, 600, 200), (400, 0, 500, 700), (500, 600, 700, 700), (500, 200, 700, 300)]
            self.mapCords = [(150, 1000), (150, 50), (350, 50), (350, 750), (750, 750), (750, 550), (550, 550), (550, 350), (750, 350), (750, 150), (550, 150), (550, -50)]            

        if map == 3:
            self.track = [(0,500, 200, 600), (100, 500, 200, 800), (100, 700, 400, 800), (300, 300, 400, 800), (100, 300, 400, 400), (100, 100, 200, 400), (100, 100, 800, 200), (700, 100, 800, 400), (500, 300, 800, 400), (500, 300, 600, 800), (500, 700, 800, 800), (700, 500, 800, 800), (700, 500, 900, 600)]
            self.mapCords = [(-100, 550), (150, 550), (150, 750), (350, 750), (350, 350), (150, 350), (150, 150), (750, 150), (750, 350), (550, 350), (550, 750), (750, 750), (750, 550), (950, 550)]

        if map == 4:
            radius = 340 
            self.track = [(0, 0, 180, 900), (720, 0, 900, 900), (0, 0, 900, 180), (0, 720, 900, 900),]
            for i in range(50):
                theta = (2 * np.pi / 50) * i
                
                x1 = int(450 + radius * np.cos(theta) - 100 / 2)
                y1 = int(450 + radius * np.sin(theta) - 100 / 2)
                
                x2 = x1 + 100
                y2 = y1 + 100
                self.track.append((x1, y1, x2, y2))

            self.mapCords = [(-100, 350), (150, 350), (150, 250), (250, 250), (250, 150), (650, 150), (650, 250), (750, 250), (750, 650), (650, 650), (650, 750), (250, 750), (250, 650), (150, 650), (150, 550), (-50,  550)]

        if map == 5:
            self.track = [(0,0,50,900), (50, 170, 112,360), (50, 770, 390, 900), (250, 0, 330, 130), (310, 220, 610, 330), (250, 340, 350, 600), (260, 550, 900, 630), (510, 0, 900, 100), (800, 0, 900, 900), (270, 635, 380, 777), (530, 280, 800, 550), (570, 850, 900, 900)]
            self.makeCircle(90, 450, 450, 20, 40)
            self.makeCircle(90, 160, 450, 20, 40)
            self.makeCircle(90, 205, 240, 20, 40)
            self.makeCircle(90, 450, 130, 20, 40)
            self.makeCircle(90, 120, 80, 20, 40)
            self.makeCircle(90, 700, 180, 20, 40)
            self.makeCircle(90, 180, 680, 20, 40)
            self.makeCircle(90, 710, 740, 20, 40)
            self.makeCircle(90, 480, 800, 20, 40)

            self.mapCords = [(-100, 350),(350, 350), (350, 250), (550, 250), (550, 350), (850, 350), (850, 550), (550, 550), (550, 650), (350, 650), (350, 550), (-50, 550)]


        if map == 6:
            self.track = [(0, 400, 900, 500), (70, 650, 200, 770), (50, 800, 200, 870)]
            self.mapCords = [(-100, 350), (950, 450)]    

        if map == 7:
            self.track = [(300,0,400,900), (500,0,600,900), (0,300,900,400), (0,500,900,600)]
            self.mapCords = [[(-100, 350), (950, 350)], [(-30, 550), (950, 550)], [(550, -30), (550, 950)], [(350, -30), (350, 950)]]    
        self.mapNum = map
        self.map = pygame.image.load(f"{prefix}maps/map{map}.png").convert_alpha()
        self.map = pygame.transform.scale(self.map, (900, 900))

        self.gamemode = gamemode

        self.textTime = 0

        self.displayPrice = None

        # Allows for tower upgrades
        self.selectedTower = None

        # Initialize lists to hold towers on the map and tower selection options and contains yarn
        self.towersOnMap = []
        self.yarnList = []
        self.projectileList = []
        self.effectList = []
        self.entityList = []
        self.yarnDeleteList = []
        self.towersOnMapToRemove = []
        # Track selected tower type and mouse interactions
        self.selected = None
        self.mousePos = [0, 0]
        self.mousePress = [0, 0, 0]

        self.difficulty = menu.difficulty

        self.inGameMenu = False
        
        pause = False
        self.gameSpeed = 60


        # Initializes Health and Money and Round
        self.health = 100
        self.money = 100
        self.round = 0
        self.roundIndex = 0


        self.roundTime = 1

        # Initializes Music into the Game
        pygame.mixer.music.load(f"{prefix}music/map{map}.mp3")
        pygame.mixer.music.play(-1)  # Play indefinitely



        self.towersMenuSelect = []
        # Create a tower selection button in the UI
        for tower, position in zip(
            ["Calico", "Tank", "Fat", "Magic", "fishFarm", "Gun", "Box", "Dumb"],
            [(30, 30), (170, 30), (30, 170), (170, 170), (30, 310), (170, 310), (30, 450), (170, 450)],
        ):
            if tower in skinsApplied and skinsApplied[tower] != 0:
                towerSelect(*position, tower+str(skinsApplied[tower]))
            else:
                towerSelect(*position, tower)


    # Allows for drawing the text onto game window
    def draw_text(self, text, text_col, x, y, window, size=100, center = False):
        font = pygame.font.Font(f"{prefix}ui/8bitOperatorPlus-Regular.ttf", size)
        img = font.render(text, True, text_col)
    
        if center:
            textRect = img.get_rect(center=(x, y))
            x, y = textRect.topleft

        window.blit(img, (x,y))

    
    def onlineUpdate(self, mousePos, mousePress):
        self.clock.tick(60)
        self.place = True
        self.mousePos = mousePos
        self.mousePress = mousePress
        self.gameWindow.fill("White")
        self.gameWindow.blit(self.map, (0, 0))


        if client.host == False:
            for tow in game.towersOnMap:
                if str(tow.id) == str(client.selectedID):
                    game.selectedTower = tow


        if client.host:
            # Round Update
            self.roundTime -= (1/60)
            if self.roundTime <= 0:
                # Check if there are yarns left in the current round
                if self.roundIndex < len(GameManager.roundNormal[self.round]):
                    # Spawn the next yarn in the round
                    yarn(-100, 300, GameManager.roundNormal[self.round][self.roundIndex][0])
                    self.roundTime = GameManager.roundNormal[self.round][self.roundIndex][1]
                    self.roundIndex += 1
                # If all yarns in the current round are spawned, check if the field is clear
                elif len(self.yarnList) == 0:
                    self.roundIndex = 0
                    self.round += 1
                    self.money+= 75
                    self.roundTime = 2
                    self.textTime = 60  # Reset text time for the new round

        for yarnBalls in self.yarnList:
            yarnBalls.update()
        
        if client.host == True:
            for yarnBalls in self.yarnDeleteList:
                self.yarnList.remove(yarnBalls)
        else:
            client.clientCooldown+=1



        self.yarnDeleteList = []


        # Update each tower on the map
        for tower in self.towersOnMap:
            tower.update()

        # Updates Projectiles
        for item in self.projectileList:
            item.update()

        for item in self.entityList:
            item.update()

        # List of tower coordinates to check placement distance
        cords = [(tower.x, tower.y) for tower in self.towersOnMap]

        # Check if the mouse is within the "track" area
        for x_start, y_start, x_end, y_end in self.track:
            if x_start-40 <= mousePos[0] - 300 <= x_end+40 and y_start-40 <= mousePos[1] <= y_end+40:
                self.place = False  # Prevent placement if on track

        # Additional check for tower spacing
        for cord in cords:
            if calDistance(mousePos[0]-340, cord[0], mousePos[1] - 40, cord[1]) < 60:
            #(((mousePos[0] - 340) - cord[0])**2 + ((mousePos[1] - 40) - cord[1])**2) < 60:
                self.place = False
        
        if mousePos[0]-300 < 0:
            self.place = False

        if self.selected != None:
            if client.host == True:
                if towerSelect.towerCosts[self.selected] > self.money:
                    self.place = False
            else:
                if client.clientCooldown > 60:
                    if towerSelect.towerCosts[self.selected] > self.money:
                        self.place = False   
                        client.clientCooldown = 0

        # Place tower if all conditions are met
        if mousePress[0] and self.selected is not None and mouseUp and self.place:
            client.queue.append(towerEntity(mousePos[0] - 340, mousePos[1] - 40, self.selected))
            self.money -= towerSelect.towerCosts[self.selected]



        self.gameUIUpdate()
        self.draw()

    

    def gameUpdate(self, mousePos, mousePress):
        self.clock.tick(self.gameSpeed)
        self.place = True  # Assume placement is allowed initially
        self.mousePos = mousePos
        self.mousePress = mousePress
        self.hover = None

        if self.gamemode == "cashhealth":
            self.health = self.money

        moneyMod = 1
        if self.difficulty == 3:
            moneyMod = 1.5


        if self.gamemode == "sandbox":
            self.money = 100000

        for tower in self.towersOnMapToRemove:
            self.towersOnMap.remove(tower)

        self.towersOnMapToRemove = []

        # Clear the game window and redraw the map
        self.gameWindow.fill("White")
        self.gameWindow.blit(self.map, (0, 0))

        if self.health < 1:
            self.gameUIUpdate()
            self.gameWindow.blit(self.dieScreen, (225, 150))
            self.draw_text(str(self.round), "BLACK", 450, 625, self.gameWindow, 100, True)
            screen.blit(self.gameWindow, (300, 0))
            screen.blit(self.gameUIWindow, (0,0))
            pygame.display.flip()
            self.selected = None
            self.selectedTower = None
            return

        # Round Update
        self.roundTime -= (1/60)
        if self.roundTime <= 0:
            # Check if there are yarns left in the current round
            if self.roundIndex < len(GameManager.roundNormal[self.round]):
                # Spawn the next yarn in the round
                yarn(self.mapCords[0][0], self.mapCords[0][1], GameManager.roundNormal[self.round][self.roundIndex][0])
                self.roundTime = GameManager.roundNormal[self.round][self.roundIndex][1]
                self.roundIndex += 1
            # If all yarns in the current round are spawned, check if the field is clear
            elif len(self.yarnList) == 0:
                self.roundIndex = 0
                self.round += 1
                self.money+= 100
                self.roundStartMoney = self.money
                self.roundTime = 2
                self.textTime = 60  # Reset text time for the new round
            

        # Updates Yarn
        for yarnBalls in self.yarnList:
            yarnBalls.update()
        
        for yarnBalls in self.yarnDeleteList:
            try:
                self.yarnList.remove(yarnBalls)
            except Exception as e:
                print(e)    
        self.yarnDeleteList = []

        # Update each tower on the map
        for tower in self.towersOnMap:
            tower.update()

        # Updates Projectiles
        for item in self.projectileList:
            item.update()

        for item in self.entityList:
            item.update()

        # List of tower coordinates to check placement distance
        cords = [(tower.x, tower.y) for tower in self.towersOnMap]

        # Check if the mouse is within the "track" area
        for x_start, y_start, x_end, y_end in self.track:
            if x_start-40 <= mousePos[0] - 300 <= x_end+40 and y_start-40 <= mousePos[1] <= y_end+40:
                self.place = False  # Prevent placement if on track

        # Additional check for tower spacing
        for cord in cords:
            if calDistance(mousePos[0]-340, cord[0], mousePos[1] - 40, cord[1]) < 60:
                self.place = False
        
        if mousePos[0]-300 < 0:
            self.place = False




        if self.selected != None:
            if towerSelect.towerCosts[re.sub(r'\d+', '', self.selected)]*moneyMod > self.money:
                self.place = False


        # Place tower if all conditions are met
        if mousePress[0] and self.selected is not None and mouseUp and self.place:
            towerEntity(mousePos[0] - 340, mousePos[1] - 40, self.selected)
            self.money -= towerSelect.towerCosts[re.sub(r'\d+', '', self.selected)]*moneyMod

        # Update UI and draw
        self.gameUIUpdate()
        self.draw()



    # Update the user interface
    def gameUIUpdate(self):
        global inGame, pause
        # Fill the UI window with a background color
        self.gameUIWindow.fill((194, 133, 105))

        moneyMod = 1
        if self.difficulty == 3:
            moneyMod = 1.5

        if self.selected:
            self.displayPrice = str(round(towerSelect.towerCosts[re.sub(r'\d+', '', self.selected)] *moneyMod))
        
        if self.displayPrice:
            pygame.draw.rect(self.gameUIWindow, (115, 62, 57), pygame.Rect(0, 700, 300, 300))
            self.gameUIWindow.blit(self.costIcon, (240,710))
            self.draw_text(self.displayPrice, "BLACK", 100, 730, self.gameUIWindow, 50, True)

        else:
            pygame.draw.rect(self.gameUIWindow, (115, 62, 57), pygame.Rect(0, 750, 300, 300))

        if self.selected == None:
            self.displayPrice = None

        if game.gamemode != "cashhealth":
            self.gameUIWindow.blit(self.healthIcon, (240,780))
            self.gameUIWindow.blit(self.moneyIcon, (200,850))
        else:
            self.gameUIWindow.blit(self.moneyIcon, (200,810))


        if self.inGameMenu:
            if 50 < mousePos[0] < 250 and 450<mousePos[1]<550:
                self.gameUIWindow.blit(pygame.transform.scale(self.leaveButton, (220, 110)), (40, 445))
                if mousePress[0] and mouseUp:
                    inGame = False
                    pygame.mixer_music.stop()

            else:                                             
                self.gameUIWindow.blit(self.leaveButton, (50, 450))

            if self.health > 0:
                if 30 < mousePos[0] < 130 and 310<mousePos[1]<410:
                    self.gameUIWindow.blit(pygame.transform.scale(self.saveButton, (110, 110)), (25, 305))
                    if mousePress[0] and mouseUp:
                        self.saveGame()
                else:                                             
                    self.gameUIWindow.blit(self.saveButton, (30, 310))

            
            


        else:
            # Draw each tower selection button in the menu
            for tower in self.towersMenuSelect:
                tower.draw(self.mousePos, self.mousePress)

        if 30 < mousePos[0] < 130 and 590<mousePos[1]<690:
            self.gameUIWindow.blit(pygame.transform.scale_by(self.menuButton, 1.1), (25, 585))
            if mousePress[0] and mouseUp:
                self.inGameMenu = not self.inGameMenu
        else:
            self.gameUIWindow.blit(self.menuButton, (30, 590))


        if pause == True:
            tempButton = self.playButton
        elif self.gameSpeed == 120:
            tempButton = self.pauseButton
        else:
            tempButton = self.twoxButton

        if 170 < mousePos[0] < 270 and 590<mousePos[1]<690:
            self.gameUIWindow.blit(pygame.transform.scale_by(tempButton, 1.1), (165, 585))
            if mousePress[0] and mouseUp:
                if pause:
                   pause = False
                   self.gameSpeed = 60
                elif self.gameSpeed == 60:
                    self.gameSpeed = 120
                else:
                    pause = True
        else:
            self.gameUIWindow.blit(tempButton, (170, 590))

            
        if game.gamemode != "cashhealth":
            self.draw_text(str(int(self.money)), "BLACK", 100, 870, self.gameUIWindow, 50, True)
            self.draw_text(str(self.health), "BLACK", 100, 800, self.gameUIWindow, 50, True)
        else:
            self.draw_text(str(int(self.money)), "BLACK", 100, 830, self.gameUIWindow, 50, True)


    def broadcastRound(self):
        self.textTime -= .5
        self.draw_text(f"Round {str(self.round+1)}", "BLACK", 100, 400, self.gameWindow, 150)


    # Render all game and UI elements to the screen
    def draw(self):
        # Draw each tower on the game window
        for tower in self.towersOnMap:
            tower.draw()
        

        #for x_start, y_start, x_end, y_end in self.track:
            #pygame.draw.rect(self.gameWindow, ("PURPLE"), pygame.Rect(x_start, y_start, x_end - x_start, y_end - y_start))



        for item in self.entityList:
            item.draw()  

        # Draws the yarn
        for yarnBalls in self.yarnList:
            yarnBalls.draw()

        # Draws the projectiles
        for item in self.projectileList:
            item.draw()

        # Draws the effects on map
        for item in self.effectList:
            item.draw()

        # Draws tower on mouse
        if self.selected != None: 
            towerToDraw = pygame.image.load(f"{prefix}towers/{self.selected}/0-0.png").convert_alpha()
            towerToDraw = pygame.transform.scale(towerToDraw, (100, 100))  
            if self.place == False:
                towerToDraw = pygame.transform.grayscale(towerToDraw)  
            self.gameWindow.blit(towerToDraw, (mousePos[0] - 350, mousePos[1]-50))

        #Builds Menu Bar
        if self.selectedTower != None:
            if self.selectedTower.y > 600:
                self.vertOffset = 0
            else:
                self.vertOffset = 700
        if self.selectedTower != None:
            pygame.draw.rect(self.gameWindow, (194, 133, 105), (0, self.vertOffset, 900, 200))
            if client.isOnline == False:
                self.selectedTower.handleUpgrades()
            else:
                self.selectedTower.handleUpgradesOnline()

        if self.textTime > 0:
            self.broadcastRound()


        # Render game and UI windows onto the main display
        screen.blit(self.gameWindow, (300, 0))
        screen.blit(self.gameUIWindow, (0, 0))
        if self.hover:
            if mousePos[1] < 600:
                textSurface = pygame.font.Font(f"{prefix}ui/8bitOperatorPlus-Regular.ttf", 20).render(str(self.hover), True, "BLACK")
                textWidth = textSurface.get_size()[0]

                padding = 15

                tooltipWidth = max(200, textWidth + 2 * padding)
                tempScreen = pygame.Surface((tooltipWidth, 100))
                pygame.draw.rect(tempScreen, "GREY", pygame.Rect(0, 0, tooltipWidth, 100))
                pygame.draw.rect(tempScreen, "BLACK", pygame.Rect(0, 0, tooltipWidth, 100), 10)

                tempScreen.set_alpha(200)

                # Adjust position if tooltip goes off the screen to the right
                xPos = mousePos[0] if mousePos[0] + tooltipWidth <= 1200 else mousePos[0] - tooltipWidth

                screen.blit(tempScreen, (xPos, mousePos[1]))

                self.draw_text(
                    self.hover, "BLACK", xPos + tooltipWidth // 2, mousePos[1] + 100 // 2, screen, 20, center=True
                )
            else:
                textSurface = pygame.font.Font(f"{prefix}ui/8bitOperatorPlus-Regular.ttf", 20).render(str(self.hover), True, "BLACK")
                textWidth = textSurface.get_size()[0]

                padding = 15

                tooltipWidth = max(200, textWidth + 2 * padding)
                tempScreen = pygame.Surface((tooltipWidth, 100))
                pygame.draw.rect(tempScreen, "GREY", pygame.Rect(0, 0, tooltipWidth, 100))
                pygame.draw.rect(tempScreen, "BLACK", pygame.Rect(0, 0, tooltipWidth, 100), 10)

                tempScreen.set_alpha(200)

                # Adjust position if tooltip goes off the screen to the right
                xPos = mousePos[0] if mousePos[0] + tooltipWidth <= 1200 else mousePos[0] - tooltipWidth

                screen.blit(tempScreen, (xPos, mousePos[1] - 100))

                self.draw_text(
                    self.hover, "BLACK", xPos + tooltipWidth // 2, (mousePos[1] + 100 // 2) - 100, screen, 20, center=True
                )

        # Update the display to show all drawn elements
        pygame.display.flip()

# Instantiate the game manager
game = GameManager()


# Calculates distance
def calDistance(x1, x2, y1, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

# Creates class for track obsticles
# Class representing obstacles or effects that interact with the game world
class entity:

    _idCounter = 0


    # Lookup table for entity sizes based on their type
    sizeLookup = {
        "Potion": (30, 30),         # Size of "Potion" entities
        "otherPotion": (30, 30),     # Size of "otherPotion" entities
        "2otherPotion": (30, 30),     # Size of "otherPotion" entities

        "lightning"  : (10, 10), # Non Needed
        "superLightning": (10,10),
        "money" : (30,30),
        "money0" : (30,30),
        "money1" : (30,30),
        "money2" : (30,30)

    }

    # Mapping for sprite changes based on the entity type and variation
    spriteChange = {
        "Potion1": "slime0",        # Maps Potion1 to slime0 sprite
        "Potion2": "slime1",        # Maps Potion2 to slime1 sprite
        "Potion3": "slime2",        # Maps Potion3 to slime2 sprite

        "otherPotion1": "otherSlime0", # Maps otherPotion1 to otherSlime0 sprite
        "otherPotion2": "otherSlime1", # Maps otherPotion2 to otherSlime1 sprite
        "otherPotion3": "otherSlime2",  # Maps otherPotion3 to otherSlime2 sprite


        "2otherPotion1": "2otherSlime0", # Maps otherPotion1 to otherSlime0 sprite
        "2otherPotion2": "2otherSlime1", # Maps otherPotion2 to otherSlime1 sprite
        "2otherPotion3": "2otherSlime2"  # Maps otherPotion3 to otherSlime2 sprite


    }


    # Initializes the entity with position, target, attributes, and behavior
    def __init__(self, x, y, target, special, damage, life, rubberDamage):
        # Position of the entity with an offset
        self.x = x + 20
        self.y = y + 20

        self.id = entity._idCounter
        entity._idCounter += 1

        # Size determined by the special type
        self.size = entity.sizeLookup[special]
        # Image for the entity based on its type, scaled appropriately
        self.image = pygame.transform.scale(
            pygame.image.load(f"{prefix}effects/{special}.png").convert_alpha(),
            entity.sizeLookup[special]
        )
        # State to track if the entity has impacted its target
        self.impact = False
        # Target coordinates where the entity is heading
        self.target = target
        # Lifespan of the entity (frames or ticks)
        self.life = life
        # Special type (e.g., "Potion", "otherPotion")
        self.special = special
        # Damage dealt to rubber-type objects
        self.rubberDamage = rubberDamage
        # General damage dealt by the entity
        self.damage = damage
        # Add this entity to the global list of entities
        game.entityList.append(self)

        # Sets up list for lightning
        self.cords = []

        self.target = (target[0] if target[0]<900 else 900, target[1] if target[1]<900 else 900)

        self.target = (target[0] if target[0]>0 else 0, target[1] if target[1]>0 else 0)

        if self.special == "lightning" or self.special == "superLightning":
            self.target = 10


    # Updates the entity's position, state, and interactions
    def update(self):
        if self.special == "money" or self.special == "money0" or self.special == "money1" or self.special == "money2":
            if self.life < 0:
                try:
                    game.entityList.remove(self)
                except:
                    return                
                return        
            self.life -= 1

            self.x += (self.target[0] - self.x) * 0.1
            self.y += (self.target[1] - self.y) * 0.1

            if calDistance(self.x, mousePos[0]-300, self.y, mousePos[1]) < 20:
                game.money+=self.damage
                try:
                    game.entityList.remove(self)
                except:
                    return
                return
            
  

        if self.special == "Potion" or self.special == "otherPotion" or self.special == "2otherPotion":
            # Remove the entity if its lifespan has ended
            if self.life < 0:
                try:
                    game.entityList.remove(self)
                except:
                    return


            
            # Move the entity towards its target using linear interpolation
            self.x += (self.target[0] - self.x) * 0.1
            self.y += (self.target[1] - self.y) * 0.1

            # Check if the entity is close enough to its target to impact
            if abs(self.target[0] - self.x) < 10 and abs(self.target[1] - self.y) < 10 and not self.impact:
                self.impact = True
                # Snap the entity's position to the target
                self.x, self.y = self.target
                # Change size and sprite to indicate the impact effect
                self.size = (80, 80)
                self.image = pygame.transform.rotate(
                    pygame.transform.scale(
                        pygame.image.load(
                            f"{prefix}effects/{entity.spriteChange[self.special + str(random.randint(1, 3))]}.png"
                        ).convert_alpha(),
                        self.size
                    ),
                    180 * random.randint(1, 2) # Random rotation for visual variety
                )

            # Reduce lifespan after impact
            if self.impact:
                self.life -= 1

            # List to hold balloons (yarn balls) that will take damage
            damageBalloons = []

            if self.life > 0 and self.impact:
                # Check for collisions with yarn balls
                for yarnBalls in game.yarnList:
                    if calDistance(yarnBalls.x, self.x, yarnBalls.y, self.y) < 20: # If within range
                        damageBalloons.append(yarnBalls)


            # Apply damage to the affected yarn balls
            for yarnBalls in damageBalloons:
                yarnBalls.damageYarn(self.damage, self.rubberDamage, self)

        
        elif self.special == "lightning" or self.special == "superLightning":
            if self.target == 10:
                self.x+=25
                self.y+=25
                toDamage = []
                visited_targets = set()  # To track which yarns have already been struck
                current_x, current_y = self.x, self.y

                for _ in range(self.life):  # Number of strikes allowed
                    closest_yarn = None
                    min_distance = float('inf')  # Start with a very large distance
                    
                    # Find the closest yarn manually
                    for yarn in game.yarnList:
                        if yarn not in visited_targets:
                            distance = calDistance(current_x, yarn.x, current_y, yarn.y)
                            if distance < min_distance:
                                min_distance = distance
                                closest_yarn = yarn
                    
                    if closest_yarn is None:  # Break if no more valid targets
                        break
                    
                    # Add it to the toDamage list and mark it as visited
                    toDamage.append(closest_yarn)
                    visited_targets.add(closest_yarn)

                    # Add the lightning path to cords and update current position
                    self.cords.append((current_x, current_y, closest_yarn.x, closest_yarn.y))
                    current_x, current_y = closest_yarn.x, closest_yarn.y

                for z in toDamage:
                    z.damageYarn(self.damage, self.rubberDamage, self)
                
            self.target-=1
            if self.target < 0:
                game.entityList.remove(self)

    # Draw the entity on the game window
    def draw(self):
        if self.special == "lightning":
            for x in self.cords:
                pygame.draw.line(game.gameWindow, (255, 255, 0), (x[0], x[1]), (x[2], x[3]), 10)
            return
        elif self.special == "superLightning":
            for x in self.cords:
                pygame.draw.line(game.gameWindow, (0, 255, 255), (x[0], x[1]), (x[2], x[3]), 10)
            return            
        # Render the entity's image at its current position, centered
        game.gameWindow.blit(self.image, (self.x - self.size[0] / 2, self.y - self.size[1] / 2))

# Placeholder Class
class Placeholder:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# Creates Projectile
class projectile:

    def __init__(self, x, y, tower, target, upgrades, damage, rubberDamage, bulletHealth, autoaim, radius, special, life, fakeX = 0, fakeY = 0):
        # Sets raw stats and adds it to the list of all projectiles
        game.projectileList.append(self)
        self.x = x+40
        self.y = y+40
        self.damage = damage
        self.rubberDamage = rubberDamage
        self.target = target
        self.bulletHealth = bulletHealth
        self.autoAim = autoaim
        self.radius = radius
        self.special = special
        self.life = life

        if self.target == None:
            self.target = Placeholder(fakeX, fakeY)
            target = self.target
        self.id = entity._idCounter
        entity._idCounter += 1

        # Calculates Angle
        self.angle = np.degrees(np.arctan2(self.y - target.y, self.x- target.x)) + 180

        tower = re.sub(r'\d+', '', tower)

        # Sets Image
        self.image = pygame.transform.scale(pygame.image.load(f"{prefix}attacks/{tower}/{upgrades}.png").convert_alpha(), (10, 10))  
        # Sets counter to update its angle
        self.updateCounter = 0
        pass

    # Draws to screen
    def draw(self):
        game.gameWindow.blit(self.image, (self.x-5, self.y-5))
        if self.updateCounter % 5 == 0:
            self.image = pygame.transform.rotate(self.image, 90)

    def update(self):
        # Sets up so the bullet can die
        if self.life:
            self.life -= 1
            if self.life < 1:
                # Handles the Fat Cat
                if self.special == "stomp":
                    damagedBalloons = []
                    for otherYarnBall in game.yarnList:
                        if calDistance(otherYarnBall.x, self.x, otherYarnBall.y, self.y) < self.radius:
                            damagedBalloons.append(otherYarnBall)
                    # Damages the balloons
                    for otherYarnBall in damagedBalloons:
                        otherYarnBall.damageYarn(self.damage, self.rubberDamage, self)
                        
                    effect(self.x, self.y, "stomp0", (200, 200), 3)

                # Delets the bullet
                game.projectileList.remove(self)
                return      

        # Increment the update counter each time update is called
        self.updateCounter += 1

        # Update the projectile's position based on its current angle and speed (15 units per frame)
        self.x += np.cos(np.radians(self.angle)) * 15
        self.y += np.sin(np.radians(self.angle)) * 15

        # Auto-aim feature: adjust the angle every 3 updates to point toward the target
        if self.updateCounter % 3 == 0 and self.autoAim:
            # Calculate the angle needed to point toward the target and add 180 to reverse direction
            self.angle = np.degrees(np.arctan2(self.y - self.target.y, self.x - self.target.x)) + 180

        # Checks for collision
        if len(game.yarnList) > 0:
            for yarnBall in game.yarnList:
                # Detects Collision with primary yarnBall
                if calDistance(yarnBall.x, self.x, yarnBall.y, self.y) < 30:
                    # Handles normal bullet behavior
                    if self.radius == 1:

                        # Apply damage and check if the projectile should be removed
                        result = yarnBall.damageYarn(self.damage, self.rubberDamage, self)

                        # If the "parent" of the yarn was already hit
                        if result == "pass":
                            return

                        # If the yarn is rubber and cant be destroyed by the current projectile
                        if result == "yarn" or result == "delete":
                            game.projectileList.remove(self)
                            return
                        

                        # Decrease bullet health after hitting
                        self.bulletHealth -= 1

                        # Removes Targeting
                        self.target = None
                        self.autoAim = False

                        # Deletes projectile if its low on health
                        if self.bulletHealth <= 0:
                            game.projectileList.remove(self)
                            return
                    else:
                        # Special case: explosion effect
                        if self.special == "tankExplosion":
                            effect(yarnBall.x, yarnBall.y, "Tank1", (200, 200), 3)

                        # Cant modify a list when moving through it
                        damagedBalloons = []

                        # Handle splash damage for all yarn balls within `self.radius`
                        for otherYarnBall in game.yarnList:
                            if calDistance(otherYarnBall.x, self.x, otherYarnBall.y, self.y) < self.radius:
                                damagedBalloons.append(otherYarnBall)
                        
                        # Damages the balloons
                        for otherYarnBall in damagedBalloons:
                            otherYarnBall.damageYarn(self.damage, self.rubberDamage, self)

                        # Decrease bullet health after splash
                        self.bulletHealth -= 1

                        # Removes Targeting
                        self.target = None
                        self.autoAim = False

                        if self.bulletHealth <= 0:
                            game.projectileList.remove(self)
                            return
                        
        # Removes if off map         
        if self.x < -50 or self.x > 950 or self.y < -50 or self.y > 950:
            game.projectileList.remove(self)
            return
        

        # Calculates Distance
        if self.target != None:
            distance = calDistance(self.x, self.target.x, self.y, self.target.y)
        
            # Turns off autoAim when close
            if distance < 70:
                self.autoAim = False

# Class for effects on screen such as explosions
class effect:
    def __init__(self, x, y, sprite, size, time):
        game.effectList.append(self)
        self.image = pygame.transform.scale(pygame.image.load(f"{prefix}effects/{sprite}.png").convert_alpha(), size)
        self.x = x
        self.y = y
        self.time = time
        self.size = size
        self.sprite = sprite
        pass
    
    def draw(self):
        #Draws the sprite
        game.gameWindow.blit(self.image, (self.x - (self.size[0]//2), self.y - (self.size[1]//2)))

        # Handels Deletion
        self.time -= 1
        if self.time < 1:
            if self.sprite == "Tank1":
                effect(self.x, self.y, "Tank2", (200,200), 3)
            if self.sprite == "Tank2":
                effect(self.x, self.y, "Tank3", (200,200), 3)  


            if self.sprite == "stomp0":
                effect(self.x, self.y, "stomp1", (200,200), 2)   
            if self.sprite == "stomp1":
                effect(self.x, self.y, "stomp2", (200,200), 2) 
            if self.sprite == "stomp2":
                effect(self.x, self.y, "stomp3", (200,200), 2) 
            if self.sprite == "stomp3":
                effect(self.x, self.y, "stomp4", (200,200), 2) 
            if self.sprite == "stomp4":
                effect(self.x, self.y, "stomp5", (200,200), 2) 




            game.effectList.remove(self)
            return
        


# Sets up yarn for cats to scratch
class yarn:

    # Sets up yarn raw stats
    # Size, Speed, Damage, Health, Spawns
    yarnStats = {
        1 : (40, 2, 1, 1, []),
        2 : (40, 2, 2, 1, [1]),
        3 : (40, 2, 4, 1, [2, 2]),
        4 : (40, 4, 8, 1, [3]),
        5 : (40, 2, 16, 1, [4, 4, 4]),
        6 : (40, 1.5, 32, 1, [5, 5]),
        7 : (40, 1, 64, 10, [5, 5, 5, 5]),
        8 : (80, .5, 128, 50, [7, 7, 6, 6, 6, 6, 6, 5, 5, 4, 4]),
        9 : (80, 1, 999, 75, [8, 8, 8, 8, 7, 7]),
        10 : (80, 1.5, 9999, 150, [9, 9, 9, 9]),
        11 : (80, .25, 99999, 500, [10, 10, 10, 10]),
        12: (80, 1, 999999999, 2000, [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    }
    def __init__(self, x, y, layer, checkpoint=0, alreadyCollided = None, mapCordsRandRange = -10):
        
        #Gives yarn its stats
        self.size = yarn.yarnStats[layer][0]
        self.speed = yarn.yarnStats[layer][1]
        self.damage = yarn.yarnStats[layer][2]
        self.health = yarn.yarnStats[layer][3]
        self.spawns = yarn.yarnStats[layer][4]
        self.layer = layer
        self.isDead = False
        # Weird that it works
        self.alreadyCollided = alreadyCollided if alreadyCollided is not None else []

        try:
            self.image1 = pygame.transform.scale(pygame.image.load(f"{prefix}yarn/layer{layer}/0.png").convert_alpha(), (self.size, self.size))  
            self.image2 = pygame.transform.scale(pygame.image.load(f"{prefix}yarn/layer{layer}/1.png").convert_alpha(), (self.size, self.size))  
        except:
            print(f"Warning: Missing image files for layer {layer}. Using placeholder.")
            self.image1 = pygame.transform.scale(pygame.image.load(f"{prefix}yarn/layer{1}/0.png").convert_alpha(), (self.size, self.size)) 
            self.image2 = pygame.transform.scale(pygame.image.load(f"{prefix}yarn/layer{1}/1.png").convert_alpha(), (self.size, self.size))  

        # Use for animations on the yarn
        self.counter = 0

        self.x = x
        self.y = y

        # Distance Setter
        self.distance = 0

        # Sets next checkpoint
        self.checkpoint = checkpoint

        self.mapCordsRandRange = -10

        # Gets the cords of the maps key checkpoints for the yarn to path find
        self.mapCords = game.mapCords
        if game.mapNum == 7:
            if mapCordsRandRange == -10:
                self.mapCordsRandRange = random.randrange(0,4)
                self.mapCords = game.mapCords[self.mapCordsRandRange]
                self.x = self.mapCords[0][0]
                self.y = self.mapCords[0][1]
            else:
                self.mapCordsRandRange = mapCordsRandRange
                self.mapCords = game.mapCords[self.mapCordsRandRange]


        game.yarnList.append(self)

        pass



    def toDict(self):
        return {
            'x': self.x,
            'y': self.y,
            'layer': int(self.layer),
            'checkpoint': self.checkpoint,
            'mapCords': self.mapCordsRandRange
        }


    def fromDict(data):
        return yarn(data['x'], data['y'], data['layer'], data['checkpoint'], None, data['mapCords'])

    # Used for getting the value
    def getValue(self, yarnLayer):
        return sum([self.getValue(x) for x in self.yarnStats[yarnLayer][4]]) if yarnLayer != 1 else 1


    # Creates function that allows for drawing of the yarn
    def draw(self):
        self.counter += .1
        # Alternates between animation 0 and 1
        if round(self.counter) % 2 == 1:
            game.gameWindow.blit(self.image1, (self.x-self.size/2, self.y-self.size/2))
        else:
            game.gameWindow.blit(self.image2, (self.x-self.size/2, self.y-self.size/2))

    def update(self):
        if self not in game.yarnDeleteList and self.layer<6 and game.round > 55:
            game.money+=1
            game.yarnDeleteList.append(self)

        # Moves the yarn to the next target on the map
        targetX, targetY = self.mapCords[self.checkpoint]
        # Update x and y towards target
        self.x += self.speed if self.x < targetX else -self.speed
        self.y += self.speed if self.y < targetY else -self.speed

        # Snap to target if close enough
        if abs(self.x - targetX) < 10:
            self.x = targetX
        if abs(self.y - targetY) < 10:
            self.y = targetY

        # Move to the next checkpoint if reached
        if self.x == targetX and self.y == targetY:
            self.checkpoint += 1

        # Calculates Distance Score
        self.distance = -(-(self.checkpoint*5000) + calDistance(self.x, targetX, self.y, targetY))
        
        # Deletes Yarn and Applys Damage if it reaches the end of the map
        if self.checkpoint > len(self.mapCords) - 1:
            game.health -= self.damage
            if game.gamemode == "cashhealth":
                game.money -= self.damage
            if self not in game.yarnDeleteList:
                game.yarnDeleteList.append(self)

    def damageYarn(self, damage, rubberDamage, projectile):
        global cash


        # Get target coordinates
        targetX, targetY = self.mapCords[self.checkpoint]

        # Avoid processing the same projectile twice
        if projectile.id in self.alreadyCollided:
            return "pass"

        # Check if the yarn is immune to the projectile
        if self.layer in (6, 7) and not rubberDamage:
            return "yarn"

        # Deduct health
        self.health -= damage

        moneyMultiplier = 1
        for tower in game.towersOnMap:
            if calDistance(self.x, tower.x, self.y, tower.y) < tower.range:
                if tower.name == "Box":
                    moneyMultiplier = tower.damage

        # If yarn is still alive, delete the projectile and return
        if self.health > 0:
            return "delete"
        cash += 1
        if game.difficulty == 1:
            moneyMultiplier*=2
        if game.round > 50:
            moneyMultiplier*=.75

        self.alreadyCollided.append(projectile.id)

        # Process "death" only once
        if not getattr(self, 'is_dead', False):
            self.is_dead = True  # Mark as "dead"
            self.health = 0 

            if self in game.yarnList:
                priorLayer = self.layer

                # Adjust the layer and calculate spawns
                if self.layer < 9:
                    self.layer = max(1, self.layer - np.ceil(damage - 1))

                self.spawns = yarn.yarnStats[self.layer][4]

                # Handels money
                if self.layer == 1:
                    game.money+= int(self.getValue(priorLayer)*moneyMultiplier)
                    if game.round > 40:
                        game.money -= int((int(self.getValue(priorLayer)*moneyMultiplier))/2)

                for z in self.spawns:
                    # Update x and y positions if significantly far from target
                    if abs(self.x - targetX) > 5:
                        self.x += self.speed * 5 if self.x < targetX else -self.speed * 5
                    if abs(self.y - targetY) > 5:
                        self.y += self.speed * 5 if self.y < targetY else -self.speed * 5

                    # Spawn new yarn
                    
                    yarn(self.x, self.y, z, self.checkpoint, alreadyCollided=self.alreadyCollided[:], mapCordsRandRange=self.mapCordsRandRange)
                    
                # Schedule removal from game yarn list
                if self not in game.yarnDeleteList:
                    game.yarnDeleteList.append(self)




# Tower selection class for handling tower icons in the UI
class towerSelect:

    towerCosts = {
        "Calico": 50,
        "Fat": 300,
        "Magic": 80,
        "Tank": 150,
        "fishFarm": 400,
        "Gun":75,
        "Box": 200,
        "Dumb": 125
    }

    towerUpgradePricesCalico = {
        "1-0": 40,
        "2-0": 290,
        "3-0": 2000,
        "0-1": 40,
        "0-2": 290,
        "0-3": 400,
        "4-0": 7500,
        "0-4": 2000,
    }


    towerUpgradePricesTank = {
        "1-0": 60,
        "2-0": 500,
        "3-0": 1500,
        "0-1": 40,
        "0-2": 140,
        "0-3": 330,
        "0-4": 500,
        "4-0": 50000,
    }

    towerUpgradePricesFat = {
        "1-0": 125,
        "2-0": 3500,
        "3-0": 7000,
        "0-1": 500,
        "0-2": 2500,
        "0-3": 7000,
        "0-4": 15000,
        "4-0": 25000
    }

    towerUpgradePricesMagic = {
        "1-0": 50,
        "2-0": 750,
        "3-0": 5020,
        "0-1": 40,
        "0-2": 730,
        "0-3": 2950,
        "0-4": 10000,
        "4-0": 10000
    }

    towerUpgradePricesfishFarm = {
        "1-0": 500,
        "2-0": 1000,
        "3-0": 5000,
        "0-1": 350,
        "0-2": 750,
        "0-3": 7500,
        "0-4": 20000,
        "4-0": 10000
    }

    towerUpgradePricesGun = {
        "1-0": 100,
        "2-0": 200,
        "3-0": 1050,
        "0-1": 150,
        "0-2": 500,
        "0-3": 7500,
        "0-4": 10000,
        "4-0": 10000
    }


    towerUpgradePricesBox = {
        "1-0": 500,
        "2-0": 2500,
        "3-0": 300,
        "4-0": 7500,
        "0-1": 500,
        "0-2": 3000,
        "0-3": 10000,
        "0-4": 7500,
    }

    towerUpgradePricesDumb = {
        "1-0": 200,
        "2-0": 500,
        "3-0": 2000,
        "4-0": 10000,
        "0-1": 100,
        "0-2": 500,
        "0-3": 1000,
        "0-4": 2000,
    }



    towerDescriptions = {
        "Calico": "Basic Cat that Spits Hairballs on Yarn",
        "Fat": "Fat Cat that jumps to make shockwaves",
        "Magic": "Magic Cat that uses energy to destroy Yarn",
        "Tank": "Cat in a tank that can pop Rubber Band Balls",
        "fishFarm": "Fish Cat that fishes for fish to sell",
        "Gun": "Gun Cat that has a gun to shoot the Yarn",
        "Box": "Box that cats can go to to get buffed",
        "Dumb": "Dumb Cat that wants to run around the map"
    }


    towerDescriptionsCalico = {
        "0-1": "Pierces through one yarn",
        "0-2": "Deals damage to rubber balls",
        "0-3": "More pierce and damage",
        "0-4": "Even more damage",
        "1-0": "Faster attack speed",
        "2-0": "Even faster attack speed",
        "3-0": "Fastest attack speed",
        "4-0": "Really, really fast attack speed",
    }

    towerDescriptionsTank = {
        "0-1": "Faster reload",
        "0-2": "Increased range",
        "0-3": "Increased pierce",
        "0-4": "Drastically increased pierce",
        "1-0": "Increased damage",
        "2-0": "Splash damage",
        "3-0": "Increased damage",
        "4-0": "Even more damage",
    }

    towerDescriptionsFat = {
        "0-1": "Faster attack speed",
        "0-2": "Significantly faster attack speed",
        "0-3": "Really fast attck speed",
        "0-4": "Really, really fast attack speed",
        "1-0": "More damage, deals damage to rubber balls",
        "2-0": "More damage, bigger AOE",
        "3-0": "Even more damage and bigger AOE",
        "4-0": "All the damage",
    }


    towerDescriptionsMagic = {
        "0-1": "Faster attack speed",
        "0-2": "Chain damage",
        "0-3": "Increased damage, larger chain range",
        "0-4": "Increased damage, largest chain range",
        "1-0": "Increased damage",
        "2-0": "Puts potion on track that deal damage",
        "3-0": "Potions deal more damage, deal rubber damage",
        "4-0": "Potions deal even more damage",
    }
    towerDescriptionsfishFarm = {
        "0-1": "Generates fish more often",
        "0-2": "Automatically collects fish",
        "0-3": "Generates fish more often",
        "0-4": "Generates fish really fast",
        "1-0": "Fish give more money",
        "2-0": "Fish give even more money",
        "3-0": "Fish give a lot more money",
        "4-0": "Fish are worth a LOT of money",
    }
    towerDescriptionsGun = {
        "0-1": "Damaged rubber balls",
        "0-2": "Increased range and pierce",
        "0-3": "Increased damage for snipers",
        "0-4": "Well lets just say its crazy powerful",
        "1-0": "Pierce damage",
        "2-0": "Spread damage",
        "3-0": "Faster fire rate",
        "4-0": "Supercharged shotgun that destroys everything",
    }

    towerDescriptionsBox = {
        "0-1": "Reduces cost of nearby towers slightly",
        "0-2": "Further reduction in tower costs",
        "0-3": "Significant cost reduction for all towers",
        "0-4": "Doubles yarn value in its range when destroyed",
        "1-0": "Provides slight buffs to nearby towers",
        "2-0": "Enhances buffs with improved range",
        "3-0": "Allows all tower in range to destroy rubber",
        "4-0": "Massive buffs with increased range",
    }

    towerDescriptionsDumb = {
        "1-0": "Increased damage",
        "2-0": "Moves faster with faster attack rate",
        "3-0": "Moves even faster with increased attack rate",
        "4-0": "Moves really fast",

        "0-1": "Can do rubber damage",
        "0-2": "Pierce and more damage",
        "0-3": "Even more pierce and more damage",
        "0-4": "Even more pierce and more damage",
    }

    def __init__(self, x, y, name):
        # Load and scale the tower selection icon image
        self.image = pygame.image.load(f"{prefix}ui/{name}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  
        self.name = name
        
        # Add this instance to the game's list of tower selection icons
        game.towersMenuSelect.append(self)
        
        # Set the position of the icon in the UI window
        self.x = x
        self.y = y




    # Draw the tower icon in the UI, and handle selection logic
    def draw(self, mousePos, mousePress):
        # Check if the mouse is hovering over the icon
        if mousePos[0] > self.x and mousePos[0] < self.x + 100 and mousePos[1] > self.y and mousePos[1] < self.y + 100:
            # Slightly enlarge icon when hovered over
            modImage = pygame.transform.scale_by(self.image, 1.1)  
            game.gameUIWindow.blit(modImage, (self.x - 5, self.y - 5))
            
            game.hover = towerSelect.towerDescriptions[self.name]

            # Select or deselect tower on click release
            if mousePress[0] and mouseUp:
                if game.selected != self.name:
                    game.selected = self.name
                else:
                    game.selected = None
                
        else:
            # Draw the icon at its regular size when not hovered
            game.gameUIWindow.blit(self.image, (self.x, self.y))
        
        # Highlight the icon if it’s selected
        if game.selected == self.name:
            pygame.draw.rect(game.gameUIWindow, (150, 255, 150), (self.x - 10, self.y - 10, 120, 120), 5)

# Class representing a placed tower on the map
class towerEntity:



    # Range, Attack Speed, Rubber Damage, Damage, Projectile Health, Splash, Special, Bullet Life, Is Entity
    towerStatsCalico = {
        "0-0": (200, 50, False, 1, 0, 1, "None", None, False),
        "0-1": (200, 50, False, 1, 2, 1, "None", None, False),
        "1-1": (200, 40, False, 1, 2, 1, "None", None, False),
        "0-2": (200, 50, True, 1, 2, 1, "None", None, False),
        "1-2": (200, 40, True, 1, 2, 1, "None", None, False),
        "0-3": (200, 50, True, 3, 5, 1, "None", None, False),
        "1-3": (200, 40, True, 3, 5, 1, "None", None, False),
        "0-4": (200, 50, True, 10, 5, 1, "None", None, False),
        "1-4": (200, 40, True, 10, 5, 1, "None", None, False),

        "2-0": (200, 30, False, 1, 0, 1, "None", None, False),
        "1-0": (200, 40, False, 1, 0, 1, "None", None, False),
        "2-1": (200, 30, False, 1, 2, 1, "None", None, False),
        "3-0": (200, 10, False, 1, 0, 1, "None", None, False),
        "3-1": (200, 10, False, 1, 2, 1, "None", None, False),
        "4-0": (200, 3, False, 1, 0, 1, "None", None, False),
        "4-1": (200, 3, False, 1, 2, 1, "None", None, False)
    }

    towerStatsTank = {
        "0-0": (200, 100, True, 1, 0, 1, "None", None, False),
        "1-0": (200, 100, True, 2, 0, 1, "None", None, False),
        "2-0": (200, 100, True, 2, 0, 100, "tankExplosion", None, False),
        "3-0": (200, 100, True, 4, 0, 100, "tankExplosion", None, False),
        "1-1": (200, 60, True, 2, 0, 1, "None", None, False),
        "2-1": (200, 60, True, 2, 0, 100, "tankExplosion", None, False),
        "3-1": (200, 60, True, 4, 0, 100, "tankExplosion", None, False),

        "4-1": (200, 60, True, 20, 0, 100, "tankExplosion", None, False),
        "4-0": (200, 100, True, 20, 0, 100, "tankExplosion", None, False),


        "0-1": (200, 60, True, 1, 0, 1, "None", None, False),
        "0-2": (350, 60, True, 1, 0, 1, "None", None, False),
        "0-3": (350, 60, True, 1, 10, 1, "None", None, False),
        "1-2": (350, 60, True, 2, 0, 1, "None", None, False),
        "1-3": (350, 60, True, 2, 10, 1, "None", None, False),

        "1-4": (350, 60, True, 2, 999, 1, "None", None, False),
        "0-4": (350, 60, True, 1, 999, 1, "None", None, False),

    }

    towerStatsFat = {
        "0-0": (150, 100, False, 1, 0, 175, "stomp", 1, False),

        "1-0": (175, 100, True, 2, 0, 200, "stomp", 1, False),
        "2-0": (200, 100, True, 4, 0, 225, "stomp", 1, False),
        "3-0": (225, 100, True, 8, 0, 250, "stomp", 1, False),

        "0-1": (150, 80, False, 1, 0, 175, "stomp", 1, False),
        "0-2": (150, 50, False, 1, 0, 175, "stomp", 1, False),
        "0-3": (150, 30, False, 1, 0, 175, "stomp", 1, False),

        "1-1": (175, 80, True, 1, 0, 200, "stomp", 1, False),
        "1-2": (175, 50, True, 1, 0, 200, "stomp", 1, False),
        "1-3": (175, 30, True, 1, 0, 200, "stomp", 1, False),

        "2-1": (200, 80, True, 4, 0, 225, "stomp", 1, False),
        "3-1": (225, 80, True, 8, 0, 250, "stomp", 1, False),


        "4-0": (250, 100, True, 16, 0, 300, "stomp", 1, False),
        "4-1": (250, 80, True, 16, 0, 300, "stomp", 1, False),

        "0-4": (150, 5, False, 1, 0, 175, "stomp", 1, False),
        "1-4": (175, 5, True, 1, 0, 200, "stomp", 1, False),

    }

    towerStatsMagic = {
        "0-0": (200, 60, False, 1, 0, 1, "None", None, False),

        "1-0": (200, 60, False, 2, 0, 1, "None", None, False),

        "2-0": (200, 60, False, .2, 0, 1, "Potion", 120, True),

        "3-0": (200, 40, True, .4, 0, 1, "otherPotion", 120, True),


        "0-1": (200, 40, False, 1, 0, 1, "None", None, False),

        "1-1": (200, 40, False, 2, 0, 1, "None", None, False),

        "2-1": (200, 40, False, .2, 0, 1, "Potion", 120, True),

        "3-1": (200, 30, True, .4, 0, 1, "otherPotion", 120, True),

        "0-2" : (200, 50, False, 1, 1, 1, "lightning", 2, True),

        "0-3" : (250, 40, True, 1, 1, 1, "lightning", 4, True),


        "1-2" : (200, 50, False, 2, 1, 1, "lightning", 2, True),

        "1-3" : (250, 40, True, 2, 1, 1, "lightning", 4, True),



        "1-4" : (250, 20, True, 2, 1, 1, "superLightning", 40, True),
        "0-4" : (250, 20, True, 1, 1, 1, "superLightning", 40, True),

        "4-1": (200, 30, True, 1, 0, 1, "2otherPotion", 240, True),
        "4-0": (200, 40, True, 1, 0, 1, "2otherPotion", 240, True),


    }
    

    # TOWER UNIQUE!!!! 0, MONEY OUTPUT SPEED, AUTOCOLLECT, VALUE, 0, FALSE, "MONEY", DESPAWN TIME, TRUE
    towerStatsfishFarm = {
        "0-0" : (0, 500, False, 15, 0, False, "money", 500, True),

        "0-1" : (0, 250, False, 15, 0, False, "money", 500, True),
        "0-2" : (0, 250, True, 15, 0, False, "money", 500, True),
        "0-3" : (0, 50, True, 15, 0, False, "money", 500, True),

        "1-1" : (0, 250, False, 20, 0, False, "money", 500, True),
        "1-2" : (0, 250, True, 20, 0, False, "money", 500, True),
        "1-3" : (0, 50, True, 20, 0, False, "money", 500, True),



        "1-0" : (0, 500, False, 20, 0, False, "money", 500, True),
        "2-0" : (0, 500, False, 30, 0, False, "money0", 500, True),
        "3-0" : (0, 500, False, 50, 0, False, "money1", 500, True),

        "2-1" : (0, 250, False, 30, 0, False, "money0", 500, True),
        "3-1" : (0, 250, False, 50, 0, False, "money1", 500, True),

        "4-1" : (0, 250, False, 100, 0, False, "money2", 500, True),
        "4-0" : (0, 500, False, 100, 0, False, "money2", 500, True),

        "1-4" : (0, 25, True, 20, 0, False, "money", 500, True),
        "0-4" : (0, 25, True, 15, 0, False, "money", 500, True),


    }

    # Range, Attack Speed, Rubber Damage, Damage, Projectile Health, Splash, Special, Bullet Life, Is Entity

    towerStatsGun = {
        "0-0": (200, 50, False, 1, 0, 1, "None", None, False),
        "1-0": (200, 50, False, 1, 2, 1, "None", None, False),
        "2-0": (150, 50, False, 1, 2, 1, "Shotgun", 10, False),
        "3-0": (200, 25, False, 1, 2, 1, "SuperShotgun", 15, False),

        "0-1": (200, 50, True, 1, 0, 1, "None", None, False),
        "0-2": (500, 100, True, 3, 2, 1, "None", None, False),
        "0-3": (1000, 120, True, 15, 3, 1, "None", None, False),

        "1-1": (200, 50, True, 1, 2, 1, "None", None, False),
        "1-2": (500, 100, True, 3, 3, 1, "None", None, False),
        "1-3": (1000, 120, True, 15, 4, 1, "None", None, False),

        "2-1": (150, 50, True, 1, 2, 1, "Shotgun", 10, False),
        "3-1": (200, 25, True, 1, 2, 1, "SuperShotgun", 15, False),

        "4-1": (200, 10, True, 1, 2, 1, "SuperShotgun", 15, False),
        "4-0": (200, 10, False, 1, 2, 1, "SuperShotgun", 15, False),

        "0-4": (1000, 120, True, 30, 3, 1, "None", None, False),
        "1-4": (1000, 120, True, 30, 4, 1, "None", None, False),


    }
    # TOWER UNIQUE!!!! Range, Attack Speed Buff + Range Buff, Rubber Buff, Yarn Value Multiplier, Money Off Tower, FALSE, "tower", DESPAWN TIME, TRUE
    towerStatsBox = {
        "0-0" : (200, 1.05, False, 1, 1, False, "box", 500, True),

        "1-0" : (200, 1.1, False, 1, 1, False, "box", 500, True),
        "2-0" : (200, 1.25, False, 1, 1, False, "box", 500, True),
        "3-0" : (200, 1.25, True, 1, 1, False, "box", 500, True),
        "4-0" : (200, 1.5, True, 1, 1, False, "box", 500, True),

        "0-1" : (200, 1.05, False, 1, .95, False, "box", 500, True),
        "0-2" : (200, 1.05, False, 1, .9, False, "box", 500, True),
        "0-3" : (200, 1.05, False, 1, .75, False, "box", 500, True),
        "0-4" : (200, 1.05, False, 2, .75, False, "box", 500, True),

        "1-1" : (200, 1.1, False, 1, .95, False, "box", 500, True),
        "1-2" : (200, 1.1, False, 1, .9, False, "box", 500, True),
        "1-3" : (200, 1.1, False, 1, .75, False, "box", 500, True),
        "1-4" : (200, 1.1, False, 2, .75, False, "box", 500, True),

        "2-1" : (200, 1.25, False, 1, .95, False, "box", 500, True),
        "3-1" : (200, 1.25, True, 1, .95, False, "box", 500, True),
        "4-1" : (200, 1.5, True, 1, .95, False, "box", 500, True),

    }


    # Range, Attack Speed, Rubber Damage, Damage, Projectile Health, Splash, Special, Bullet Life, Is Entity

    towerStatsDumb = {
        "0-0" : (150, 75, False, 1, 0, 1, "mobile", None, False, 16),
        "1-0" : (150, 75, False, 2, 0, 1, "mobile", None, False, 16),
        "2-0" : (150, 50, False, 2, 0, 1, "mobile", None, False, 15),
        "3-0" : (150, 25, False, 2, 0, 1, "mobile", None, False, 10),
        "4-0" : (150, 15, False, 2, 0, 1, "mobile", None, False, 5),

        "1-1" : (150, 75, True, 2, 0, 1, "mobile", None, False, 16),
        "2-1" : (150, 50, True, 2, 0, 1, "mobile", None, False, 15),
        "3-1" : (150, 25, True, 2, 0, 1, "mobile", None, False, 10),
        "4-1" : (150, 15, True, 2, 0, 1, "mobile", None, False, 5),


        "0-1" : (150, 75, True, 1, 0, 1, "mobile", None, False, 16),
        "0-2" : (150, 75, True, 2, 5, 1, "mobile", None, False, 16),
        "0-3" : (150, 75, True, 10, 10, 1, "mobile", None, False, 16),
        "0-4" : (150, 75, True, 20, 100, 1, "mobile", None, False, 16),

        "1-2" : (150, 75, True, 4, 5, 1, "mobile", None, False, 16),
        "1-3" : (150, 75, True, 20, 10, 1, "mobile", None, False, 16),
        "1-4" : (150, 75, True, 40, 100, 1, "mobile", None, False, 16),


    }



    def __init__(self, x, y, name, leftUpgrade = 0, rightUpgrade = 0, id = 0, rotation = 0, value = 0):
        # Load and scale the tower's initial image
        self.image = pygame.image.load(f"{prefix}towers/{name}/0-0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  
        
        self.trashButton = pygame.image.load(f"{prefix}ui/trashButton.png").convert_alpha()
        self.trashButton = pygame.transform.scale(self.trashButton, (150, 150))  


        # Set tower position and upgrade levels
        self.x = x
        self.y = y

        self.calcX=x
        self.calcY=y

        self.speed = 20

        self.leftUpgrade = leftUpgrade
        self.rightUpgrade = rightUpgrade
        self.name = name
        self.targetedTower = None
        self.rotation = rotation
        self.cooldown = 0
        self.range = 0
        self.isEntity = False

        self.costBuff = 1

        self.autoaim = True

        self.speedBuff=1
        if game.difficulty == 3:
            self.costBuff = 1.5        
        self.rangeBuff=1
        self.yarnBuff = False

        self.pathfindCooldown = 0
        self.path = []

        self.buffIcons = {
            "speedBuff": pygame.transform.scale( pygame.image.load(f"{prefix}towerEffects/speed.png").convert_alpha(), (35, 35)),
            "costBuff": pygame.transform.scale( pygame.image.load(f"{prefix}towerEffects/money.png").convert_alpha(), (35, 35)),
            "rangeBuff": pygame.transform.scale( pygame.image.load(f"{prefix}towerEffects/range.png").convert_alpha(), (35, 35)),
            "yarnBuff": pygame.transform.scale( pygame.image.load(f"{prefix}towerEffects/yarn.png").convert_alpha(), (35, 35)),

        }


        if value == 0:
            self.value = towerSelect.towerCosts[re.sub(r'\d+', '', name)]
        else:
            self.value = value

        invalidUpgrades = [(2, 3), (3, 2), (3, 3)]
        upgradePath = (leftUpgrade, rightUpgrade)

        if upgradePath in invalidUpgrades:
            if self.leftUpgrade == 2:
                self.leftUpgrade = 1
            elif self.rightUpgrade == 2:
                self.rightUpgrade = 1
            else:
                self.rightUpgrade = 1
                self.leftUpgrade = 1



        if id == 0:
            self.id = str(uuid.uuid4())
        else:
            self.id = id


        # Creates a dictionary containing the upgrade images
        self.upgradeImages = {}
        
        # Loop through the files in the tower's image folder
        tempName = re.sub(r'\d+', '', name)
        for filename in os.listdir(f"{prefix}upgrades/{tempName}"):
            if filename.endswith(".png"):

                # Load and scale the image
                image = pygame.image.load(os.path.join(f"{prefix}upgrades/{tempName}", filename)).convert_alpha()
                image = pygame.transform.scale(image, (300, 150))
                
                # Add the image to the dictionary under the correct upgrade levels
                self.upgradeImages[filename[:3]] = image        

        # Loads Stats
        self.updateImage()

        # Add this tower instance to the game map's list of towers
        game.towersOnMap.append(self)

    def toDict(self):
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'leftUpgrade': self.leftUpgrade,
            'rightUpgrade': self.rightUpgrade,
            'id': self.id,
            'rotation': self.rotation,
            'value': self.value
        }
    



    def fromDict(data):
        return towerEntity(data['x'], data['y'], data['name'], data['leftUpgrade'], data['rightUpgrade'], data['id'], data['rotation'], data['value'])
    




    def pathfind(start, end, outOfBounds):
        start = (50*(np.floor(start[0]/50)), 50*(np.floor(start[1]/50)))
        end = (50*(np.floor(end[0]/50)), 50*(np.floor(end[1]/50)))

        possibleDir = [(-50, 0), (50, 0), (0, 50), (0, -50)]

        visited = set()

        for bounds in outOfBounds:
            x1, y1, x2, y2 = bounds
            for x in range(x1, x2, 50):
                for y in range(y1, y2, 50):
                    visited.add((x, y))


        if start in visited:
            if (start[0]-50, start[1]) not in visited:
                start =  (start[0]-50, start[1])

            elif (start[0]+50, start[1]) not in visited:
                start =  (start[0]+50, start[1])

            elif (start[0], start[1]+50) not in visited:
                start =  (start[0], start[1]+50)

            elif (start[0], start[1]-50) not in visited:
                start =  (start[0], start[1]-50)
        

        queue = deque([(start, [start])])  # Use deque for efficient popping


        while queue:
            current, path = queue.popleft()  # Faster O(1) pop from the left

            if current == end:
                return path
            
            if current in visited:
                continue

            visited.add(current)

            for direction in possibleDir:
                nextPos = (current[0] + direction[0], current[1] + direction[1])

                if 0 <= nextPos[0] < 50*(np.floor(900/50)) and 0 <= nextPos[1] < 50*(np.floor(900/50)) and nextPos not in visited:
                    queue.append((nextPos, path + [nextPos]))























    def loadTrackInRange(self):
        newTrack = []
        counter = 0
        mapX, mapY = game.mapCords[0]
        
        while counter < len(game.mapCords):
            targetX, targetY = game.mapCords[counter]

            # Update x and y towards target
            mapX += 5 if mapX < targetX else -5
            mapY += 5 if mapY < targetY else -5

            # Snap to target if close enough
            if abs(mapX - targetX) < 10:
                mapX = targetX
            if abs(self.y - targetY) < 10:
                mapY = targetY

            # Adds point to map
            newTrack.append((mapX, mapY))


            # Move to the next checkpoint if reached
            if mapX == targetX and mapY == targetY:
                counter += 1

        return([x for x in newTrack if calDistance(x[0]-40, self.x, x[1]-40, self.y) < self.range])


    # Update method for tower functionality
    def update(self):
        # Handels Upgrades
        if self.x < game.mousePos[0]-300 < self.x + 80 and self.y < game.mousePos[1] < self.y + 80 and game.mousePress[0] and mouseUp and game.selected == None:
            if game.selectedTower == self:
                game.selectedTower = None
                if client.isOnline == True and client.host == False:
                    client.selectedID = None
            else:
                if game.selectedTower == None:
                    game.selectedTower = self
                    if client.isOnline == True and client.host == False:
                        client.selectedID = self.id
                elif game.selectedTower.y > 600 and mousePos[1] > 200:
                    game.selectedTower = self
                    if client.isOnline == True and client.host == False:
                        client.selectedID = self.id
                elif game.selectedTower.y < 600 and mousePos[1] < 700:
                    game.selectedTower = self
                    if client.isOnline == True and client.host == False:
                        client.selectedID = self.id

        # Detects if it attacks yarn or lays stuff on the track
        if self.isEntity:
            self.cooldown += (1*self.speedBuff)

            if self.special == "lightning" or self.special == "superLightning":
                # Initialize variables to find the closest yarn
                min_distance = float('inf')
                closest_yarn = None

                # Find the closest yarn within the range
                for yarn in game.yarnList:
                    distance = calDistance(self.x+40, yarn.x, self.y+40, yarn.y)

                    if distance < min_distance:
                        min_distance = distance
                        closest_yarn = yarn

                if closest_yarn:
                    self.rotation = ((-np.degrees(np.arctan2(self.y - closest_yarn.y, self.x - closest_yarn.x)) + 180) + self.rotation*9)/10

                # If a valid target is within range, calculate rotation and fire
                if closest_yarn and min_distance < self.range*self.rangeBuff and self.cooldown > self.attackSpeed:
                    self.cooldown = 0
                    entity(self.x, self.y, None, self.special, self.damage, self.bulletLife, self.rubberDamage)

            elif self.special == "money" or self.special == "money0" or self.special == "money1" or self.special == "money2":
                if self.cooldown > self.attackSpeed:
                    self.cooldown = 0
                    angle = random.uniform(0, 2*np.pi)
                    r = np.sqrt(random.uniform(0,1)) * 100
                    if self.rubberDamage == False:
                        entity(self.x+20, self.y+20, (self.x + 40 + r * np.cos(angle), self.y + 40 + r * np.sin(angle)), self.special, self.damage, self.bulletLife, self.rubberDamage)
                    else:
                        game.money+=self.damage



            elif self.special == "box":
                for tower in game.towersOnMap:
                    if tower == self:
                        pass
                    elif calDistance(self.x, tower.x, self.y, tower.y) < self.range*self.rangeBuff:

                        if tower.costBuff > self.projectileHealth:
                            tower.costBuff = self.projectileHealth

                        if tower.rangeBuff < self.attackSpeed:
                            tower.rangeBuff = self.attackSpeed

                        if tower.speedBuff < self.attackSpeed:
                            tower.speedBuff = self.attackSpeed

                        if self.rubberDamage:
                            tower.rubberDamage = self.rubberDamage
                            tower.yarnBuff = True

            elif self.cooldown > self.attackSpeed and len(self.trackInRange) > 0:
                self.cooldown = 0
                min_distance = float('inf')
                choice = random.choice(self.trackInRange)
                self.rotation = -np.degrees(np.arctan2(self.y - choice[1], self.x-choice[0])) + 180  
                entity(self.x, self.y, choice, self.special, self.damage, self.bulletLife, self.rubberDamage)


        elif self.special == "mobile":
            self.pathfindCooldown+=1
            if self.pathfindCooldown > 20:
                self.pathfindCooldown = 0
                if len(game.yarnList) != 0:
                    smallest = game.yarnList[0]
                    for yarnBall in game.yarnList:
                        if yarnBall.distance > smallest.distance:
                            smallest = yarnBall
                    self.targetedTower = smallest
                else:
                    self.targetedTower =None



                if self.targetedTower:
                    self.path = []
                    for offset in [(-75, 0), (0, 75), (75, 0), (0, -75)]:
                        self.path = towerEntity.pathfind((self.calcX+50, self.calcY+50), (self.targetedTower.x+offset[0], self.targetedTower.y+offset[1]), game.track)

                        if self.path:
                            break


            if self.path:
                #for x in self.path:
                 #   pygame.draw.circle(game.gameWindow, "RED", (x[0]+25, x[1] + 25), 5)
      
                self.calcX = self.path[0][0]-25
                self.calcY = self.path[0][1]-25

                if abs(self.x-self.calcX) < 25 and abs(self.y-self.calcY) < 25:
                    self.path.pop(0)


           # for x in range(0, 900, 50):
               # for y in range(0, 900, 50):
                    #pygame.draw.rect(game.gameWindow, "BLACK", pygame.Rect(x, y, 50, 50), 1)

            self.x = (self.x*self.speed+self.calcX)/(self.speed+1)
            self.y = (self.y*self.speed+self.calcY)/(self.speed+1)


            yarnInRange = []
            for yarnBall in game.yarnList:
                if np.sqrt((yarnBall.x-self.x-40)**2 + (yarnBall.y-self.y-40)**2) < self.range*self.rangeBuff:
                    yarnInRange.append(yarnBall)
            
            # Finds shortest one and if not returns None
            if len(yarnInRange) != 0:
                smallest = yarnInRange[0]
                for yarnBall in yarnInRange:
                    if yarnBall.distance > smallest.distance:
                        smallest = yarnBall
                self.targetedTower = smallest
            else:
                self.targetedTower =None



            if self.targetedTower:

                targetAngle = -np.degrees(np.arctan2(self.y - self.targetedTower.y, self.x - self.targetedTower.x)) + 180

                # Normalize the difference between the current and target angles
                angleDiff = (targetAngle - self.rotation + 180) % 360 - 180

                # Smoothly interpolate the rotation
                self.rotation += angleDiff / 10      

                self.cooldown += (1*self.speedBuff) 

                if self.cooldown > self.attackSpeed and calDistance(self.x+50, self.targetedTower.x, self.y+50, self.targetedTower.y) < 100:
                    self.cooldown = 0
                    projectile(self.x, self.y, self.name, self.targetedTower, (str(self.leftUpgrade) + "-" + str(self.rightUpgrade)), self.damage, self.rubberDamage, self.projectileHealth, self.autoaim, self.radius, "None", self.bulletLife)


        else:
            # Creates a list of all the towers in range
            yarnInRange = []
            for yarnBall in game.yarnList:
                if np.sqrt((yarnBall.x-self.x-40)**2 + (yarnBall.y-self.y-40)**2) < self.range*self.rangeBuff:
                    yarnInRange.append(yarnBall)
            
            # Finds shortest one and if not returns None
            if len(yarnInRange) != 0:
                smallest = yarnInRange[0]
                for yarnBall in yarnInRange:
                    if yarnBall.distance > smallest.distance:
                        smallest = yarnBall
                self.targetedTower = smallest
            else:
                self.targetedTower =None

            # Shoots at the tower
            if self.targetedTower:
                if self.cooldown > self.attackSpeed:
                    if self.special == "Shotgun":
                        for i in range(7):
                            pelletAngle = np.degrees(np.arctan2(self.y - self.targetedTower.y, self.x- self.targetedTower.x)) + 180          
                            distance = 100  
                            spread = 7
                            pelletAngle += ((i-.5)-3.5)*spread
                            fakeX = self.x + distance * np.cos(np.radians(pelletAngle))
                            fakeY = self.y + distance * np.sin(np.radians(pelletAngle))
                            projectile(self.x, self.y, self.name, None, (str(self.leftUpgrade) + "-" + str(self.rightUpgrade)), self.damage, self.rubberDamage, self.projectileHealth, self.autoaim, self.radius, self.special, self.bulletLife, fakeX, fakeY)
                        self.cooldown = 0
                    elif self.special == "SuperShotgun":
                        for i in range(10):
                            pelletAngle = np.degrees(np.arctan2(self.y - self.targetedTower.y, self.x- self.targetedTower.x)) + 180          
                            distance = 100  
                            spread = 5
                            pelletAngle += ((i-.5)-5)*spread
                            fakeX = self.x + distance * np.cos(np.radians(pelletAngle))
                            fakeY = self.y + distance * np.sin(np.radians(pelletAngle))
                            projectile(self.x, self.y, self.name, None, (str(self.leftUpgrade) + "-" + str(self.rightUpgrade)), self.damage, self.rubberDamage, self.projectileHealth, self.autoaim, self.radius, self.special, self.bulletLife, fakeX, fakeY)
                        self.cooldown = 0


                    else:
                        self.cooldown = 0 
                        projectile(self.x, self.y, self.name, self.targetedTower, (str(self.leftUpgrade) + "-" + str(self.rightUpgrade)), self.damage, self.rubberDamage, self.projectileHealth, self.autoaim, self.radius, self.special, self.bulletLife)



                targetAngle = -np.degrees(np.arctan2(self.y - self.targetedTower.y, self.x - self.targetedTower.x)) + 180

                # Normalize the difference between the current and target angles
                angleDiff = (targetAngle - self.rotation + 180) % 360 - 180

                # Smoothly interpolate the rotation
                self.rotation += angleDiff / 10      

                self.cooldown += (1*self.speedBuff) 


    def resetbuffs(self):
        self.speedBuff=1
        self.costBuff=1
        self.rangeBuff=1     
        self.yarnBuff = False
        if game.difficulty == 3:
            self.costBuff = 1.5


    # Draw the tower image at its position on the game map
    def draw(self):

        if self.name == "Fat":
            self.rotation = 270

        if game.selectedTower == self:
            transparency = pygame.Surface((900, 900), pygame.SRCALPHA)
            transparency.set_alpha(80)
            pygame.draw.circle(transparency, (90, 105, 136), (self.x + 40, self.y + 40), self.range*self.rangeBuff)
            game.gameWindow.blit(transparency, (0, 0))
            modImage = pygame.transform.scale(self.image, (100, 100))
            modImage = pygame.transform.rotate(modImage, self.rotation)
            rect = modImage.get_rect(center=(self.x + 40, self.y +40))

            game.gameWindow.blit(modImage, rect.topleft)

        else:
            rotatedImage = pygame.transform.rotate(self.image, self.rotation)
            rect = rotatedImage.get_rect(center=(self.x + 40, self.y + 40))
            game.gameWindow.blit(rotatedImage, rect.topleft)


    # Create the upgrade button for the player
    def handleUpgrades(self):
        # Dynamically select the correct upgrade price dictionary based on cat type
        tempName = re.sub(r'\d+', '', self.name)
        upgradePrices = getattr(towerSelect, f"towerUpgradePrices{tempName}", {})

        hoverText = getattr(towerSelect, f"towerDescriptions{tempName}", {})


        # Handle Left Upgrade
        if self.leftUpgrade < 4 and ((self.rightUpgrade > 1 and self.leftUpgrade == 1) == False):
            leftUpgrade = self.upgradeImages[f"{self.leftUpgrade+1}-0"]
            leftCost = upgradePrices.get(f"{self.leftUpgrade+1}-0", float('inf'))
            leftCost = int(leftCost*self.costBuff)
            canAffordLeft = game.money >= leftCost

            if 300 < mousePos[0] < 600 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset:
                game.displayPrice = str(leftCost)
                game.hover = hoverText.get(f"{self.leftUpgrade+1}-0", "ERROR")
            if 300 < mousePos[0] < 600 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset and canAffordLeft:
                leftUpgrade = pygame.transform.scale(leftUpgrade, (320, 160))
                game.gameWindow.blit(leftUpgrade, (0, 20 + game.vertOffset))
                if mousePress[0] and mouseUp:
                    game.money -= upgradePrices.get(f"{self.leftUpgrade+1}-0", 0)*self.costBuff
                    self.value += upgradePrices.get(f"{self.leftUpgrade+1}-0", 0)
                    self.leftUpgrade += 1
                    self.updateImage()
            else:
                if not canAffordLeft:
                    game.gameWindow.blit(pygame.transform.grayscale(leftUpgrade), (10, 25 + game.vertOffset))
                else:
                    game.gameWindow.blit(leftUpgrade, (10, 25 + game.vertOffset))

        # Handle Right Upgrade
        if self.rightUpgrade < 4 and ((self.leftUpgrade > 1 and self.rightUpgrade == 1) == False):
            rightUpgrade = self.upgradeImages[f"0-{self.rightUpgrade+1}"]
            rightCost = upgradePrices.get(f"0-{self.rightUpgrade+1}", float('inf'))
            rightCost = int(rightCost*self.costBuff)
            canAffordRight = game.money >= rightCost

            if 800 < mousePos[0] < 1100 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset:
                game.displayPrice = str(rightCost)
                game.hover = hoverText.get(f"0-{self.rightUpgrade+1}", "ERROR")

            if 800 < mousePos[0] < 1100 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset and canAffordRight:
                rightUpgrade = pygame.transform.scale(rightUpgrade, (320, 160))
                game.gameWindow.blit(rightUpgrade, (490, 20 + game.vertOffset))
                if mousePress[0] and mouseUp:
                    game.money -= upgradePrices.get(f"0-{self.rightUpgrade+1}", 0)*self.costBuff
                    self.value += upgradePrices.get(f"0-{self.rightUpgrade+1}", 0)
                    self.rightUpgrade += 1
                    self.updateImage()
            else:
                if not canAffordRight:
                    game.gameWindow.blit(pygame.transform.grayscale(rightUpgrade), (500, 25 + game.vertOffset))
                else:
                    game.gameWindow.blit(rightUpgrade, (500, 25 + game.vertOffset))

        activeBuffs = []
        if self.speedBuff != 1:
            activeBuffs.append(self.buffIcons["speedBuff"])
        if self.costBuff < 1:
            activeBuffs.append(self.buffIcons["costBuff"])
        if self.yarnBuff == True:
            activeBuffs.append(self.buffIcons["yarnBuff"])
        if self.rangeBuff != 1:
            activeBuffs.append(self.buffIcons["rangeBuff"])

        totalWidth = len(activeBuffs) * 35 + (len(activeBuffs) - 1) * 20

        startX = self.x + 40 - totalWidth//2

        for i, icon in enumerate(activeBuffs):
            game.gameWindow.blit(icon, (startX+i * (35+20), self.y-40))


        if client.isOnline == False:
            if 630<mousePos[0]<780 and 25+game.vertOffset<mousePos[1]<175+game.vertOffset:
                game.gameWindow.blit(pygame.transform.scale(self.trashButton, (160, 160)), (325, 20 + game.vertOffset))
                if mousePress[0]:
                    game.money += int(np.floor(self.value*.75))*self.costBuff
                    game.towersOnMapToRemove.append(self)
                    game.selectedTower = None
                    for tower in game.towersOnMap:
                        tower.resetbuffs()
                    return
            else:
                game.gameWindow.blit(self.trashButton, (330, 25 + game.vertOffset))

    def handleUpgradesOnline(self):
        if client.host == True:
            self.handleUpgrades()
            return
        
        if client.clientCooldown < 60:
            return

        upgradePrices = getattr(towerSelect, f"towerUpgradePrices{self.name}", {})

        # Handle Left Upgrade
        if self.leftUpgrade < 3 and ((self.rightUpgrade > 1 and self.leftUpgrade == 1) == False):
            leftUpgrade = self.upgradeImages[f"{self.leftUpgrade+1}-0"]
            leftCost = upgradePrices.get(f"{self.leftUpgrade+1}-0", float('inf'))
            canAffordLeft = game.money >= leftCost

            if 300 < mousePos[0] < 600 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset:
                game.displayPrice = str(upgradePrices.get(f"{self.leftUpgrade+1}-0", 0))

            if 300 < mousePos[0] < 600 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset and canAffordLeft:
                leftUpgrade = pygame.transform.scale(leftUpgrade, (320, 160))
                game.gameWindow.blit(leftUpgrade, (0, 20 + game.vertOffset))

                if mousePress[0] and mouseUp:
                    if canAffordLeft:
                        # Add to the local upgrade queue
                        upgradeData = {
                            "towerID": self.id,  # Unique identifier for the tower
                            "type": "left",
                            "level": self.leftUpgrade + 1,
                            "cost": leftCost
                        }
                        client.upgradeQueue.append(upgradeData)  # Add upgrade to queue
                        print(f"Upgrade queued: {upgradeData}")
                        game.money -= upgradePrices.get(f"{self.leftUpgrade+1}-0", 0)
                        client.clientCooldown = 0
            else:
                if not canAffordLeft:
                    game.gameWindow.blit(pygame.transform.grayscale(leftUpgrade), (10, 25 + game.vertOffset))
                else:
                    game.gameWindow.blit(leftUpgrade, (10, 25 + game.vertOffset))

        # Handle Right Upgrade
        if self.rightUpgrade < 3 and ((self.leftUpgrade > 1 and self.rightUpgrade == 1) == False):
            rightUpgrade = self.upgradeImages[f"0-{self.rightUpgrade+1}"]
            rightCost = upgradePrices.get(f"0-{self.rightUpgrade+1}", float('inf'))
            canAffordRight = game.money >= rightCost

            if 800 < mousePos[0] < 1100 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset:
                game.displayPrice = str(upgradePrices.get(f"0-{self.rightUpgrade+1}", 0))

            if 800 < mousePos[0] < 1100 and 20 + game.vertOffset < mousePos[1] < 180 + game.vertOffset and canAffordRight:
                rightUpgrade = pygame.transform.scale(rightUpgrade, (320, 160))
                game.gameWindow.blit(rightUpgrade, (490, 20 + game.vertOffset))
                if mousePress[0] and mouseUp:
                    if canAffordRight:
                        # Add to the local upgrade queue
                        upgradeData = {
                            "towerID": self.id,  # Unique identifier for the tower
                            "type": "right",
                            "level": self.rightUpgrade + 1,
                            "cost": rightCost
                        }
                        client.upgradeQueue.append(upgradeData)  # Add upgrade to queue
                        print(f"Upgrade queued: {upgradeData}")
                        game.money -= upgradePrices.get(f"0-{self.rightUpgrade+1}", 0)

                        client.clientCooldown = 0

            else:
                if not canAffordRight:
                    game.gameWindow.blit(pygame.transform.grayscale(rightUpgrade), (500, 25 + game.vertOffset))
                else:
                    game.gameWindow.blit(rightUpgrade, (500, 25 + game.vertOffset))


    def updateImage(self):
        # Updates Image
        self.image = pygame.image.load(f"{prefix}towers/{self.name}/{self.leftUpgrade}-{self.rightUpgrade}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  

        # Handels Upgrades
        # Range, Attack Speed, Rubber Damage, Damage, Projectile Health, Splash, Special, Bullet Life, Is Entity

        # Map tower names to their corresponding stats tables
        towerStatsMapping = {
            "Calico": towerEntity.towerStatsCalico,
            "Tank": towerEntity.towerStatsTank,
            "Fat": towerEntity.towerStatsFat,
            "Magic": towerEntity.towerStatsMagic,
            "fishFarm": towerEntity.towerStatsfishFarm,
            "Gun": towerEntity.towerStatsGun,
            "Box" : towerEntity.towerStatsBox,
            "Dumb" : towerEntity.towerStatsDumb
        }

        # Check if the name exists in the mapping
        if re.sub(r'\d+', '', self.name) in towerStatsMapping:
            stats = towerStatsMapping[re.sub(r'\d+', '', self.name)][f"{self.leftUpgrade}-{self.rightUpgrade}"]

            # Unpack stats into instance variables
            self.range = stats[0]
            self.attackSpeed = stats[1]
            self.rubberDamage = stats[2]
            self.damage = stats[3]
            self.projectileHealth = stats[4]
            self.radius = stats[5]
            self.special = stats[6]
            self.bulletLife = stats[7]
            self.isEntity = stats[8]
            if self.name == "Dumb":
                self.speed = stats[9]

        if self.isEntity:
            self.trackInRange = self.loadTrackInRange()


# Main game loop
running = True
mouseUp = False
pause = False
pKeyRelease = True


inGame = False

offsetx = 0
offsety = 0

avgTop = (0,0,0)
avgBottom = (0,0,0)
avgLeft = (0,0,0)
avgRight = (0,0,0)

def main():
    
    global mousePos, mousePress, mouseUp, pause, running, offsetx, offsety, avgTop, avgRight, avgLeft, avgBottom
    while running:
        # Get current mouse position and press states
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        mousePos = (mousePos[0]-offsetx, mousePos[1]-offsety)

        # Track if the left mouse button was just released
        if mousePress[0] == False:
            mouseUp = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for escape key press to quit
        key = pygame.key.get_pressed() 
        if key[pygame.K_ESCAPE]:
            running = False

        if key[pygame.K_p] and pKeyRelease:
            pause = not pause
            pKeyRelease = False

        

        if not key[pygame.K_p]:
            pKeyRelease = True


        if inGame:
            # Update game state with current mouse interactions
            if client.inGame == False and pause == False:
                game.gameUpdate(mousePos, mousePress)

            elif client.inGame == False and pause == True:
                game.gameUIUpdate()
                screen.blit(game.gameUIWindow, (0,0))
                game.draw_text("Pause", "BLACK", 450, 450, game.gameWindow, 200, True)
                pygame.draw.rect(game.gameWindow, "GREY", pygame.Rect(600, 0, 300, 100))
                game.draw_text(str(mousePos[0] - 300) + ", " + str(mousePos[1]), "BLACK", 650, 20, game.gameWindow, 50)
                screen.blit(game.gameWindow, (300, 0))
                pygame.display.flip()
                
            if client.inGame == True:
                game.onlineUpdate(mousePos, mousePress)

        elif not inGame:
            menu.update()

        # Reset mouse release tracking if button is pressed again
        if mousePress[0] == True:
            mouseUp = False
        
        if screenDis.get_width() != 1200:
            offsetx = (screenDis.get_width() - screen.get_width()) // 2
            offsety = (screenDis.get_height() - screen.get_height()) // 2

            screenDis.blit(screen, (offsetx, offsety))

            topRow = [screen.get_at((x, 0)) for x in range(1200)]
            rightColumn = [screen.get_at((1200 - 1, y)) for y in range(900)]
            bottomRow = [screen.get_at((x, 900 - 1)) for x in range(1200)]
            leftColumn = [screen.get_at((0, y)) for y in range(900)]

            def average_color(pixels):
                return tuple(
                    sum(pixel[i] for pixel in pixels) // len(pixels) for i in range(3) 
                )
            
            avgTop = (
                (average_color(topRow)[0] + avgTop[0] * 19) / 20, 
                (average_color(topRow)[1] + avgTop[1] * 19) / 20, 
                (average_color(topRow)[2] + avgTop[2] * 19) / 20
            )
            avgRight = (
                (average_color(rightColumn)[0] + avgRight[0] * 19) / 20, 
                (average_color(rightColumn)[1] + avgRight[1] * 19) / 20, 
                (average_color(rightColumn)[2] + avgRight[2] * 19) / 20
            )
            avgBottom = (
                (average_color(bottomRow)[0] + avgBottom[0] * 19) / 20, 
                (average_color(bottomRow)[1] + avgBottom[1] * 19) / 20, 
                (average_color(bottomRow)[2] + avgBottom[2] * 19) / 20
            )
            avgLeft = (
                (average_color(leftColumn)[0] + avgLeft[0] * 19) / 20, 
                (average_color(leftColumn)[1] + avgLeft[1] * 19) / 20, 
                (average_color(leftColumn)[2] + avgLeft[2] * 19) / 20
            )



            pygame.draw.rect(screenDis, (avgTop), pygame.Rect(0, 0, screenDis.get_width(), offsety))
            pygame.draw.rect(screenDis, (avgBottom), pygame.Rect(0, screenDis.get_height()-offsety, screenDis.get_width(), offsety))
            pygame.draw.rect(screenDis, (avgLeft), pygame.Rect(0, 0, offsetx, screenDis.get_height()))
            pygame.draw.rect(screenDis, (avgRight), pygame.Rect(screenDis.get_width()-offsetx, 0, offsetx, screenDis.get_height()))


        else:
            screenDis.blit(screen, (0,0))
            offsetx = 0
            offsety = 0




        pygame.display.flip()


from tkinter.scrolledtext import ScrolledText
import io

# Run the profiler
def profile_game():
    """Profile the Pygame game and return the stats as a string."""
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    
    # Capture stats in a string
    output = io.StringIO()
    stats = pstats.Stats(profiler, stream=output)
    stats.strip_dirs().sort_stats('cumulative').print_stats()
    return output.getvalue()

def show_stats_in_tkinter(stats):
    """Show profiling stats in a Tkinter window."""
    root = tk.Tk()
    root.title("Profiling Results")

    text_widget = ScrolledText(root, wrap=tk.WORD, width=100, height=40)
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert(tk.END, stats)
    text_widget.configure(state='disabled')  # Make it read-only

    root.mainloop()
def show_stats_in_tkinter_with_search(stats):
    def search():
        query = search_entry.get()
        text_widget.tag_remove("highlight", "1.0", tk.END)
        if query:
            start = "1.0"
            while True:
                start = text_widget.search(query, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(query)}c"
                text_widget.tag_add("highlight", start, end)
                start = end
            text_widget.tag_config("highlight", background="yellow", foreground="black")

    root = tk.Tk()
    root.title("Profiling Results")

    search_frame = tk.Frame(root)
    search_frame.pack(fill=tk.X)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    search_button = tk.Button(search_frame, text="Search", command=search)
    search_button.pack(side=tk.RIGHT)

    text_widget = ScrolledText(root, wrap=tk.WORD, width=100, height=40)
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert(tk.END, stats)
    text_widget.configure(state='disabled')

    root.mainloop()


if __name__ == '__main__':
    profiling_results = profile_game()
    show_stats_in_tkinter_with_search(profiling_results)


saveData = {
    'cash': cash,
    "maps": ownedmaps,
    "skins": ownedSkins
}
with open(f"{prefix}saves/savegame.json", "w") as file:
    json.dump(saveData, file, indent=5)

# Quit pygame and close the program
pygame.quit()
sys.exit()



