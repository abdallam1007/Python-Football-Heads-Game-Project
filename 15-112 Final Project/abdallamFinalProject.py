# NAME: ABDALLA HASSAN MOHAMED
#andrewID: abdallam
import time
import math
import pygame
pygame.init()

# initialize the window and the caption
window = pygame.display.set_mode((600,600))
pygame.display.set_caption("HEAD SOCCER")

screenWidth = 1200
screenHeight = 600
drag = 1
elasticity = 0.75
gravity,bd = math.pi, 0.2

# this is a helper function that calculates the vectors
# used in calculating the angles
def addVectors(angle1, length1, angle2, length2):
	x = math.sin(angle1) * length1 + math.sin(angle2) * length2
	y = math.cos(angle1) * length1 + math.cos(angle2) * length2
	angle = 0.5 * math.pi - math.atan2(y,x)
	length  = math.hypot(x,y)
	return (angle, length)

# this is the class responsible for creating the ball
class Particle():
	def __init__(self, ballX, ballY, ballSize,ball):
		self.ballX = 600
		self.ballY = 450
		self.ballSize = 80
		self.angle = 0
		self.speed = 10
		self.ball = ball
		self.hitboxB = (self.ballX,self.ballY,self.ballSize,self.ballSize)

	# this function is responsible for for drawing the ball on the screen 
	def display(self):
		window.blit(self.ball,[self.ballX,self.ballY])
		
	# this function is responsible for moving the ball and 
	# calculating the friction with air which makes the projectile 
	# movment 
	def move(self):
		(self.angle, self.speed) = addVectors(self.angle, self.speed, gravity,bd)
		self.ballX += math.sin(self.angle) * self.speed
		self.ballY -= math.cos(self.angle) * self.speed
		self.speed *= drag

	# this is responsible for the collisions between the ball and the goals
	def goalBounce(self,goalLR,goalRR,goalW,goalH):
		ballRect = pygame.draw.rect(window,(255,0,0),\
			(self.ballX,self.ballY,self.ballSize-15,self.ballSize-15),2)
		if goalLR.colliderect(ballRect):
			if self.ballY > goalH:
				self.ballX = 2*self.ballSize - self.ballX
				self.angle = - self.angle
				self.speed *= elasticity
			if self.ballY <= goalH:
				self.ballY = 2*(goalH - self.ballSize) - self.ballY
				self.angle = math.pi - self.angle
				self.speed *= elasticity

		if goalRR.colliderect(ballRect):
			if self.ballY > goalH:
				self.ballX = 2*((screenWidth-goalW) - self.ballSize) - self.ballX
				self.angle = - self.angle
				self.speed *= elasticity

			if self.ballY <= goalH:
				self.ballY = 2*(goalH - self.ballSize) - self.ballY
				self.angle = math.pi - self.angle
				self.speed *= elasticity

	# this function uses gravity,friction and collisions to 
	# to make the movment of the ball as real as possible along the screen
	# it's also responsible for the collisions and reflections with the walls 
	def bounce(self,goalLX,goalLY,goalW,goalH):

		if self.ballX > screenWidth - self.ballSize:
			self.ballX = 2*(screenWidth - self.ballSize) - self.ballX
			self.angle = - self.angle
			self.speed *= elasticity

		elif self.ballX < self.ballSize:
			self.ballX = 2*self.ballSize - self.ballX
			self.angle = - self.angle
			self.speed *= elasticity

		if self.ballY > screenHeight - self.ballSize:
			self.ballY = 2*(screenHeight - self.ballSize) - self.ballY
			self.angle = math.pi - self.angle
			self.speed *= elasticity

		elif self.ballY < self.ballSize:
			self.ballY = 2*self.ballSize - self.ballY
			self.angle = math.pi - self.angle
			self.speed *= elasticity

	# this function detects the collision between 
	# the ball and the left goal
	def isCollision(self,rectP1):
		ballRect = pygame.draw.rect(window,(255,0,0),\
			(self.ballX,self.ballY,self.ballSize-15,self.ballSize-15),2)
		if rectP1.colliderect(ballRect):
			return True

	# this function detects the collision between 
	# the ball and the left goal
	def isCollision2(self,rectP2):
		ballRect = pygame.draw.rect(window,(255,0,0),\
			(self.ballX,self.ballY,self.ballSize-15,self.ballSize-15),2)
		if rectP2.colliderect(ballRect):
			return True

	# this function is responsible for colliding the left player 
	# with the ball
	def collide(self,leadX1,leadY1,leadXChange1):
		dx = leadX1 - self.ballX
		dy = leadY1 - self.ballY
		tangent = math.atan2(dy,dx)
		self.angle = 0.5 * math.pi + tangent
		angle1 = 2 * tangent - self.angle
		angle2 = 2 * tangent - self.angle
		speed1 = leadXChange1 + self.speed
		speed2 = leadXChange1 + self.speed
		(self.angle, self.speed) = (angle1, speed1)
		(self.angle, self.speed) = (angle2, speed2)
		self.ballX += math.sin(self.angle)
		self.ballY -= math.cos(self.angle)

	# this function is responsible for colliding the right player 
	# with the ball
	def collide2(self,leadX2,leadY2,leadXChange2):
		dx = leadX2 - self.ballX
		dy = leadY2 - self.ballY
		tangent = math.atan2(dy,dx)
		self.angle = 0.5 * math.pi + tangent
		angle1 = 2 * tangent - self.angle
		angle2 = 2 * tangent - self.angle
		speed1 = leadXChange2 + self.speed
		speed2 = leadXChange2 + self.speed
		(self.angle, self.speed) = (angle1, speed1)
		(self.angle, self.speed) = (angle2, speed2)
		self.ballX += math.sin(self.angle)
		self.ballY -= math.cos(self.angle)

	# this function is responsible for knowing when a goal
	# is scored in the left goal
	def goalScored(self,goalLX,goalLY,goalW,goalH):
		if self.ballX < goalLX + goalW and self.ballX + self.ballSize \
		< goalLX + goalW:
			if self.ballY > goalLY and self.ballY + self.ballSize \
			> goalLY:
				self.ballX = 600
				self.ballY = 450
				self.angle = 0
				self.speed = 10
				return True

	# this function is responsible for knowing when a goal
	# is scored in the right goal
	def goalScored2(self,goalRX,goalRY,goalW,goalH):
		if self.ballX + self.ballSize > goalRX and self.ballX < goalRX:
			if self.ballY > goalRY and self.ballY + self.ballSize \
			> goalRY:
				self.ballX = 600
				self.ballY = 450
				self.angle = 0
				self.speed = 10
				return True

	# this function is responsible for all the movment that the 
	# computer player makes.
	# the AI will depend on dividing the play ground into boxes and 
	# when the ball is in each one of them a different action will be done by the 
	# computer player
	def AIFunc(self,jumpingC,leadX2,playerWidth):
		# this makes the players collide with each other and not go
		# throgh each other
		if leadX2 + 5 < 995 and leadX2 - 5 > 180 + 40:
			# this checks if the ball is inside the first box 
			if self.ballX <= 300:
				leadX2 -= 5
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 10  
			# this checks if the ball is inside the second box 
			if 300 < self.ballX <= 600: 
				leadX2 -= 5
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 10 
			# this checks if the ball is inside the third box 
			if 600 < self.ballX <= 900:
				leadX2 -= 5
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 10 
			# this checks if the ball is inside the fourth box 
			if 900 < self.ballX <= 1200: 
				leadX2 -= 5
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 10 
			# this checks if the ball is inside the fifth box 
			if self.ballX <= 300 and self.ballY < 300:
				leadX2 -= 5
				# because the ball reached a ceratin height the 
				# the player shuld jump
				jumpingC = True
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 5
			# this checks if the ball is inside the sixth box 
			if 300 < self.ballX <= 600 and self.ballY < 300:
				leadX2 -= 5
				# because the ball reached a ceratin height the 
				# the player shuld jump
				jumpingC = True
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 5
			# this checks if the ball is inside the seventh box 
			if 600 < self.ballX <= 900 and self.ballY < 300:
				leadX2 -= 5
				# because the ball reached a ceratin height the 
				# the player shuld jump
				jumpingC = True
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 5
			# this checks if the ball is inside the eightth box 
			if 900 < self.ballX <= 1200 and self.ballY < 300:
				leadX2 -= 5 
				# because the ball reached a ceratin height the 
				# the player shuld jump
				jumpingC = True
				# this checks if the ball is in front of the player 
				# or behind him.
				# if the ball is behind him the player moves backward 
				if self.ballX + self.ballSize > leadX2 + playerWidth\
				or self.ballSize + self.ballSize > leadX2\
				or self.ballX > leadX2 + playerWidth \
				or self.ballX > leadX2:
					leadX2 += 5 
		return [leadX2,jumpingC]


