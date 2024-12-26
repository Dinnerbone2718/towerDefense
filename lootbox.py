import pygame
import os
import random

pygame.init()
pygame.mixer.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
prefix = f"{script_dir}/"

print(prefix)

screen = pygame.display.set_mode((1200, 900), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption('Tower Defense')

class Audio:
    def __init__(self):
        self.lootBoxTick = pygame.mixer.Sound(f"{prefix}audio/lootBoxTick.wav")
        self.lootBoxDone = pygame.mixer.Sound(f"{prefix}audio/lootBoxDone.wav")


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

    def update(self):
        self.draw()

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

        elif self.selectionSpeed < 0.05:
            self.selectionSpeed = 0
            self.shuffleCount = 0
            audio.lootBoxDone.play()

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
            else:
                fadedImg = self.skins[key]
                fadedImg.set_alpha(50)
                screen.blit(fadedImg, (x * 200 + 300, y * 200 + 160))            

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.shuffledSpot%3 * 200 + 300, self.shuffledSpot//3 * 200 + 160, 160, 160), 10)

        self.selectedBox = (self.shuffledSpot%3, self.shuffledSpot//3)
        

menuLoot = lootBoxes()

audio = Audio()

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill("BLACK")
    menuLoot.update()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False