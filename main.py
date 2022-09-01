import pygame, random, screenClass, widget, character, database
pygame.init()

## Set the width and height of the screen
SCREENWIDTH = SCREENHEIGHT = 950
## Initialise the window
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
## Create the game clock
clock = pygame.time.Clock()
## Set the title of the window
pygame.display.set_caption("Maze Game")

## Create the font for the game
textFont = pygame.font.Font("Fonts/font.ttf", 75)

## Set the inital values of the game settings
numRounds = 1
computerDifficulty = 5
mazeDifficulty = 5
playerScore = computerScore = 0
winnerName = ""

## Connect to the database
databaseFile = "highscores.db"
dbConnection = database.createDatabase(databaseFile)

## Create a group to hold the screens and maze screens
mazeScreens = pygame.sprite.Group()
screens = pygame.sprite.Group()
## Add all screens to the group
screens.add(screenClass.Screen((145, 145, 145), [widget.Button(270, 25, "Maze Game", (0, 0, 0), (145, 145, 145), 75, 0, True),
                                                 widget.Button(310, 275, "Play Game", (0, 0, 0), (180, 180, 180), 60, 1),
                                                 widget.Button(275, 400, "High Scores", (0, 0, 0), (180, 180, 180), 60, 3),
                                                 widget.Button(400, 525, "Help", (0, 0, 0), (180, 180, 180), 60, 2),
                                                 widget.Button(425, 825, "Quit", (0, 0, 0), (180, 180, 180), 40, -1)], [], []),
            screenClass.Screen((145, 145, 145), [widget.Button(250, 25, "Game Settings", (0, 0, 0), (145, 145, 145), 65, 1, True),
                                                 widget.Button(10, 850, "Start Single Round", (0, 0, 0), (180, 180, 180), 38, 19),
                                                 widget.Button(460, 850, "Start Multiple Rounds", (0, 0, 0), (180, 180, 180), 38, 20),
                                                 widget.Button(10, 150, "Maze Difficulty:", (0, 0, 0), (145, 145, 145), 40, 1, True),
                                                 widget.Button(10, 350, "Computer Difficulty:", (0, 0, 0), (145, 145, 145), 40, 1, True),
                                                 widget.Button(10, 550, "Number of Rounds:", (0, 0, 0), (145, 145, 145), 40, 1, True),
                                                 widget.Button(10, 10, "Back", (0, 0, 0), (180, 180, 180), 35, 0)],
                                                [widget.Slider(50, 225, 600, 50, 0, 20, mazeDifficulty, "mazeDifficulty", (145, 145, 145), (0, 0, 0), (0, 0, 255), (0, 0, 0)),
                                                 widget.Slider(50, 425, 600, 50, 0, 20, computerDifficulty, "computerDifficulty", (145, 145, 145), (0, 0, 0), (0, 0, 255), (0, 0, 0)),
                                                 widget.Slider(50, 625, 600, 50, 1, 5, numRounds, "numRounds", (145, 145, 145), (0, 0, 0), (0, 0, 255), (0, 0, 0))], []),
            screenClass.Screen((145, 145, 145), [widget.Button(10, 10, "Back", (0, 0, 0), (180, 180, 180), 35, 0),
                                                 widget.Button(SCREENWIDTH/2-95, 25, "Help", (0, 0, 0), (145, 145, 145), 75, 2, True),
                                                 widget.Button(SCREENWIDTH/2-250, 200, "Welcome to the Maze Game!", (0, 0, 0), (145, 145, 145), 35, 2, True),
                                                 widget.Button(30, 350, "In this game, you must race through a randomly generated maze against a computer.", (0, 0, 0), (145, 145, 145), 19, 2, True),
                                                 widget.Button(SCREENWIDTH/2-350, 450, "You can change the difficulty of the maze and the computer,", (0, 0, 0), (145, 145, 145), 20, 2, True),
                                                 widget.Button(SCREENWIDTH/2-295, 500, "and choose whether you play a single round or many.", (0, 0, 0), (145, 145, 145), 20, 2, True),
                                                 widget.Button(SCREENWIDTH/2-260, 650, "You are the blue square, the computer is red.", (0, 0, 0), (145, 145, 145), 20, 2, True),
                                                 widget.Button(SCREENWIDTH/2-175, 700, "Race to the finish flag to win.", (0, 0, 0), (145, 145, 145), 20, 2, True),
                                                 widget.Button(SCREENWIDTH/2-100, 850, "Good Luck!", (0, 0, 0), (145, 145, 145), 35, 2, True)], [], []))

