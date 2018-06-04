#__________________________________________
#Date: June 3, 2018
#Developer: Joyce Bacic
#Uses Pygame 
#The tritris.py and tritrisObj.py are both required to play this game
#Tritris game is like Tetris but each piece is made of 3 blocks
#The objective is to accumulate as many points as possible 
#The tritris.py and tritrisObj.py are both required to play this game
#Coded using Python 3.6.4 and Pygame 1.9.3
#_______________________________________________
import pygame
import random 
import tritrisObj
from pygame.locals import *

playing = False
open = True

width = 9
height = 18
extraSpace = 6

playingBoard = []
currentPiece = tritrisObj.Piece()
points = 0
highScore = 0

milsec = 400
waitAfterEvent=150

#-----------------------MAIN METHOD------------------------------------------------------				
def main():
	pygame.init()
	global currentPiece

	screen = pygame.display.set_mode(((width+extraSpace)*tritrisObj.scale, height*tritrisObj.scale))
	
	#--------------------------Display---------------------------------
	buttonFont = pygame.font.SysFont("Arial", 24, True)
	labelFont = pygame.font.SysFont("Arial", 18, True)
	newGame(screen, buttonFont, labelFont)
	
	x=introOK(screen)
	newGame(screen, buttonFont, labelFont)
	
	global open
	global playing
	counter = milsec
	
	while open:
		for evt in pygame.event.get():
			if evt.type == QUIT:
				open = False #checks to see if user clicks on "Exit" button

		#--------start/pause
		if clickedButton() == "s/p":
			playing = True
			pygame.draw.rect(screen, (210,210,25), (10*tritrisObj.scale, 5.5*tritrisObj.scale, 4*tritrisObj.scale, 2*tritrisObj.scale))
			pauseText = buttonFont.render("    Pause", 1, (0,0,0))
			screen.blit(pauseText, (10*tritrisObj.scale, 6*tritrisObj.scale))
			currentPiece.updatePiece(playingBoard)
			update(screen)
			pygame.display.update()

			playing = True

		while playing:
			pygame.time.delay(5)
			counter -= 5 #reduce counter by milliseconds that have passed

#-------------change in game status----------------------------------------------------------
			for evt in pygame.event.get():
				if evt.type == QUIT:
					open = False #checks to see if user clicks on "Exit" button
					playing = False

			#--------start/pause
			if clickedButton() == "s/p":
				playing = False
				pygame.draw.rect(screen, (0,210,25), (10*tritrisObj.scale, 5.5*tritrisObj.scale, 4*tritrisObj.scale, 2*tritrisObj.scale))
				startText = buttonFont.render("     Start", 1, (0,0,0))
				screen.blit(startText, (10*tritrisObj.scale, 6*tritrisObj.scale))

#-------------------piece fall------------------------------------------------------------		

			#--------if milliseconds passed is the given amount will move piece down
			if counter <= 0:
				#----when the piece can still move down		
				if currentPiece.canMoveDown(playingBoard):
					currentPiece.erase(playingBoard)
					currentPiece.moveDown()
					currentPiece.updatePiece(playingBoard)
					update(screen)
					
				#----when the piece can no longer move down	
				else:
					counter = milsec

					#-----check to see if player lost the game
					hasLost = False
					for s in currentPiece.sqrs:
						playingBoard[s[0]][s[1]].empty = False
						if ((s[1]==0)and(s[0]==4 or s[0]==5)):#check if player lost
							lost(screen)
							newGame(screen, buttonFont, labelFont)
							currentPiece = tritrisObj.Piece()
							hasLost = True
							break
				
					#-----calls method to check if there are full rows and sends the array of rows to the deleteRows method
					deleteRows(checkRows(), screen)
					
					#-------------------point lable update 
					pygame.draw.rect(screen, (0,0,0), (9.5*tritrisObj.scale, 1*tritrisObj.scale, 5.5*tritrisObj.scale, 1*tritrisObj.scale))
					pointText = "POINTS "+ str(points)
					pointLabel = labelFont.render(pointText, 1, (255,255,255))
					screen.blit(pointLabel, (9.5*tritrisObj.scale, 1*tritrisObj.scale))
					
					#-----------makes a new piece object
					currentPiece = tritrisObj.Piece()
					currentPiece.updatePiece(playingBoard)
					if (not hasLost): #this will make sure that the new piece is drawn as long as it is not a new game
						update(screen)
						pygame.display.update()
				counter = milsec #reset counter
				
				
