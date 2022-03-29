import Constants, pygame

def getImage(tileContents,entityList):
    if (tileContents == "m"): #If character in map file is this character, make the variable "tileImage" the correct image
        tileImage = Constants.wallPicScaled
    if tileContents == ".":
        tileImage = Constants.floorPicScaled

    else: #If it is an entity
        for i in entityList: #for each entity
            if i.gridLetter == tileContents:
                tileImage = i.pictureFile #load that entity's picture

    return tileImage

def drawMap(screen, mapTiles,entityList, isEntityMap):
    for j, tile in enumerate(mapTiles):  #For each row in world map, j is the index, tile is the element in maptiles[j]
        for i, tileContents in enumerate(tile): # for each tile in each row, i is the index, tileContents is the element in tile[i]
            if isEntityMap is False or (tileContents != "." and tileContents != "m"): #If it's not the entity map, or there is an entity in the position that needs to be drawn
                image = getImage(tileContents, entityList)
                screen.blit(image,(i * Constants.tileWidth, j * Constants.tileHeight))  # Put the image on the screen




def readMap(mapFile):
    with open(mapFile, 'r') as file:
        worldMap = file.readlines() #read map file

    for index, line, in enumerate(worldMap):
        worldMap[index] = line.strip() # remove \n at the end of each element in list

    return get2DMapList(worldMap) #Return map list

def get2DMapList(maplist):
    seperatedMapList = [] #creates new list to be added to as 2d list for coordinates
    for row in maplist:  # for each row in map list
        seperatedMapList.append(list(row))  # Creates seperatedMapList, with each list being a different row of the map with each letter seperated into seperate elements
    return seperatedMapList #returns 2d list with each list being a row, split up into seperate elements for each character

def worldMapCleaner(map):
    for i in map:
        for j in map:
            if map[i][j] != "m" and map[i][j] != ".":
                map[i][j] = "."

    return map

