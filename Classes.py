import GridMaker, Constants, random, pygame, time

class entity():
    def __init__(self,health,strength,gridLetter,pictureFile): # attributes for class to be used
        self.health = health #This will be the amount of health points the entity has
        self.strength = strength  #This will be the amount of damage to health points that the character will do
        self.gridLetter = gridLetter # This will be the letter that represents the character in the map file
        self.pictureFile = pygame.transform.scale(pygame.image.load(pictureFile), (Constants.tileWidth, Constants.tileHeight)) #This will be the name of the file for the picture for the entity

    def findSelf(self,entityFile):
        for row in entityFile: # for each row in map list
            if self.gridLetter in row: #If the entity is in this row
                secondIndex = row.index(self.gridLetter)   #Store the index of where the entity is in this row
                firstIndex = entityFile.index(row) #Stores the row that the entity is in

        return (firstIndex,secondIndex) #returns the coordinates of the entity as a tuple


    def findEntityInDirection(self,direction,entityFile,entityList):
        (yValue, xValue) = self.findSelf(entityFile)  # unpacks the tuple into 2 values to be used as Y x coordinates in 2d list

        if direction == "Right": #If entity is right of player
            gridLetter = entityFile[yValue][xValue+1] #gridLetter is the element to the right of player

        if direction == "Left": #If entity is left of player
            gridLetter = entityFile[yValue][xValue-1] #gridLetter is the element to the left of player

        if direction == "Up": #If entity is Up of player
            gridLetter = entityFile[yValue-1][xValue] #gridLetter is the element to the Up of player

        if direction == "Down": #If entity is Down of player
            gridLetter = entityFile[yValue+1][xValue] #gridLetter is the element to the Down of player

        for i in entityList: #for each object in the entity list
            if i.gridLetter == gridLetter: #if the grid letter corresponds to that object's grid letter
                return i #return that object


    def move(self,direction,entityFile,mapFile):
        #Play animation of moving here, add this code when created animations
        (yValue, xValue) = self.findSelf(entityFile)  # unpacks the tuple into 2 values to be used as Y x coordinates in 2d list

        if direction == "Right":
            if (mapFile[yValue][xValue+1] == "m") or (entityFile[yValue][xValue+1] != "."):
                #There is a wall or an entity stopping the player from moving
                Constants.soundEffects.play(Constants.failSound)
                print("Cant move") #Debugger code for later to replace with sound

            else:
                entityFile[yValue][xValue+1] = self.gridLetter #Make new position reflect changes
                entityFile[yValue][xValue] = "." #make old position show nothing there now

        elif direction == "Left":
            if (mapFile[yValue][xValue - 1] == "m") or (entityFile[yValue][xValue - 1] != "."):

                Constants.soundEffects.play(Constants.failSound)
                print("Cant move")

            else:
                entityFile[yValue][xValue - 1] = self.gridLetter
                entityFile[yValue][xValue] = "."

        elif direction == "Up":
            if (mapFile[yValue-1][xValue] == "m") or (entityFile[yValue-1][xValue] != "."):

                Constants.soundEffects.play(Constants.failSound)
                print("Cant move")


            else:
                entityFile[yValue-1][xValue] = self.gridLetter
                entityFile[yValue][xValue] = "."

        elif direction == "Down":
            if (mapFile[yValue + 1][xValue] == "m") or (entityFile[yValue + 1][xValue] != "."):

                Constants.soundEffects.play(Constants.failSound)
                print("Cant move")


            else:
                entityFile[yValue + 1][xValue] = self.gridLetter
                entityFile[yValue][xValue] = "."
        
        return entityFile


    def attack(self, direction, entityFile,entityList):
        (yValue, xValue) = self.findSelf(entityFile)  # unpacks the tuple into 2 values to be used as Y x coordinates in 2d list

        if direction == "Right":
            if entityFile[yValue][xValue+1] != ".": #If there is an entity here
                enemy = self.findEntityInDirection(direction, entityFile, entityList) #checks which enemy is in that position
                enemy.health = enemy.health - self.strength # damages enemies health


        if direction == "Left":
            if entityFile[yValue][xValue-1] != ".":
                enemy = self.findEntityInDirection(direction, entityFile, entityList)
                enemy.health = enemy.health - self.strength


        if direction == "Up":
            if entityFile[yValue-1][xValue] != ".":
                enemy = self.findEntityInDirection(direction, entityFile, entityList)
                enemy.health = enemy.health - self.strength


        if direction == "Down":
            if entityFile[yValue+1][xValue] != ".":
                print(entityFile[yValue+1][xValue])
                enemy = self.findEntityInDirection(direction, entityFile, entityList)
                enemy.health = enemy.health - self.strength