#-------------------- code for button or key click to move piece-----------------
			#--------rotate
			if (clickedButton() == "r")or(pressedKey() == "r") :
				counter -= waitAfterEvent #adjust counter for wait
				currentPiece.erase(playingBoard)	
				currentPiece.rotate(playingBoard)
				currentPiece.updatePiece(playingBoard)

				update(screen)

			#-------move left
			elif (clickedButton() == 'L')or(pressedKey() == "L"):
				counter -= waitAfterEvent #adjust counter for wait
				if currentPiece.canMoveLeft(playingBoard):
					currentPiece.erase(playingBoard)	
					currentPiece.moveLeft()
					currentPiece.updatePiece(playingBoard)

				update(screen)

			#-------move right
			elif (clickedButton() == 'R')or(pressedKey() == "R"):
				counter -= waitAfterEvent #adjust counter for wait
				if currentPiece.canMoveRight(playingBoard):
					currentPiece.erase(playingBoard)	
					currentPiece.moveRight()
					currentPiece.updatePiece(playingBoard)

				update(screen)

			#--------speed up
			elif (clickedButton() == "D")or(pressedKey() == "D"):
				counter = 0
				if currentPiece.canMoveDown(playingBoard):
					currentPiece.erase(playingBoard)
					currentPiece.moveDown()
					if currentPiece.canMoveDown(playingBoard):	
						currentPiece.moveDown()
						counter = milsec
					currentPiece.updatePiece(playingBoard)
					
				else:
					break
				

				update(screen)
			pygame.display.update()
			
		
		
	pygame.quit()
	exit()


#-----this method adds buttons and labels to the screen and resets the playing board with empty squares
def drawScreen(screen, buttonFont, labelFont):#clears screen and puts buttons and labels on screen 
	
	#---clears screen
	pygame.draw.rect(screen, (0,0,0), (0,0, (width+extraSpace)*tritrisObj.scale, height*tritrisObj.scale))
	
	#-----------------------making Start/Pause button
	pygame.draw.rect(screen, (0,210,25), (10*tritrisObj.scale, 5.5*tritrisObj.scale, 4*tritrisObj.scale, 2*tritrisObj.scale))
	startText = buttonFont.render("     Start", 1, (0,0,0))
	screen.blit(startText, (10*tritrisObj.scale, 6*tritrisObj.scale))

	#-----------------------making rotate button
	pygame.draw.rect(screen, (244,144,208), (10*tritrisObj.scale, 9*tritrisObj.scale, 4*tritrisObj.scale, 2*tritrisObj.scale))
	rotateText = buttonFont.render("    Rotate", 1, (0,0,0))
	screen.blit(rotateText, (10*tritrisObj.scale, 9.5*tritrisObj.scale))

	#-------------making move left button 
	pygame.draw.rect(screen, (150,25, 184), (10*tritrisObj.scale, 12*tritrisObj.scale, 1.75*tritrisObj.scale, 2*tritrisObj.scale))
	leftText = buttonFont.render("   <", 1, (0,0,0))
	screen.blit(leftText, (10*tritrisObj.scale, 12.5*tritrisObj.scale))

	#--------------making move right button 
	pygame.draw.rect(screen, (255,217,0), (12.25*tritrisObj.scale, 12*tritrisObj.scale, 1.75*tritrisObj.scale, 2*tritrisObj.scale))
	rightText = buttonFont.render("   >", 1, (0,0,0))
	screen.blit(rightText, (12.25*tritrisObj.scale, 12.5*tritrisObj.scale))
	
	#--------------making move down button 
	pygame.draw.rect(screen, (20,217,174), (11*tritrisObj.scale, 14.5*tritrisObj.scale, 2*tritrisObj.scale, 1.75*tritrisObj.scale))
	downText = buttonFont.render("    v", 1, (0,0,0))
	screen.blit(downText, (11*tritrisObj.scale, 14.75*tritrisObj.scale))

	#--------------points label
	pointText = "POINTS "+ str(points)
	pointLabel = labelFont.render(pointText, 1, (255,255,255))
	screen.blit(pointLabel, (9.5*tritrisObj.scale, 1*tritrisObj.scale))
	
	#--------------high score label
	highScoreText = "HIGH SCORE "+ str(highScore)
	highScoreLabel = labelFont.render(highScoreText, 1, (255,255,255))
	screen.blit(highScoreLabel, (9.5*tritrisObj.scale, 2.5*tritrisObj.scale))
	
	
	#-----------------clear and create playingBoard
	playingBoard.clear()
	for i in range(width):
		col = []#----x value
		for j in range (height):
			col.append(tritrisObj.Square(i,j))
		playingBoard.append(col)