# this function detects the hover of the mouse over the buttons
# and changes them accordingly and opens new windows according to the button pressed 
def buttonHover(x,y,width,height,inactive,active,action = None):
	position = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + width > position[0] > x and y + height > position[1] > y:
		pygame.draw.rect(window,active,(x,y,width,height),2)
		if click[0] and action != None:
			if action == "quit":
				pygame.quit()
				quit()
			if action == "pvsp":
				playerVS()
			if action == "pvsc":
				ComputerVS()
			if action == "instr":
				Instructions()
			if action == "mainMenu":
				mainGame()
	else:
		pygame.draw.rect(window,inactive,(x,y,width,height),2)

# this function is responsible for inserting messages to the screen 
def insertMessage(msg,color,fontS,XnY,window):
	font = pygame.font.SysFont("comicsansms",fontS)
	txt = font.render(msg,True,color)
	window.blit(txt,[XnY[0],XnY[1]])

# this function is responsible for the window that shows the 
# instructions of the game 
def Instructions():
	insWindow = pygame.display.set_mode((600,600))
	pygame.display.set_caption("Instructions")
	Image = pygame.image.load("background image 13.jpg")

	inactive = (0,0,0)
	active = (100,100,100)

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				run = False

		insWindow.fill((255,255,255))
		window.blit(Image,(0,0))
		insertMessage("How To Play:-",(0,180,0),50,[135,10],insWindow)
		insertMessage(">> Player 1:",(250,0,0),35,[20,80],insWindow)
		insertMessage("- 'right arrow' => move forward "\
			,(230,191,0),25,[25,125],insWindow)
		insertMessage("- 'left arrow' => move backward"\
			,(230,191,0),25,[25,165],insWindow)
		insertMessage("- 'up arrow' => jump",(230,191,0),25,[25,205],insWindow)
		insertMessage("- 'down arrow' => move the leg to shoot the ball",\
			(230,191,0),25,[25,245],insWindow)
		insertMessage(">> Player 2:",(250,0,0),35,[20,285],insWindow)
		insertMessage("- Letter 'D' >> move forward",\
			(230,191,0),25,[25,330],insWindow)
		insertMessage("- Letter 'A' >> move backward",\
			(230,191,0),25,[25,370],insWindow)
		insertMessage("- Letter 'W' >> jump",(230,191,0),25,[25,410],insWindow)
		insertMessage("- Letter 'S' >> move the leg to shoot the ball",\
			(230,191,0),25,[25,450],insWindow)
		buttonHover(200,522,207,50,inactive,active,"mainMenu")
		insertMessage("Main Menu",(0,180,0),40,[205,517],window)
		pygame.display.update()

