import pygame_gui
import pygame, Constants


def textFormat(message, textFont, textSize, textColor):
    newText = textFont.render(message, 0, textColor) # draw text to the screen

    return newText

def startFunction():
    print("Starting game")

def quitFunction():
    pygame.quit()
    quit()

class option:
    def __init__(self,text,functionOfOption):
        self.text = text
        self.textFormat = textFormat(text.upper(), Constants.FONTFORPLAYERDETAILS, 75, Constants.BLACK) # What the text will look like
        self.rectangle = self.textFormat.get_rect()
        self.functionofOption = functionOfOption  # What will happen when enter pressed on the option

# Main Menu
def mainMenu(screen,clock):
    menu = True
    Start = option("Start",startFunction)
    Quit = option("Quit",quitFunction)

    optionSelected = "Start" #What default option is first selected by the user
    optionsClasses = [Start,Quit] #All the possible options on the screen
    options = []
    for i in optionsClasses:
        options.append(i.text) #Create list of strings of the possible options.

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and optionSelected != optionSelected[0]:
                    optionSelected = options[options.index(optionSelected) - 1] #Move up one option

                elif event.key == pygame.K_DOWN and optionSelected != optionSelected[-1]:
                    optionSelected = options[options.index(optionSelected) + 1].text #Move down one option

                if event.key == pygame.K_RETURN:
                    optionsClasses[options.index(optionSelected)].functionofOption() #Do the function of the selected option

        # Main Menu UI
        screen.fill(Constants.BLUE)
        title = textFormat("Title", Constants.FONTFORPLAYERDETAILS, 90, Constants.GREEN)

        for i in optionsClasses:
            if optionSelected == i.text:
                i.textFormat = textFormat(i.text.upper(), Constants.FONTFORPLAYERDETAILS, 75, Constants.WHITE)
            else:
                i.textFormat = textFormat(i.text.upper(), Constants.FONTFORPLAYERDETAILS, 75, Constants.BLACK)

        titleRect = title.get_rect()

        # Main Menu Text
        screen.blit(title, (Constants.sizeOfWindow(0) / 2 - (titleRect(2) / 2), 80))

        for i in optionsClasses:
            screen.blit(i.text, (Constants.sizeOfWindow(0) / 2 - (i.rectangle(2) / 2), 300))

        pygame.display.update()
        clock.tick(60)