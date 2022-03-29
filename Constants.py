import pygame
pygame.init()
# RGB Definitions of colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

#Window size
sizeOfWindow = (1920, 1080)
sizeOfLevel = (sizeOfWindow[0], sizeOfWindow[1] - round(sizeOfWindow[1]/8)) #Size of game level, change is proportional to the size of the Window

#TileMap Creation
numberOfTilesHigh = 12 #How many divisions in the map vertically
numberOfTilesWide = 12 #How many divisions in the map horizontally
tileHeight = round(sizeOfLevel[1]/numberOfTilesHigh) #Creating the individual height of each tile to fit whatever size of window user has
tileWidth = round(sizeOfLevel[0]/numberOfTilesWide) #Creating the individual width of each tile to fit whatever size of window user has

MAPFILE = "Map.txt"
ENTITYFILE = "MapOfEntities.txt"

#Fonts and Text for Game

FONTFORPLAYERDETAILS = pygame.font.SysFont("Arial MS",int(128*sizeOfWindow[1]/1080)) #This will be the font which describes the player details, such as what weapon they have etc.
playerDetailsX = sizeOfWindow[0] - int(((sizeOfWindow[0])/4)) #Horizontally, will be 1/4 of entire window size away from right side
playerDetailsY = sizeOfWindow[1] - int((sizeOfWindow[1])/10) #Horizontally, will be 1/20 of entire window size away from bottom


#Images for game
HEARTPIC = pygame.image.load("Heart.png") #Loads the heart image from folder
heartPicSmall = pygame.transform.scale(HEARTPIC, (int(124*sizeOfWindow[0]/1920), int(100*sizeOfWindow[1]/1080))) #Scales heart pic to be smaller so it can fit on screen
heartX = sizeOfWindow[0]/22
heartY = sizeOfWindow[1] - sizeOfWindow[1]/10

WALLPIC = pygame.image.load("Wall.jpg")
wallPicScaled = pygame.transform.scale(WALLPIC, (tileWidth, tileHeight))  # This changes the size of the image to fit the tiles

FLOORPIC = pygame.image.load("Floor.jpg")
floorPicScaled = pygame.transform.scale(FLOORPIC, (tileWidth, tileHeight))  # This changes the size of the image to fit the tiles

#Sounds
#missedSound = pygame.mixer.Sound('missed.wav')

soundEffects = pygame.mixer.Channel(5)
attackSound = pygame.mixer.Sound("Attack.mp3")
hitSound = pygame.mixer.Sound("Hit.mp3")
failSound = pygame.mixer.Sound("ActionFailed.mp3")
attackSound.set_volume(0.35)
hitSound.set_volume(0.35)