def updateHighScores():
    ## Add the correct data to the high score screens

    ## Create the high score screens
    for i in range(5):
        screens.add(screenClass.Screen((145, 145, 145), [widget.Button(10, 10, "Back", (0, 0, 0), (180, 180, 180), 30, 0),
                                                         widget.Button(SCREENWIDTH/2-260, 25, "High Scores", (0, 0, 0), (145, 145, 145), 75, i+3, True),
                                                         widget.Button(205, 170, "Name", (0, 0, 0), (145, 145, 145), 30, i+3, True),
                                                         widget.Button(375, 170, "Round Number", (0, 0, 0), (145, 145, 145), 30, i+3, True),
                                                         widget.Button(650, 170, "Score", (0, 0, 0), (145, 145, 145), 30, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(3/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(4/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(5/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(6/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(7/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(8/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(9/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(10/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(11/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(200, SCREENHEIGHT*(12/13), " "*35, (0, 0, 0), (180, 180, 180), 25, i+3, True),
                                                         widget.Button(10, 380, "Sort by:", (0, 0, 0), (145, 145, 145), 30, i+3, True),
                                                         widget.Button(25, 440, "Score", (0, 0, 0), (180, 180, 180), 30, (i+3)-1 if (i+3) % 2 == 0 else (i+3)),
                                                         widget.Button(25, 500, "Round", (0, 0, 0), (180, 180, 180), 30, int(round((i+3)/2, 0)*2) if i != 4 else 7),
                                                         widget.Button(16, 537, "Number", (0, 0, 0), (180, 180, 180), 30, int(round((i+3)/2,0)*2) if i != 4 else 7),
                                                         widget.Button(790, 320, "Single", (0, 0, 0), (180, 180, 180), 30, 7),
                                                         widget.Button(800, 357, "Round", (0, 0, 0), (180, 180, 180), 30, 7),
                                                         widget.Button(773, 457, "Multiple", (0, 0, 0), (180, 180, 180), 30, 5 if i != 3 else 6),
                                                         widget.Button(800, 494, "Round", (0, 0, 0), (180, 180, 180), 30, 5 if i != 3 else 6),
                                                         widget.Button(818, 594, "All", (0, 0, 0), (180, 180, 180), 30, (i%2)+3)], [], []))

    allScores = database.getScoreTable(dbConnection)
    for i in range(5):
        for j in range(len(allScores[i])):
            currentButton = screens.sprites()[i+3].buttons.sprites()[j+5]
            newText = [" " for x in range(35)]

            ## Add the name to the new text
            for k in range(len(allScores[i][j][0])):
                newText[k] = allScores[i][j][0][k]

            ## Add the score to the new text
            scoreLength = len(str(allScores[i][j][1]))
            for k in range(scoreLength):
                newText[35-scoreLength+k] = str(allScores[i][j][1])[k]

            ## Add the number of rounds to the new text
            newText[18] = str(allScores[i][j][3])

            ## Join all the text into one string and
            ## set it to the text of the specific highscore
            currentButton.text = "".join(newText)
            currentButton.updateButton()

## Update all the high score displays
updateHighScores()

currentScreen = pygame.sprite.GroupSingle()
## Set currentScreen to the first element of screens
currentScreen.add(screens.sprites()[0])

## Create the players group
players = pygame.sprite.Group()

carryOn = playing = True
counter = 0

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   ## If the 'X' is clicked
            carryOn = False             ## Tell the program to quit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()   ## Get the position of the mouse
            for button in currentScreen.sprite.buttons.sprites():  ## Check every button in the currentScreen
                if button.isClicked(mousex, mousey):      ## If the button has been clicked
                    if button.goTo == -1:
                        carryOn = False
                    elif button.goTo == 20:   ## Multiple round mode has started
                    	## Reset the maze screens group
                        mazeScreens.empty()
                        for i in range(8, len(screens.sprites())):
                            screens.remove(screens.sprites()[i])
                        playerScore = computerScore = 0
                        
                        ## Generate all the mazes
                        currentRound = 0
                        for i in range(numRounds):
                            mazeScreens.add(screenClass.MazeScreen((185, 185, 185), (0, 0, 0), mazeDifficulty))

                        ## Move the screen to the first maze
                        currentScreen.add(mazeScreens.sprites()[0])
                        gamemode = "multiple"
                    elif button.goTo == 19:    ## Single round mode has started
                    	## Reset the maze screens group
                        mazeScreens.empty()
                        for i in range(8, len(screens.sprites())):
                            screens.remove(screens.sprites()[i])
                        playerScore = computerScore = 0
                        
                        ## Generate a maze
                        mazeScreens.add(screenClass.MazeScreen((185, 185, 185), (0, 0, 0), mazeDifficulty))
                        numRounds = 1

                        ## Move the screen to the maze
                        currentScreen.add(mazeScreens.sprites()[0])
                        gamemode = "single"
                    else:
                        currentScreen.add(screens.sprites()[button.goTo])  ## Change currentScreen to the new index
            ## Check if any slider has been clicked
            for slider in currentScreen.sprite.sliders.sprites():
                slider.isClicked(mousex, mousey)
            ## Check if any textbox has been clicked
            for textBox in currentScreen.sprite.textBoxes.sprites():
                textBox.active = textBox.isBoxClicked(mousex, mousey)
                if textBox.isButtonClicked(mousex, mousey):
                    winnerName = textBox.getText(mousex, mousey)

                    ## Save the game if the 'Enter' button is pressed
                    ## Add the score to the database
                    database.addItem(dbConnection, winnerName, playerScore, gamemode, numRounds)
                    updateHighScores()
                    ## Move back to the start-up screen
                    currentScreen.add(screens.sprites()[0])
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = pygame.mouse.get_pos()
            ## Check all sliders
            for slider in currentScreen.sprite.sliders.sprites():
                if slider.active:
                    ## Change the value of a slider if it is active
                    slider.changeValue(mousex)
                    ## Change the variable which the slider is linked to
                    globals()[slider.setting] = slider.getValue()
            for button in currentScreen.sprite.buttons.sprites():
                ## Set a button to active if the mouse is over it
                button.setActive(button.isClicked(mousex, mousey))
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = pygame.mouse.get_pos()
            ## Set all sliders to not active when the mouse is released
            for slider in currentScreen.sprite.sliders.sprites():
                slider.active = False
        elif event.type == pygame.KEYDOWN:
            ## Move the player if they are currently playing a game
            if currentScreen.sprite.__class__.__name__ == "MazeScreen" and playing:
                currentScreen.sprite.moveUser(event.key, player)
            else:
                ## Add text to any active textboxes
                for textBox in currentScreen.sprite.textBoxes.sprites():
                    if textBox.active:
                        textBox.addText(event.key)

    if currentScreen.sprite.__class__.__name__ == "MazeScreen":
        if not currentScreen.sprite.generated:
            playing = True

            ## Generate a new maze
            currentScreen.sprite.generateMaze(SCREENWIDTH, SCREENHEIGHT)
            numCells = len(currentScreen.sprite.cells) ** 0.5

            ## Generate random co-ordinates for the player and computer
            playerCoords = (random.randint(0, numCells-1), random.randint(0, numCells-1))
            computerCoords = (random.randint(0, numCells-1), random.randint(0, numCells-1))

            ## Create the player and computer
            player = character.Character(playerCoords[0], playerCoords[1], currentScreen.sprite.cellWidth, (0, 0, 255))
            computer = character.Character(computerCoords[0], computerCoords[1], currentScreen.sprite.cellWidth, (255, 0, 0))

            ## Generate the finish and the computer's path
            finish = currentScreen.sprite.getFinish(player, computer)
            currentScreen.sprite.computerPath = currentScreen.sprite.aStar((computer.gridX, computer.gridY), finish)

            ## Check if the length to the finish is greater than 10
            while len(currentScreen.sprite.computerPath) < 10:
                ## Generate random co-ordinates for the player and computer
                playerCoords = (random.randint(0, numCells-1), random.randint(0, numCells-1))
                computerCoords = (random.randint(0, numCells-1), random.randint(0, numCells-1))

                ## Create the player and computer
                player = character.Character(playerCoords[0], playerCoords[1], currentScreen.sprite.cellWidth, (0, 0, 255))
                computer = character.Character(computerCoords[0], computerCoords[1], currentScreen.sprite.cellWidth, (255, 0, 0))

                ## Generate the finish and the computer's path
                finish = currentScreen.sprite.getFinish(player, computer)
                currentScreen.sprite.computerPath = currentScreen.sprite.aStar((computer.gridX, computer.gridY), finish)
            players.add(player, computer)

            ## Adjust for maze offset
            player.rect.x += currentScreen.sprite.offset+1
            player.rect.y += currentScreen.sprite.offset+1
            computer.rect.x += currentScreen.sprite.offset+1
            computer.rect.y += currentScreen.sprite.offset+1
        else:
            ## Draw the finish
            if playing:
                cellWidth = currentScreen.sprite.cellWidth
                offset = currentScreen.sprite.offset

                ## Fill the background of the finish black
                pygame.draw.rect(screen, (0, 0, 0),
                                (finish[0]*cellWidth+offset+1,
                                 finish[1]*cellWidth+offset+1,
                                 cellWidth-1, cellWidth-1))

                ## Draw small white squares on top
                for i in range(0, 5):
                    if i % 2 == 0:
                        for j in range(1, 5, 2):
                            pygame.draw.rect(screen, (255, 255, 255),
                                             ((finish[0]*cellWidth+j*cellWidth/5)+offset+1, (finish[1]*cellWidth+i*cellWidth/5)+offset+1, cellWidth/5, cellWidth/5))
                    else:
                        for j in range(0, 5, 2):
                            pygame.draw.rect(screen, (255, 255, 255),
                                             ((finish[0]*cellWidth+j*cellWidth/5)+offset+1, (finish[1]*cellWidth+i*cellWidth/5)+offset+1, cellWidth/5, cellWidth/5))

            if not playing:
                ## Display the winner text if the game ended
                screen.blit(winnerText, (SCREENWIDTH/2 - winnerText.get_width()/2, 100))
                screen.blit(playerScoreText, (SCREENWIDTH/2 - playerScoreText.get_width()/2, 250))
                screen.blit(computerScoreText, (SCREENWIDTH/2 - computerScoreText.get_width()/2, 400))
                screen.blit(enterNameText, (SCREENWIDTH/2 - 400, 650))
            elif counter % (60 - computerDifficulty*2) == 0:
                ## Move the computer
                currentScreen.sprite.moveComputer(computer)

            ## Check if there is a winner
            winner = currentScreen.sprite.getWinner(player, computer, finish)
            if winner != False and playing:
                if winner == "player":
                    ## Calculate the player's score
                    score = 10 * len(currentScreen.sprite.computerPath) + 100
                    playerScore += score

                    ## Render the winner text
                    winnerText = textFont.render("Player Wins!", False, (0, 0, 0))
                elif winner == "computer":
                    ## Calculate the best path from the player to the finish
                    playerPath = currentScreen.sprite.aStar((player.gridX, player.gridY), finish)
                    ## Calculate the computer's score
                    score = 10 * (len(playerPath) - 1) + 100
                    computerScore += score

                    ## Render the winner text
                    winnerText = textFont.render("Computer Wins!", False, (0, 0, 0))

                ## Render the text to show the players' scores
                playerScoreText = textFont.render("Player Score : " + str(playerScore), False, (0, 0, 0))
                computerScoreText = textFont.render("Computer Score : " + str(computerScore), False, (0, 0, 0))
                enterNameText = textFont.render("", False, (0, 0, 0))


                if playing:
                    ## Create a text box if the full game has finished and the player has won
                    if (gamemode == "single" or (gamemode == "multiple" and mazeScreens.sprites().index(currentScreen.sprite) == numRounds-1)) and winner == "player":
                        enterNameText = textFont.render("Enter your name :", False, (0, 0, 0))
                        currentScreen.sprite.textBoxes.add(widget.Textbox(SCREENWIDTH/2-400, 750, 800, 120, (140, 140, 140), (180, 180, 180), (0, 0, 0), 75))
                    ## Create a back button if the player lost
                    elif (gamemode == "single" or (gamemode == "multiple" and mazeScreens.sprites().index(currentScreen.sprite) == numRounds-1)) and winner == "computer":
                        currentScreen.sprite.buttons.add(widget.Button(SCREENWIDTH/2-100, 650, "Back", (0, 0, 0), (140, 140, 140), 85, 0))
                    else:
                        ## Otherwise move onto the next maze
                        currentRound += 1
                        screens.add(mazeScreens.sprites()[currentRound])

                        ## Create a button to move to the next game
                        currentScreen.sprite.buttons.add(widget.Button(SCREENWIDTH/2-220, 650, "Next Round", (0, 0, 0), (140, 140, 140), 85, currentRound+7))
                ## Finish playing the game and delete the players
                playing = False
                players.empty()

    pygame.display.flip()  ## Update the display
    clock.tick(60)
    counter += 1

    ## Draw the screen
    currentScreen.draw(screen)

    ## Draw the widgets and players
    currentScreen.sprite.buttons.draw(screen)
    currentScreen.sprite.sliders.draw(screen)
    currentScreen.sprite.textBoxes.draw(screen)
    players.draw(screen)

## Close the database and quit Pygame
database.closeDatabase(dbConnection)
pygame.quit()
