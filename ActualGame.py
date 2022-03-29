# Import the pygame library and initialise the game engine
import pygame, Constants, Classes
import GridMaker
import pygame_gui
import mysql.connector


entityList = [] #this will be a list of all the objects of entities that are alive right now in the game
turnCounter = 1
pygame.init()

# Open a new window
screen = pygame.display.set_mode(Constants.sizeOfWindow) # Makes window the size specified
screen.fill(Constants.WHITE)  # Set background to be white

pygame.display.set_caption("2D Game") #Set name of window

# The loop will carry on until the user clicks the close button).
keepPlaying = True

# The clock uses the inbuilt clock in pygame to control how fast the screen updates
clock = pygame.time.Clock()

# Main Program Loop
def realGame(screen, entityList, turnCounter,difficulty):
    keepPlaying = True
    screen.fill(Constants.WHITE)
    worldMap = GridMaker.readMap(Constants.MAPFILE) #read level map
    entityMap = GridMaker.readMap(Constants.ENTITYFILE) # read entity map
    worldMap = Classes.mapMaker.placeWalls(worldMap)


    print(worldMap)
    sword = Classes.weapon("Longsword",2,"picture.png")
    player = Classes.player(10,10,"x","Knight.png","hello",sword) # Create object called player with 10 health, 10 strength, x as gridletter and G.png as pic
    entityList.append(player)
    #enemy = Classes.enemy(20,1,"g","Demon.png") #create enemy with gridletter as g
    #entityList.append(enemy)
    #enemy2 = Classes.enemy(30,2,"c","Demon.png")
    #entityList.append(enemy2)

    entityList = entityList + Classes.mapMaker.createEnemy(5)


    #(newEnemies, entityMap) = Classes.mapMaker.placeEnemies(worldMap,5)
    #entityList = entityList + newEnemies
    print(entityList)
    #Music
    pygame.mixer.music.load("InGameMusic.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    ##Text rendering
    text = Constants.FONTFORPLAYERDETAILS.render("Turn: " + str(turnCounter), True, Constants.BLACK) #Create with my font text saying Turn: 1 etc. In black.
    screen.blit(text, (Constants.playerDetailsX, Constants.playerDetailsY)) #renders text to screen

    #Hearts rendering
    heartPicPositionAffect = 0  # This is the how many pixels away from the original heart the heart will be drawn, this will make them be sequential
    for i in range(player.health):
        screen.blit(Constants.heartPicSmall,(Constants.heartX + heartPicPositionAffect, Constants.heartY))  # renders picture to screen
        heartPicPositionAffect += (Constants.heartX * 3 / 2)  # Move heartPositionAffect to be the size of the height from the edge plus a half of it more.

    GridMaker.drawMap(screen,worldMap,entityList, False) # Create map
    print(entityMap)
    print(worldMap)
    #newMap = GridMaker.worldMapCleaner(worldMap)
    allowedKeys = [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_SPACE,pygame.K_e]
    itemUsed = False
    while keepPlaying:

        for event in pygame.event.get():  # When User does something
            if event.type == pygame.KEYDOWN:
                screen.fill(Constants.WHITE)

                #-----AI Part----#
                if event.key != pygame.K_ESCAPE and event.key in allowedKeys:
                    for i in entityList[1:]: #Starting from the 2nd element, as first element is player
                        i.enemyAttackSequence(entityMap,entityList,worldMap) #Make enemy search for player, move towards them or attack
                       
                    turnCounter += 1  # Add 1 to turn timer as turn has been taken doing action.

                #-----Movement------#
                if event.key == pygame.K_UP: # If user presses up arrow key
                    player.move("Up",entityMap,worldMap) #Try to move up
                elif event.key == pygame.K_DOWN:
                    player.move("Down",entityMap,worldMap)
                elif event.key == pygame.K_LEFT:
                    player.move("Left",entityMap,worldMap)
                elif event.key == pygame.K_RIGHT:
                    player.move("Right",entityMap,worldMap)

                #-----Attacking-----#
                elif event.key == pygame.K_w: # If user presses w key
                    player.attack("Up",entityMap,entityList) #Try to attack upwards
                elif event.key == pygame.K_s:
                    player.attack("Down",entityMap,entityList)
                elif event.key == pygame.K_a:
                    player.attack("Left",entityMap,entityList)
                elif event.key == pygame.K_d:
                    player.attack("Right",entityMap,entityList)

                elif event.key == pygame.K_e and itemUsed == False:
                    player.health = 10
                    itemUsed = True # Can only use item once

                #-------Escaping to main menu------#
                elif event.key == pygame.K_ESCAPE:
                    menu(screen,clock,False,False,False,turnCounter)


                #-----Check if anyone has died

                for i in entityList:

                    if i.health <= 0:
                        if i.gridLetter == player.gridLetter: #If it is the player whose health is less than 0
                            print("Player died")
                            screen.fill(Constants.BLUE)
                            title = Constants.FONTFORPLAYERDETAILS.render("You died, try again?", False, Constants.GREEN)
                            titleRect = title.get_rect()

                            # Main Menu Text
                            screen.blit(title, (Constants.sizeOfWindow[0] / 2 - 200, Constants.sizeOfWindow[1] / 5 - 100))  # Places text at top of screen
                            menu(screen,clock,False,True,False,turnCounter)

                        else:
                            (firstIndex,secondIndex) = i.findSelf(entityMap)
                            #Play entity dying animation
                            entityMap[firstIndex][secondIndex] = "." #replaces enemy's position with normal floor
                            entityList.remove(i)
                            del i #Deletes the instantiated i object


                for i in entityList:
                    print(i.health)


                text = Constants.FONTFORPLAYERDETAILS.render("Turn: " + str(turnCounter), True, Constants.BLACK) #Create with my font text saying Turn: 1 etc. In black.
                screen.blit(text, (Constants.playerDetailsX, Constants.playerDetailsY)) #renders text to screen

                heartPicPositionAffect = 0 #This is the how many pixels away from the original heart the heart will be drawn, this will make them be sequential
                for i in range(player.health):
                    screen.blit(Constants.heartPicSmall, (Constants.heartX+heartPicPositionAffect, Constants.heartY))  # renders picture to screen
                    heartPicPositionAffect += (Constants.heartX *3/2) #Move heartPositionAffect to be the size of the height from the edge plus a half of it more.

            if event.type == pygame.QUIT:  # If user clicked close
                keepPlaying = False  # keepPlaying = false, ends loop which then ends program

        #print(newMap)
        #GridMaker.drawMap(screen, newMap, entityList, False)
        GridMaker.drawMap(screen, worldMap, entityList, False)
        GridMaker.drawMap(screen,entityMap,entityList, True) #draw entity map second


        # Limit to 60 frames per second
        fps = 60
        clock.tick(fps)
        pygame.display.update() # Update screen to show changes

        if entityList == [player]:
            menu(screen,clock, False,False,True,turnCounter)



# Code for Main menu

def startFunction():
    realGame(screen, [], 1)


def quitFunction():
    pygame.quit()
    quit()

def quitToMenuFunction():
   menu(screen,clock,True,False,False,turnCounter)

class option:
    def __init__(self,text,functionOfOption):
        self.text = text
        self.textFormat = Constants.FONTFORPLAYERDETAILS.render(text.upper(), 0, Constants.BLACK) # What the text will look like
        self.rectangle = self.textFormat.get_rect()
        self.functionofOption = functionOfOption  # What will happen when enter pressed on the option



# Main Menu
def menu(screen,clock,firstTime,dead,win,turnCounter,difficulty):
    menu = True
    start = option("Start",startFunction)
    quitGame = option("Quit",quitFunction)
    login = option("Login", loginMenu)
    resume = option("Resume",startFunction)
    quitToMenu = option("Quit to Main Menu", quitToMenuFunction)
    tryAgain = option("Try Again?",startFunction)

    if firstTime == True:
        optionSelected = start #What default option is first selected by the user
        optionsClasses = [start,login,quitGame] #All the possible options on the screen

    elif dead == True or win==True:
        optionSelected = tryAgain
        optionsClasses = [tryAgain,quitToMenu]
    else:
        optionSelected = resume
        optionsClasses = [resume, quitToMenu]

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: #If user presses a key
                if event.key == pygame.K_UP and optionSelected != optionsClasses[0]: #If tries to go up and not at first option
                    optionSelected = optionsClasses[optionsClasses.index(optionSelected) - 1] #Move up one option

                elif event.key == pygame.K_DOWN and optionSelected != optionsClasses[-1]: #If tries to go down and not at last option
                    optionSelected = optionsClasses[optionsClasses.index(optionSelected) + 1] #Move down one option

                if event.key == pygame.K_RETURN:
                    if optionSelected == resume:
                        screen.fill(Constants.WHITE) #So that bottom part is white
                        return None
                    else:
                        optionSelected.functionofOption() #Do the function of the selected option

        # Main Menu UI
        screen.fill(Constants.BLUE)

        if firstTime == True:
            title = Constants.FONTFORPLAYERDETAILS.render("Dungeon",False, Constants.GREEN)
            titleRect = title.get_rect()

            # Main Menu Text
            screen.blit(title, (Constants.sizeOfWindow[0] / 2 -200, Constants.sizeOfWindow[1] / 5 -100))  # Places title text at top of screen

        elif dead == True:

            title = Constants.FONTFORPLAYERDETAILS.render("You died", False, Constants.GREEN)
            titleRect = title.get_rect()
            # Main Menu Text
            screen.blit(title, (Constants.sizeOfWindow[0] / 2 - 200, Constants.sizeOfWindow[1] / 5 - 100))  # Places text at top of screen

        elif win == True:

            title = Constants.FONTFORPLAYERDETAILS.render("You win!", False, Constants.GREEN)
            titleRect = title.get_rect()
            # Main Menu Text
            screen.blit(title, (Constants.sizeOfWindow[0] / 2 - 200, Constants.sizeOfWindow[1] / 5 - 100))  # Places text at top of screen
            scoreText = Constants.FONTFORPLAYERDETAILS.render("Your score was "+str(10000-turnCounter*50), False, Constants.RED)
            screen.blit(scoreText, (Constants.sizeOfWindow[0] / 2 - 300, Constants.sizeOfWindow[1] / 5 +20))

        for i in optionsClasses:
            if optionSelected == i:
                i.textFormat = Constants.FONTFORPLAYERDETAILS.render(i.text.upper(), False, Constants.WHITE) #Make text white if selected
            else:
                i.textFormat = Constants.FONTFORPLAYERDETAILS.render(i.text.upper(), False, Constants.BLACK) #Make text black if not selected



        for i in optionsClasses:
            screen.blit(i.textFormat, (Constants.sizeOfWindow[0] / 2 - (i.rectangle[2] / 2), (Constants.sizeOfWindow[1] / 3 +(optionsClasses.index(i) * 150)))) #Places each option, using screen measurements to change for screen size

        pygame.display.update()
        clock.tick(60)


def loginMenu():
    usernameBox = Classes.inputBox(100, Constants.sizeOfWindow[1]/4, 140, int(128*Constants.sizeOfWindow[1]/1080), "username", False) #The box where username is entered
    passwordBox = Classes.inputBox(100, Constants.sizeOfWindow[1]*3/4 , 140, int(128*Constants.sizeOfWindow[1]/1080),"Password",True)
    inputBoxes = [usernameBox, passwordBox]
    usernameText = Constants.FONTFORPLAYERDETAILS.render("Username", True, Constants.WHITE)
    passwordText = Constants.FONTFORPLAYERDETAILS.render("Password", True, Constants.WHITE)


    done = False

    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    username = usernameBox.text
                    password = passwordBox.text

                    if len(username) > 3: #More validation will be added later for password
                        print("Username is ok. Checking database for if the data entered is correct")

                        # Connecting to the database
                        connectiondb = mysql.connector.connect(host="localhost", user="root", passwd="3)MEyys{KaUC#yW(sezU",database="Accounts", auth_plugin = "mysql_native_password")
                        cursordb = connectiondb.cursor() #Create the cursor to be able to control the database

                        userVerification = username
                        passVerification = password
                        sql = "select * from UsernamesAndPasswords where username = "+userVerification +" and password = "+passVerification # SQL search
                        cursordb.execute(sql)
                        results = cursordb.fetchall() #Fetch all results from the search
                        if results: #If there are results in table
                            print("User found!")
                            done = True
                            break

                        else:
                            print("User not found! Please try other user")

                    else:
                        print("Please make the username longer than 3 letters")



            for box in inputBoxes:
                box.events(event)

        for box in inputBoxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in inputBoxes:
            box.draw(screen) #Draw every box to screen with text

        screen.blit(usernameText, (usernameBox.rect.x, usernameBox.rect.y - int(128*Constants.sizeOfWindow[1]/1080)))
        screen.blit(passwordText, (passwordBox.rect.x, passwordBox.rect.y - int(128*Constants.sizeOfWindow[1]/1080)))
        pygame.display.update()
        clock.tick(30)






# Once we have exited the main program loop we can stop the game engine:
menu(screen,clock,True,False,False,turnCounter)
#realGame(screen, entityList, turnCounter,keepPlaying)

pygame.quit()