class player(entity):
    def __init__(self,health,strength,gridLetter,pictureFile,heldItem,heldWeapon):
        super().__init__(health, strength, gridLetter, pictureFile) #inherits all methods and attributes of entity parent class
        self.heldItem = heldItem #heldItem will be a class that will hold the function of the item, for example, increase the strength or restore health
        self.heldWeapon = heldWeapon #The heldWeapon will be a class of weapon, which will hold the weapon's name, picture and damage modifier.
        self.maxHealth = health # This will be the maximum health that the player has at the start, this will be used for when the items restore the player's health

    def attack(self, direction, entityFile,entityList):
        (yValue, xValue) = self.findSelf(entityFile)  # unpacks the tuple into 2 values to be used as Y x coordinates in 2d list
        # Music
        if not Constants.soundEffects.get_busy(): #If there isn't already a sound effect playing
            Constants.soundEffects.play(Constants.attackSound)
        pygame.mixer.music.load("InGameMusic.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
        if direction == "Right":
            if entityFile[yValue][xValue+1] != ".": #If there is an entity here
                enemy = self.findEntityInDirection(direction, entityFile, entityList) #checks which enemy is in that position
                enemy.health = enemy.health - (self.strength + self.heldWeapon.damage) # damages enemies health
                time.sleep(2) #Wait for old sound effect to end
                Constants.soundEffects.play(Constants.hitSound)

        if direction == "Left":
            if entityFile[yValue][xValue-1] != ".":
                enemy = self.findEntityInDirection(direction, entityFile, entityList)
                enemy.health = enemy.health - (self.strength + self.heldWeapon.damage)
                time.sleep(2) #Wait for old sound effect to end
                Constants.soundEffects.play(Constants.hitSound)

        if direction == "Up":
            if entityFile[yValue-1][xValue] != ".":
                enemy = self.findEntityInDirection(direction, entityFile, entityList)
                enemy.health = enemy.health - (self.strength + self.heldWeapon.damage)
                time.sleep(2) #Wait for old sound effect to end
                Constants.soundEffects.play(Constants.hitSound)

        if direction == "Down":
            if entityFile[yValue+1][xValue] != ".":
                enemy = self.findEntityInDirection(direction, entityFile, entityList)
                enemy.health = enemy.health - (self.strength + self.heldWeapon.damage)
                time.sleep(2) #Wait for old sound effect to end
                Constants.soundEffects.play(Constants.hitSound)

class enemy(entity):
    def __init__(self,health,strength,gridLetter,pictureFile):
        super().__init__(health, strength, gridLetter, pictureFile) #inherits all methods and attributes of entity parent class

    def enemyAttackSequence(self,entityFile,entityList,mapFile):

        (yValue, xValue) = self.findSelf(entityFile)  # unpacks the tuple into 2 values to be used as Y x coordinates in 2d list

        if entityFile[yValue][xValue + 1] == entityList[0].gridLetter: #If to the right of the enemy is the player
            self.attack("Right",entityFile,entityList) #attack the player to the right

        elif entityFile[yValue][xValue - 1] == entityList[0].gridLetter: #If to the left of the enemy is the player
            self.attack("Left",entityFile,entityList)

        elif entityFile[yValue-1][xValue] == entityList[0].gridLetter: #If up of the enemy is the player
            self.attack("Up",entityFile,entityList)

        elif entityFile[yValue+1][xValue] == entityList[0].gridLetter: #If down of the enemy is the player
            self.attack("Down",entityFile,entityList)

        else: #If cannot attack player
            (yValuePlayer, xValuePlayer) = entityList[0].findSelf(entityFile) # Save x and y values of player

            possibleMoves = []

            if (xValuePlayer > xValue) and (mapFile[yValue][xValue + 1] != "m"): #If Player x value to right of enemy
                possibleMoves.append("Right") #Add moving to right to possible good moves

            if (xValuePlayer < xValue) and (mapFile[yValue][xValue - 1] != "m"): #If player x value to left of enemy
                possibleMoves.append("Left")

            if (yValuePlayer < yValue) and (mapFile[yValue-1][xValue] != "m"): #If Player is y value above enemy
                possibleMoves.append("Up")

            if (yValuePlayer > yValue) and (mapFile[yValue+1][xValue] != "m"): # If player is y value below enemy
                possibleMoves.append("Down")

            if possibleMoves == []: #If can't move towards player
                if mapFile[yValue][xValue + 1] != "m":  # If no wall to right
                    possibleMoves.append("Right")  # Add moving to right to possible good moves

                if mapFile[yValue][xValue - 1] != "m":  # If no wall to left of enemy
                    possibleMoves.append("Left")

                if mapFile[yValue - 1][xValue] != "m":  # no wall above enemy
                    possibleMoves.append("Up")

                if mapFile[yValue + 1][xValue] != "m":  # If no wall below enemy
                    possibleMoves.append("Down")

            self.move(random.choice(possibleMoves), entityFile,mapFile) #Randomise through the good possible moves as a way to move for the enemy

class weapon():
    def __init__(self,name,damage, pictureFile):
        self.name = name
        self.damage = damage
        self.pictureFile = pictureFile


class inputBox:

    def __init__(self, x, y, w, h, text, hideText):
        self.rect = pygame.Rect(x, y, w, h) #Rectangle of Text
        self.colour = Constants.BLACK
        self.text = text
        self.hideText = hideText
        if hideText == True:
            self.shownText = ""
            for i in range(len(self.text)):
                self.shownText = self.shownText + "*"
        else:
            self.shownText = self.text

        self.txtSurface = Constants.FONTFORPLAYERDETAILS.render(self.shownText, True, self.colour) #Text font
        self.active = False


    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            if self.active:
                self.colour = Constants.WHITE

            else:
                self.colour = Constants.BLACK
            self.txtSurface = Constants.FONTFORPLAYERDETAILS.render(self.shownText, True, self.colour)


        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN: # Enter data
                    #This is where the function checking the validation etc will be
                    print("Enter pressed")
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text)<30: #Check if text is too long and would go off screen, if it is not too large, add input
                        self.text += event.unicode
                # Re-render the text.
                if self.hideText == True:
                    self.shownText = "*"*len(self.text)

                else:
                    self.shownText = self.text

                self.txtSurface = Constants.FONTFORPLAYERDETAILS.render(self.shownText, True, self.colour)


    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txtSurface.get_width()+10)
        self.rect.w = width


    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txtSurface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)