#---------------this method is called to display a window to introduce the user to the game 
def introOK(screen):
	#----makes window
	pygame.draw.rect(screen, (5,5,85), (1*tritrisObj.scale, 1*tritrisObj.scale, 13*tritrisObj.scale, 11.5*tritrisObj.scale))
	welcomeText = ["Welcome to TriTris! Here's how to play:", "  - Click the 'Start' button to get pieces to fall", "  - Move these pieces to make full rows of blocks,", "    you get a point and the row disappears", "  - Use the buttons on screen or your arrow keys", "    to move LEFT, RIGHT and DOWN", " - Use the 'Rotate' button and the 'R' key to", "    rotate your piece"]
	introFont  = pygame.font.SysFont("Tahoma", 12, True)
	for i in range (len(welcomeText)):
		text = introFont.render(welcomeText[i], 1, (255,255,255))
		screen.blit(text, (1.2*tritrisObj.scale, (1.5+1*i)*tritrisObj.scale))

	#--- makes ok button 
	pygame.draw.rect(screen, (75,250,70), (9*tritrisObj.scale, 10*tritrisObj.scale, 3.5*tritrisObj.scale, 1.5*tritrisObj.scale))
	welcomeText = "GOT IT!"
	introFont  = pygame.font.SysFont("Tahoma", 20, True)
	text = introFont.render(welcomeText, 1, (0,0,0))
	screen.blit(text, (9.2*tritrisObj.scale, 10.2*tritrisObj.scale))

	pygame.display.update()
	
	#-----game waits for ok button to be pressed
	while True:
		evt = pygame.event.wait()
		if evt.type == QUIT:
			open = False
			break

		if evt.type == MOUSEBUTTONDOWN:
			x, y = evt.pos
	
			#----new game
			if x/tritrisObj.scale >9 and x/tritrisObj.scale <12.5 and y/tritrisObj.scale >10 and y/tritrisObj.scale <11.5:
				break
	
#-----this updates the pieces area (that displays on the left side of the screen)
def update(screen):
	for col in playingBoard:
		for s in col:
			s.draw(screen)
 
#--------#looks to see if there is a full row and returns an array of row index to be deleted (and adds to points)
def checkRows():
	global points
	rowsToDelete = []
	for j in range(height):
		rowFull = True
		for i in range (width):
			if (playingBoard[i][j].empty):
				rowFull = False
				break
		if (rowFull):
			rowsToDelete.append(j)
			points +=1
	return rowsToDelete

#------takes in array list of rows to be deleted and removes these from the screen
def deleteRows(rowNums, screen): 
	for rowNum in rowNums:#iterates through the rows that need to be deleted 	
		for j in range (rowNum,0, -1):
			for i in range (width):
				#-----------set color and empty state to that of the block above it for the row to be deleted to row 1
				playingBoard[i][j].empty=playingBoard[i][j-1].empty
				playingBoard[i][j].color = playingBoard[i][j-1].color
		
		for k in range (width):
			#----------set row 0 to be empty 
			playingBoard[k][0].empty = True
			playingBoard[k][0].color = (117,117,117) 

