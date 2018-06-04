#__________________________________________
#Date: June 3, 2018
#Developer: Joyce Bacic
#Uses Pygame 
#This file contains the objects and the ‘scale’ constant used in the tritris game  
#The square objects are used to make up the piece objects 
#This file is required to run the tritris game
#Coded using Python 3.6.4 and Pygame 1.9.3
#_______________________________________________
import pygame
import random

scale=25

class Square:
	def __init__(self, x_value, y_value, color=(117,117,117)):
		self.x = x_value
		self.y = y_value
		self.scale = scale
		self.empty = True
		self.color = color


	def draw(self, surface):
		pygame.draw.rect(surface, self.color, (self.x*scale, self.y*scale, scale, scale))



# pieces are LINE and CORNER
class Piece:
	def __init__(self):
		self.type = random.choice(["line", "corner"])
		self.pos = 1
		self.sqrs = [] 
		
		if self.type == "line": #colour is blue
			self.color = (27,161,226)
			self.sqrs.append([3,0])
			self.sqrs.append([4,0])
			self.sqrs.append([5,0])

		else: 	#colour is red
			self.color = (240,20,50)
			self.sqrs.append([4,0])
			self.sqrs.append([5,0])
			self.sqrs.append([4,1])

#---------Moving-------		
	def moveDown(self):
		for i in range (3):
			self.sqrs[i][1]+=1 
	def moveLeft(self):
		for i in range(3):
			self.sqrs[i][0]-=1
	def moveRight(self):
		for i in range(3):
			self.sqrs[i][0]+=1

#----------Can Move--------
	def canMoveLeft(self, playingBoard):
		canMove = True
		for s in self.sqrs:
			if (s[0]-1 <0) or (playingBoard[s[0]-1][s[1]].empty==False):
				canMove = False
				break
		
		return canMove

	def canMoveRight(self, playingBoard):
		canMove = True
		for s in self.sqrs:
			if (s[0]+1>8) or (playingBoard[s[0]+1][s[1]].empty==False):
				canMove = False
				break
		return canMove

	def canMoveDown(self, playingBoard):
		canMove = True
		for s in self.sqrs:
			if (s[1]+1 == 18) or (playingBoard[s[0]][s[1]+1].empty==False):
				canMove = False
				break
		return canMove

#-----------Pre and Post move Methods----------
	def updatePiece(self, playingBoard):
		for s in self.sqrs:
			playingBoard[s[0]][s[1]].color = self.color
			
	def erase(self, playingBoard):
		for s in self.sqrs:
			playingBoard[s[0]][s[1]].color = (117,117,117)
			

#----------Rotate-----------
	def rotate(self, board):
	# ------for a line ----------
		if self.type == "line":
			if self.pos == 1 and self.sqrs[2][1]<17: #-------horizontal to vertical 
				if board[self.sqrs[0][0] + 1][self.sqrs[0][1]-1].empty and board[self.sqrs[2][0] -1][self.sqrs[2][1]+1].empty:
					self.sqrs[0][0] +=1
					self.sqrs[0][1] -=1
					self.sqrs[2][0] -=1
					self.sqrs[2][1] +=1
					self.pos = 2
			elif self.pos == 2 and self.sqrs[0][0]>0 and self.sqrs[0][0]<8: #-----vertical to horizonal 
				if board[self.sqrs[0][0] -1][self.sqrs[0][1]+1].empty and board[self.sqrs[0][0]+1][self.sqrs[0][1]-1].empty:
					self.sqrs[0][0] -=1
					self.sqrs[0][1] +=1
					self.sqrs[2][0] +=1
					self.sqrs[2][1] -=1
					self.pos = 1
	#--------for a corner------------
		else : 
			if self.pos == 1 and board[self.sqrs[2][0]+1][self.sqrs[2][1]].empty:
				self.sqrs[2][0] +=1 # -----gose from 	|0||1| to |0||1|
				self.pos = 2	   #-----		|2|          |2|
			elif self.pos == 2 and board[self.sqrs[0][0]][self.sqrs[0][1]+1].empty:
				self.sqrs[0][1] +=1 # -----gose from 	|0||1| to   |1|
				self.pos = 3	   #-----		   |2|   |0||2|
			elif self.pos == 3 and board[self.sqrs[1][0]-1][self.sqrs[1][1]].empty:
				self.sqrs[1][0] -=1 # -----gose from    |1| to|1|
				self.pos = 4	   #-----	       |0||2|   |0||2|
			elif self.pos == 4 and board[self.sqrs[2][0]][self.sqrs[1][1]].empty:
				self.sqrs[1][0]+=1 #----- gose from |1|    to |0||1|
				self.sqrs[0][1]-=1 #-----	      |0||2|    |2|
				self.sqrs[2][0]-=1
				self.pos = 1