class mapMaker():
    def placeWalls(map):
        for i in range(len(map[0])): #For the sides of rooms
            map[0][i-1] = "m" #Makes the left sides a wall
            map[-1][i-1] = "m" #makes the right sides a wall

        for i in range(len(map[0])): #For the tops and bottom
            map[i-1][0] = "m" #for the top
            map[i-1][-1] = "m" # for the bottom


        wallChance = 0.2

        for i in range(len(map)): #Column
            for j in range(len(map[0])): #row
                if map[i-1][j-1] != ".": #If the square is not empty
                    print("Square is not empty!")
                    continue
                else:
                    if map[i-2][j-1] == "m": #If behind it is a wall
                        wallChance = wallChance + 0.15
                    if map[i-1][j-2] == "m": #if above it is a wall
                        wallChance = wallChance + 0.15
                    print(wallChance)
                    randomiser = random.randint(0,100)
                    print(randomiser)
                    if randomiser < (wallChance*100):
                        map[i-1][j-1] = "m"
                    wallChance = 0.2
        return map

    def placeEnemies(map, difficulty):
        numAmountEnemies = random.randint(1, 5) #randomises amount of enemies to place
        arrayOfEnemies = [] #list of enemies created
        for i in range(numAmountEnemies):
            if difficulty > 1: #make sure enough difficulty to make full enemy

                possibleSpacesY = [] #Saves the possible spaces on the line
                possibleSpacesX = []
                for k in range(1,len(map)-2):#Since do not want to include ends as they will definitely be fully blocked by walls
                    for j in map[k]:
                        if j == ".": #If empty space
                            possibleSpacesY.append(k)
                            possibleSpacesX.append(map[k].index(j))

                if difficulty >= 5:
                    strength = random.randint(1,4) #1-4 so 1 always left for health
                    difficulty = difficulty - strength

                else:
                    strength = random.randint(1,difficulty-1)
                    difficulty = difficulty - strength

                if difficulty >= 5:
                    health = random.randint(1,5)
                    difficulty = difficulty - health

                else:
                    health = random.randint(1,difficulty)
                    difficulty = difficulty - health

                enemyPics = ["Demon.png"] #possible pics for enemy generator to choose from
                possibleLetters = "abcdefghijklnopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWXYZ!+_-[],.<>?:@~#;" #possible gridletters
                newEnemy = enemy(health, strength, random.choice(possibleLetters), random.choice(enemyPics))
                yCoordinate = random.choice(possibleSpacesY)

                map[yCoordinate][possibleSpacesX[possibleSpacesY.index(yCoordinate)]] = newEnemy.gridLetter
                arrayOfEnemies.append(newEnemy)

        return (arrayOfEnemies, map) #returns the list of new enemies and the new altered map as a tuple to be unpacked

    def createEnemy(difficulty):
        enemyArray = []
        enemyGridLetters = ["g","c"]
        for i in range(2):
            if difficulty > 1:  # make sure enough difficulty to make full enemy
                if difficulty >= 5:
                    strength = random.randint(1, 4)  # 1-4 so 1 always left for health
                    difficulty = difficulty - strength

                else:
                    strength = random.randint(1, difficulty - 1)
                    difficulty = difficulty - strength

                if difficulty >= 5:
                    health = random.randint(1, 5)
                    difficulty = difficulty - health

                else:
                    health = random.randint(1, difficulty)
                    difficulty = difficulty - health

                enemyPics = ["Demon.png"]  # possible pics for enemy generator to choose from
                enemyGrid = random.choice(enemyGridLetters)
                enemyGridLetters.remove(enemyGrid)
                newEnemy = enemy(health, strength, enemyGrid, random.choice(enemyPics))
                enemyArray.append(newEnemy)
        return enemyArray