# this function is responsible for making the player jump whenever 
# the up arrow is pressed 
def jumping(jumping1,maxJump1,leadY1,up,jumpHeight1):
	returned = []
	if jumping1:
		if leadY1 != maxJump1 and leadY1 > maxJump1 and up == True:	
			leadY1 -= 2**2 + 2
		elif leadY1 < jumpHeight1:
			leadY1 += 2**2 + 2
			up = False
		elif leadY1 >= jumpHeight1:
			jumping1 = False
			up = True
	returned += [jumping1] + [maxJump1] + [leadY1] + [up] + [jumpHeight1]
	return returned

# this function is responsible for showing the 
# endgame window when the timer hits 0
# and shows which player one or the computer
def gameEnd(score1,score2,vsplayerorcomputer):
	W = 600
	H = 600
	gameEndWindow = pygame.display.set_mode((W,H))
	pygame.display.set_caption("Game Over")
	Image = pygame.image.load("background image 14.jpg")

	inactive = (0,0,0)
	active = (100,100,100)

	run = True
	while run:
		gameEndWindow.fill((255,255,255))
		window.blit(Image,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					mainGame()
				if event.key == pygame.K_q:
					run = False
		if score1 > score2:
			insertMessage("Player 1 won !!!",(0,180,0),60,[100,50],window)
			insertMessage(str(score1)+" : "+str(score2),(0,180,0),60,[230,150],window)
		elif score2 > score1:
			if not vsplayerorcomputer:
				insertMessage("Player 2 won !!!",(0,180,0),60,[100,50],window)
				insertMessage(str(score1)+" : "+str(score2),(0,180,0),60,[230,150],window)
			else:
				insertMessage("Computer won !!!",(180,0,0),60,[80,50],window)
				insertMessage(str(score1)+" : "+str(score2),(180,0,0),60,[230,150],window)
		elif score2 == score1:
			insertMessage("It's a draw!!"\
				,(180,0,0),60,[130,50],window)
			insertMessage(str(score1)+" : "+str(score2),(180,0,0),60,[230,150],window)

		buttonHover(330,355,207,50,inactive,active,"mainMenu")
		insertMessage("Main Menu",(0,180,0),40,[335,350],window)
		buttonHover(370,425,130,50,inactive,active,"quit")
		insertMessage("QUIT",(0,180,0),40,[380,420],window)
		pygame.display.update()

# this function is responsible for the window of the game 
# mode where two players play against each other
def playerVS():
	screenWidth = 1200
	screenHeight = 600

	playersWindow = pygame.display.set_mode((screenWidth,screenHeight))
	pygame.display.set_caption("Player Vs Player")

	player1imgI = pygame.image.load("player Idle 1.png")
	player1imgF = pygame.image.load("player forward 1.png")

	player1imgB = pygame.image.load("player backward 1.png")
	player1imgBmask = pygame.mask.from_surface(player1imgB)
	player1imgBrect = player1imgB.get_rect()

	player1imgJ = pygame.image.load("player jumping 1.png")
	player1imgS = pygame.image.load("player shooting 1.png")
	player2imgI = pygame.image.load("player Idle 2.png")
	player2imgF = pygame.image.load("player forward 2.png")

	player2imgB = pygame.image.load("player backward 2.png")
	player2imgBmask = pygame.mask.from_surface(player2imgB)
	player2imgBrect = player2imgB.get_rect()

	player2imgJ = pygame.image.load("player jumping 2.png")
	player2imgS = pygame.image.load("player shooting 2.png")
	goalR = pygame.image.load("goal 1.png")
	goalL = pygame.image.load("goal 2.png")
	ball = pygame.image.load("ball 3.png")

	vsPlayer = True
##########goals#######
	goalLX = 0
	goalLY = 300
	goalRX = 1020
	goalRY = 300
	goalW = 180
	goalH = 300
##########players#########
	playerWidth = 65
	playerHeight = 150
	leadX1 = 180
	leadX2 = 920
	leadY1 = 450
	leadY2 = 450
	leadXChange1 = 0
	leadXChange2 = 0
	maxWidthR = goalRX - 25
	maxWidthL = goalLX + goalW
	#######JUMP########
	jumping1 = False
	jumpHeight1 = leadY1
	maxJump1 = 350
	up1 = True
	#################
	jumping2 = False
	jumpHeight2 = leadY2
	maxJump2 = 350
	up2 = True
	########ballMovment#########
	ballX = 600
	ballY = 450
	ballSize = 80
	########Scores############
	score1 = 0
	score2 = 0
	#########timer########
	frameCount = 0
	frameRate = 80
	startTime = 90
	gameend = False
	

	# here we create the ball 
	particle = Particle(ballX,ballY,ballSize,ball)

	clock = pygame.time.Clock()
	run = True
	while run:
		# Here we draw the goals 
		goalLR = pygame.draw.rect(playersWindow,(255,0,0)\
			,(goalLX,goalLY,goalW,20),2)
		goalRR = pygame.draw.rect(playersWindow,(255,0,0)\
			,(goalRX,goalRY,goalW,20),2)

		# here we draw the hitboxes for thentwo players 
		hitboxP1 = (leadX1,leadY1,playerWidth,playerHeight)
		hitboxP2 = (leadX2 + 25,leadY2,playerWidth,playerHeight)
		# we draw the rectangles around the hitboxes 
		rectP1 = pygame.draw.rect(playersWindow,(255,0,0),hitboxP1,2)
		rectP2 = pygame.draw.rect(playersWindow,(255,0,0),hitboxP2,2)

		# here we check for collisions between the ball and the goals 
		particle.goalBounce(goalLR,goalRR,goalW,goalH)

		# here we apply the collision function and call the collide function 
		# accordingly 
		isCollided = particle.isCollision(rectP1)
		if isCollided:
			particle.collide(leadX1,leadY1,leadXChange1)

		isCollided2 = particle.isCollision2(rectP2)
		if isCollided2:
			particle.collide(leadX2,leadY2,leadXChange2)

		playersWindow.fill((96,168,48),rect = (0,430,1200,170))
		playersWindow.fill(((115,194,251)),rect = (0,0,1200,430))
		
		# here we chwck all the events and handle them 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				#mainGame()
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					leadXChange1 = 5
					right = True
				if event.key == pygame.K_LEFT:
					leadXChange1 = -5
				if event.key == pygame.K_UP:
					if jumping1 == False and leadY1 == jumpHeight1:
						jumping1 = True

				if event.key == pygame.K_d:
					leadXChange2 = 5
				if event.key == pygame.K_a:
					leadXChange2 = -5
				if event.key == pygame.K_w:
					if jumping2 == False and leadY2 == jumpHeight2:
						jumping2 = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					leadXChange1 = 0
				if event.key == pygame.K_LEFT:
					leadXChange1 = 0
				if event.key == pygame.K_d:
					leadXChange2 = 0
				if event.key == pygame.K_a:
					leadXChange2 = 0
		# here we change the x and y cordenates to 
		# move the players right and left 
		leadX1 += leadXChange1
		leadX2 += leadXChange2
		# here are the boundries for moving the players
		if leadX1 <= maxWidthL or leadX1 + playerWidth >= maxWidthR:
			leadX1 += -leadXChange1
		if leadX2 <= maxWidthL or leadX2 + playerWidth >= maxWidthR:
			leadX2 += -leadXChange2
		# here we apply the function responsible for making the players jump
		if jumping1:
			returned = jumping(jumping1,maxJump1,leadY1,up1,jumpHeight1)
			jumping1,maxJump1,leadY1,up1,jumpHeight1 = returned[0],returned[1]\
			,returned[2],returned[3],returned[4]
		if jumping2:
			returned = jumping(jumping2,maxJump2,leadY2,up2,jumpHeight2)
			jumping2,maxJump2,leadY2,up2,jumpHeight2 = returned[0],returned[1]\
			,returned[2],returned[3],returned[4]

		# here we move the ball
		particle.move()
		
		# here we check if the ball hit any walls
		particle.bounce(goalLX,goalLY,goalW,goalH)
		# here we draw the ball
		particle.display()
		# here we draw the goals and the players 
		playersWindow.blit(goalL,[goalLX,goalLY])
		playersWindow.blit(goalR,[goalRX,goalRY])
		playersWindow.blit(player1imgB,[leadX1,leadY1])
		playersWindow.blit(player2imgB,[leadX2,leadY2])

		# here we apply the functiion that checks if a goal is scored
		# and increases the score accordingly
		goalS1 = particle.goalScored(goalLX,goalLY,goalW,goalH)
		if goalS1:
			score2 += 1
			leadX1 = 180
			leadX2 = 920
			leadY1 = 450
			leadY2 = 450
			leadXChange1 = 0
			leadXChange2 = 0

		# here we apply the functiion that checks if a goal is scored
		# and increases the score accordingly
		goalS2 = particle.goalScored2(goalRX,goalRY,goalW,goalH)
		if goalS2:
			score1 += 1
			leadX1 = 180
			leadX2 = 920
			leadY1 = 450
			leadY2 = 450
			leadXChange1 = 0
			leadXChange2 = 0

		# here we check if there is collision between the players 
		isOverlap = player1imgBmask.overlap(player2imgBmask,\
			(leadX2-leadX1,leadY2-leadY1))
		if isOverlap:
			if leadX1 > maxWidthL:
				leadX1 -= 5
			if leadX2 + playerWidth < maxWidthR: 
				leadX2 += 5

		insertMessage("Player 1: " + str(score1),\
			(0,180,0),20,[10,0],playersWindow)
		insertMessage("Player 2: " + str(score2),\
			(180,0,0),20,[1080,0],playersWindow)

		# here we introduce the timer to the game 
		totalSeconds = frameCount // frameRate
		totalSeconds = startTime - (frameCount // frameRate)
		if totalSeconds < 0:
			totalSeconds = 0
		seconds = totalSeconds
		outputString = "{}".format(seconds)
		font = pygame.font.SysFont("comicsansms",40)
		text = font.render(outputString, True, (0,0,180)) 
		window.blit(text, [595, 0])
		frameCount += 1
		if seconds == 0:
			run = False
			gameend = True

		pygame.display.update()
		clock.tick(frameRate)
	# here we call the endgame window when the game is over 
	if gameend:
		vsPlayer = False
		gameEnd(score1,score2,vsPlayer)

# this function is responsible for the window of the game 
# mode where a players plays against the computer 
def ComputerVS():
	screenWidth = 1200
	screenHeight = 600

	playersWindow = pygame.display.set_mode((screenWidth,screenHeight))
	pygame.display.set_caption("Player Vs Computer")

	player1imgI = pygame.image.load("player Idle 1.png")
	player1imgF = pygame.image.load("player forward 1.png")

	player1imgB = pygame.image.load("player backward 1.png")
	player1imgBmask = pygame.mask.from_surface(player1imgB)
	player1imgBrect = player1imgB.get_rect()

	player1imgJ = pygame.image.load("player jumping 1.png")
	player1imgS = pygame.image.load("player shooting 1.png")
	player2imgI = pygame.image.load("player Idle 2.png")
	player2imgF = pygame.image.load("player forward 2.png")

	player2imgB = pygame.image.load("player backward 2.png")

	player2imgJ = pygame.image.load("player jumping 2.png")
	player2imgS = pygame.image.load("player shooting 2.png")
	goalR = pygame.image.load("goal 1.png")
	goalL = pygame.image.load("goal 2.png")
	ball = pygame.image.load("ball 3.png")

	vsComputer = False
##########goals#######
	goalLX = 0
	goalLY = 300
	goalRX = 1020
	goalRY = 300
	goalW = 180
	goalH = 300
##########players#########
	playerWidth = 65
	playerHeight = 150
	leadX1 = 180
	leadX2 = 920
	leadY1 = 450
	leadY2 = 450
	leadXChange1 = 0
	leadXChange2 = 0
	maxWidthR = goalRX - 25
	maxWidthL = goalLX + goalW
	#######JUMP########
	jumping1 = False
	jumpHeight1 = leadY1
	maxJump1 = 350
	up1 = True
	jumpingC = False
	jumpHeight2 = leadY2
	maxJump2 = 350
	up2 = True
	leadY2b = 0 
	########ballMovment#########
	ballX = 600
	ballY = 450
	ballSize = 80
	##########Sprites##########
	right = False
	i = 0 
	########Scores############
	score1 = 0
	score2 = 0
	#########timer########
	frameCount = 0
	frameRate = 80
	startTime = 90
	gameend = False

	compR = False
	compL = False
	countComp = 0 
	

	# here we create the ball 
	particle = Particle(ballX,ballY,ballSize,ball)

	player2imgBmask = pygame.mask.from_surface(player2imgB)
	player2imgBrect = player2imgB.get_rect()

	clock = pygame.time.Clock()
	run = True
	while run:
		
		# here we draw the hitboxes for thentwo players 
		hitboxP1 = (leadX1,leadY1,playerWidth,playerHeight)
		hitboxP2 = (leadX2 + 25,leadY2,playerWidth,playerHeight)
		# we draw the rectangles around the hitboxes 
		rectP1 = pygame.draw.rect(playersWindow,(255,0,0),hitboxP1,2)
		rectP2 = pygame.draw.rect(playersWindow,(255,0,0),hitboxP2,2)

		goalLR = pygame.draw.rect(playersWindow,(255,0,0)\
			,(goalLX,goalLY,goalW,20),2)
		goalRR = pygame.draw.rect(playersWindow,(255,0,0)\
			,(goalRX,goalRY,goalW,20),2)

		# here we check for collisions between the ball and the goals 
		particle.goalBounce(goalLR,goalRR,goalW,goalH)

		# here we apply the collision function and call the collide function 
		# accordingly 
		isCollided = particle.isCollision(rectP1)
		if isCollided:
			particle.collide(leadX1,leadY1,leadXChange1)

		isCollided2 = particle.isCollision2(rectP2)
		if isCollided2:
			particle.collide2(leadX2,leadY2,leadXChange2)

		playersWindow.fill((96,168,48),rect = (0,430,1200,170))
		playersWindow.fill(((115,194,251)),rect = (0,0,1200,430))

		# here we chwck all the events and handle them 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					leadXChange1 = 5
					right = True
				if event.key == pygame.K_LEFT:
					leadXChange1 = -5
				if event.key == pygame.K_UP:
					if jumping1 == False and leadY1 == jumpHeight1:
						jumping1 = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					leadXChange1 = 0
				if event.key == pygame.K_LEFT:
					leadXChange1 = 0
		# here we change the x and y cordenates to 
		# move the players right and left 
		leadX1 += leadXChange1
		movmentComp = particle.AIFunc(jumpingC,leadX2,playerWidth)
		leadX2 = movmentComp[0]
		jumpingC = movmentComp[1]
		# here are the boundries for moving the players
		if leadX1 <= maxWidthL or leadX1 + playerWidth >= maxWidthR:
			leadX1 += -leadXChange1
		if leadX2 <= maxWidthL or leadX2 + playerWidth >= maxWidthR:
			leadX2 += -5
		# here we apply the function responsible for making the players jump
		if jumping1:
			returned = jumping(jumping1,maxJump1,leadY1,up1,jumpHeight1)
			jumping1,maxJump1,leadY1,up1,jumpHeight1 = returned[0],returned[1]\
			,returned[2],returned[3],returned[4]

		if jumpingC:
			returned = jumping(jumpingC,maxJump2,leadY2,up2,jumpHeight2)
			jumpingC,maxJump2,leadY2,up2,jumpHeight2 = returned[0],returned[1]\
			,returned[2],returned[3],returned[4]


		# here we move the ball
		particle.move()
		
		# here we check if the ball hit any walls
		particle.bounce(goalLX,goalLY,goalW,goalH)
		# here we draw the ball
		particle.display()
		# here we draw the goals and the players 
		playersWindow.blit(goalL,[goalLX,goalLY])
		playersWindow.blit(goalR,[goalRX,goalRY])
		playersWindow.blit(player1imgB,[leadX1,leadY1])
		playersWindow.blit(player2imgB,[leadX2,leadY2])


		# here we apply the functiion that checks if a goal is scored
		# and increases the score accordingly
		goalS1 = particle.goalScored(goalLX,goalLY,goalW,goalH)
		if goalS1:
			score2 += 1
			leadX1 = 180
			leadX2 = 920
			leadY1 = 450
			leadY2 = 450
			leadXChange1 = 0
			leadXChange2 = 0

		# here we apply the functiion that checks if a goal is scored
		# and increases the score accordingly
		goalS2 = particle.goalScored2(goalRX,goalRY,goalW,goalH)
		if goalS2:
			score1 += 1
			leadX1 = 180
			leadX2 = 920
			leadY1 = 450
			leadY2 = 450
			leadXChange1 = 0
			leadXChange2 = 0

		# here we check if there is collision between the players 
		isOverlap = player1imgBmask.overlap(player2imgBmask,\
			(leadX2-leadX1,leadY2-leadY1))
		if isOverlap:
			if leadX1 > maxWidthL:
				leadX1 -= 5
			if leadX2 + playerWidth < maxWidthR: 
				leadX2 += 5

		insertMessage("Player 1: " + str(score1),\
			(0,180,0),20,[10,0],playersWindow)
		insertMessage("Computer: " + str(score2),\
			(180,0,0),20,[1080,0],playersWindow)

		# here we introduce the timer to the game 
		totalSeconds = frameCount // frameRate
		totalSeconds = startTime - (frameCount // frameRate)
		if totalSeconds < 0:
			totalSeconds = 0
		seconds = totalSeconds
		outputString = "{}".format(seconds)
		font = pygame.font.SysFont("comicsansms",40)
		text = font.render(outputString, True, (0,0,180)) 
		window.blit(text, [595, 0])
		frameCount += 1
		if seconds == 0:
			run = False
			gameend = True

		pygame.display.update()
		clock.tick(frameRate)
	# here we call the endgame window when the game is over 
	if gameend:
		vsComputer = True
		gameEnd(score1,score2,vsComputer)


# this represents the main loop of the program, all the functions are executed here 
# and there are checks for inputs from the user 
def mainGame():
	window = pygame.display.set_mode((600,600))
	pygame.display.set_caption("HEAD SOCCER")
	Image = pygame.image.load("background image 6.jpg")

	inactive = (0,0,0)
	active = (100,100,100)
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		window.fill((255,255,255))
		window.blit(Image,[0,0])
		insertMessage("HEAD SOCCER",(0,180,0),60,[90,10],window)
		buttonHover(40,520,100,50,inactive,active,"pvsp")
		insertMessage("P Vs P",(0,180,0),25,[57,527],window)
		buttonHover(180,520,104,50,inactive,active,"pvsc")
		insertMessage("P Vs Comp",(0,180,0),20,[185,527],window)
		buttonHover(320,520,100,50,inactive,active,"instr")
		insertMessage("Instruc",(0,180,0),25,[325,527],window)
		buttonHover(460,520,100,50,inactive,active,"quit")
		insertMessage("QUIT",(0,180,0),25,[475,527],window)
		pygame.display.update()
	
	pygame.quit()
	quit()

mainGame()