#----------returns letter associated with key being pressed
def pressedKey():
	key = "null"
	keysPressed = pygame.key.get_pressed()
	if keysPressed[K_r]:
		pygame.time.wait(waitAfterEvent)
		key = "r"
		
	if keysPressed[K_LEFT]:
		pygame.time.wait(waitAfterEvent)
		key = "L"
		
	if keysPressed[K_RIGHT]:
		pygame.time.wait(waitAfterEvent)
		key = "R"
		
	if keysPressed[K_DOWN]:
		pygame.time.wait(waitAfterEvent)
		key = "D"
		
	return key
		
#--------------------returns letter associated with button on screen the user is clicking 
def clickedButton():
	button = "null"
	if pygame.mouse.get_pressed()[0] == True:
		(x,y) = pygame.mouse.get_pos()
		pygame.time.wait(waitAfterEvent)
		
		#----start/pause
		if x/tritrisObj.scale >10 and x/tritrisObj.scale <14 and y/tritrisObj.scale >5.5 and y/tritrisObj.scale <7.5:
			button = "s/p"

		#----rotate
		if x/tritrisObj.scale >10 and x/tritrisObj.scale <14 and y/tritrisObj.scale >9 and y/tritrisObj.scale <11:
			button = "r"
		
		#----left
		elif x/tritrisObj.scale >10 and x/tritrisObj.scale <11.75 and y/tritrisObj.scale >12 and y/tritrisObj.scale <14:
			button = "L"

		#----right
		elif x/tritrisObj.scale >12.25 and x/tritrisObj.scale <14 and y/tritrisObj.scale >12 and y/tritrisObj.scale <14:
			button = "R"

		#----down
		elif x/tritrisObj.scale >11 and x/tritrisObj.scale <13 and y/tritrisObj.scale >14.5 and y/tritrisObj.scale <16.25:
			button = "D"
		
	return button

#-------method called when the player has lost  
def lost(screen):
	global playing
	playing = False 
	
	global highScore

	#-----determines string to appear on window
	if (points>highScore):   
		lostStr = str(points)+" is a new high score!"
		highScore = points
	else:
		lostStr = "      Sorry . . . you lost"

	#------------draws windows
	pygame.draw.rect(screen, (5,5,85), (2*tritrisObj.scale, 5*tritrisObj.scale, 9*tritrisObj.scale, 4.75*tritrisObj.scale))
	endFont = pygame.font.SysFont("Arial", 16, True)
	lostText = endFont.render(lostStr, 1, (255,255,255))
	screen.blit(lostText, (3.25*tritrisObj.scale, 5.5*tritrisObj.scale))
	
	#------------draws buttons 
	pygame.draw.rect(screen, (75,250,70), (3*tritrisObj.scale, 6.5*tritrisObj.scale, 7*tritrisObj.scale, 1*tritrisObj.scale))
	newGameText = endFont.render("New Game", 1, (0,0,0))
	screen.blit(newGameText, (5.2*tritrisObj.scale, 6.6*tritrisObj.scale))

	pygame.draw.rect(screen, (255,117,111), (3*tritrisObj.scale, 8*tritrisObj.scale, 7*tritrisObj.scale, 1*tritrisObj.scale))
	doneText = endFont.render("I'm Done", 1, (0,0,0))
	screen.blit(doneText, (5.4*tritrisObj.scale, 8.1*tritrisObj.scale))
	pygame.display.update()
	
	
	#----checks for first choice 
	global open
	while True:
		choiceEvent = pygame.event.wait()
		if choiceEvent.type == QUIT:
			open = False
			break

		if choiceEvent.type == MOUSEBUTTONDOWN:
			x, y = choiceEvent.pos
	
			#----new game
			if x/tritrisObj.scale >3 and x/tritrisObj.scale <10 and y/tritrisObj.scale >6.5 and y/tritrisObj.scale <7.5:
				break

			#----I'm done
			elif x/tritrisObj.scale >3 and x/tritrisObj.scale <10 and y/tritrisObj.scale >8 and y/tritrisObj.scale <9:
				open = False
				break

#-----------method to reset for a new game   
def newGame(screen, buttonFont, labelFont):
	global points
	points = 0
		
	drawScreen(screen, buttonFont, labelFont)
	update(screen) 
	pygame.display.update()
	
		
		

main()