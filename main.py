# Trinity Y.
# Zelda Culminating ICS201
# June 17th 2019

import pygame
import os
import random
import time
import math
pygame.init()

#window
WIDTH = 1132
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

#sections
intro = False
playing = False
goodending = False
badending = True

#colours
WHITE = (249, 246, 244)
BLACK = (35, 35, 34)

#main 
frame = 0
activeRect = ''

#sorcerer
IDLE = 0
RUN = 1
ATTACK = 2
DEATH = 3
villainAttack = []
villainDeath = []
villainIdle = []
villainHealth = 1500

for i in range(10):#sorcerer load pictures
	villainAttack.append(pygame.transform.scale(pygame.image.load(os.path.join('villainanimations', 'attack0' + str(i) + '.png')), (300, 300)))#every image has th same name except for a number. i used a for loop to cycle through these numbers.
for i in range(25):
	villainDeath.append(pygame.transform.scale(pygame.image.load(os.path.join('villainanimations', 'death' + str(i) + '.png')), (300, 300)))#this method is used for every animation loading
for i in range(2):
	villainIdle.append(pygame.transform.scale(pygame.image.load(os.path.join('villainanimations', 'death' + str(i) + '.png')), (300, 300)))

villainState = IDLE
villainFrame = 0
villainCoords = (450, -30)
attackVariable = 2000
villainRect = (450, -30, 300, 300)

#protagonist load
charX = 10
charY = 500
runFrame = 0
attackFrame = 0
idleFrame = 0
direction = 'forward'
state = IDLE
playerHealth = 400
speed = 20
money = 0
#player load idle
frontIdle = []
for i in range(1, 4):
	frontIdle.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\idle', ' (' + str(i) + ').png')), (150, 150)))
#player load attack
frontAttack = []
leftAttack = []
rightAttack = []
backAttack = []
for i in range(1, 4):
	frontAttack.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\front attack', ' (' + str(i) + ').png')), (150, 150)))
for i in range(1, 4):
	leftAttack.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\left attack', ' (' + str(i) + ').png')), (150, 150)))
for i in range(1, 4):
	rightAttack.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\right attack', '(' + str(i) + ').png')), (150, 150)))
for i in range(1, 4):
	backAttack.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\back attack', ' (' + str(i) + ').png')), (150, 150)))

#player load run
frontRun = []
leftRun = []
rightRun = []
backRun = []
for i in range(1, 6):
	frontRun.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\front run', ' (' + str(i) + ').png')), (150, 150)))
for i in range(1, 6):
	leftRun.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\left run', ' (' + str(i) + ').png')), (150, 150)))
for i in range(1, 6):
	rightRun.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\right run', ' (' + str(i) + ').png')), (150, 150)))
for i in range(1, 6):
	backRun.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\back run', ' (' + str(i) + ').png')), (150, 150)))


#projectiles
activeProjectiles = []
fireballimage = []
PROJECTILESPEED = 6
for i in range(1, 6):
	fireballimage.append(pygame.transform.scale(pygame.image.load(os.path.join('fireball', 'fireball (' + str(i) + ').gif')), (110, 110)))

class projectile:#fix rect with sizes
	def __init__(self, aimX, aimY):#when activating a projectile do projectile(charactersX, chractersY)
		global fireballimage
		self.animation = fireballimage#sets all variables for prpjectile
		self.frame = 0
		self.x = 595
		self.y = 35
		self.goalX = aimX
		self.goalY = aimY
		self.rect = pygame.Rect(self.x, self.y, 110, 110)
		self.rise = self.goalY - self.y#calculates rise (y2-y1)
		self.run = self.goalX - self.x#caclulates run (x2-x1)
		self.hypotenuse = math.sqrt(self.rise*self.rise + self.run*self.run)#calculates hypotenuse using pythagorean theorem
		self.speedX = self.run/self.hypotenuse * PROJECTILESPEED#calculates speed of x
		self.speedY = self.rise/self.hypotenuse * PROJECTILESPEED#calculates speed of y
		self.hit = False

	def update(self, index):#every loop
		global activeRect, PROJECTILESPEED, activeProjectiles
		self.x = int(round(self.x + self.speedX))#change the x & y moving the object
		self.y = int(round(self.y + self.speedY))
		self.rect = pygame.Rect(self.x, self.y, 110, 110)
		if self.frame >= 3:
			self.frame += 1
		else:
			self.frame == 0
		if self.rect.colliderect(activeRect) and self.hit == False:#if hit player, subtract health and set hit tue
			global state, playerHealth
			playerHealth -= 50
			self.hit = True
		if self.x >= WIDTH or self.x <= 0 or self.y >= HEIGHT or self.y <= 0 or self.hit == True:#deletes itself if it goes past borders or if it hits player
			activeProjectiles.pop(index)
		window.blit(pygame.transform.rotate(self.animation[self.frame], math.degrees(math.atan2(-(self.y-self.goalY), self.x-self.goalX))+180), (self.x, self.y))#blits and rotates object towards player

def renderProjectiles():#renders every projectile in the master list
	for projectile in activeProjectiles:
		projectile.update(activeProjectiles.index(projectile))


#enemy
enemies = []
#enemy load attack
frontAttackEnemy = []
leftAttackEnemy = []
rightAttackEnemy = []
backAttackEnemy = []

for i in range(1, 5):
	frontAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'attack front (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	leftAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'attack left (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	rightAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'attack right (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	backAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'attack back (' + str(i) + ').png')), (100, 100)))
#enemy load run
frontRunEnemy = []
leftRunEnemy = []
rightRunEnemy = []
backRunEnemy = []
for i in range(1, 5):
	frontRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'run front (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	leftRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'run left (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	rightRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'run right (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	backRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy_chars', 'run back (' + str(i) + ').png')), (100, 100)))

class enemy:#enemy class
	def __init__(self):#on initiation
		self.x = random.choice([0 + 100, WIDTH -100])#chooes a random place to spawn
		self.y = random.randrange(300, HEIGHT - 50)
		self.frame = 0#variables
		self.directionCounter = 0
		self.health = 30
		self.hitbox = pygame.Rect(100, 100, self.x, self.y)
		if self.x == WIDTH - 100:#left = -1, right = 1, back = 2, front = -2
			self.direction = -1
		else:
			self.direction = 1
		self.image = leftRunEnemy[self.frame]
		self.state = 0#run = 0, attack =1 
		self.attackCounter = 0

	def update(self, index):
		global state, playerHealth
		self.directionCounter += 1
		if self.x >= WIDTH or self.x <= 0 or self.y >= HEIGHT or self.y <= 0 or self.health <= 0:#if the enemy goes out of the border or dies
			global enemies, villainHealth
			if self.health <=0:#if it's killed by player
				global money
				villainHealth -= 5#harm te villain
				if playerHealth < 380:#heal he player for a mximum of 400 health
					playerHealth += 20
				elif playerHealth > 380 and playerHealth < 400:
					playerHealth += (400-playerHealth)
				money += 10#give money

			enemies.pop(index)#delete

		if self.directionCounter % 300 == 0:#change direction every 300 frames
			self.direction = random.choice([1, -1, 2, -2])
			directionCounter = 0

		self.hitbox = pygame.Rect(self.x, self.y, 100, 100)#generates rectangle

		if self.directionCounter % 40:#so attack isnt spammed
			if self.hitbox.colliderect(activeRect) and self.attackCounter <= 20: #timer so it doesnt constantly attack
				self.state=1
				self.attackCounter += 1
			elif self.attackCounter <= 40 and self.attackCounter > 20:
				self.state= 0
				self.attackCounter +=1
			else:
				self.attackCounter = 0


			if self.frame < 3:#changes the frame
				self.frame += 1
			else:
				self.frame = 0

			if self.state == 0:#if running
				if self.direction == -1:#for each direction
					self.image = leftRunEnemy[self.frame]#change animation frame
					self.x -= 3#move character accordingly
				if self.direction == 1:
					self.image = rightRunEnemy[self.frame]
					self.x += 3
				if self.direction == 2:
					self.image = backRunEnemy[self.frame]
					self.y -= 3
				if self.direction == -2:
					self.image = frontRunEnemy[self.frame]
					self.y += 3
			elif self.state == 1:#attack
				if self.direction == -1:
					self.image = leftAttackEnemy[self.frame]
				if self.direction == 1:
					self.image = rightAttackEnemy[self.frame]
				if self.direction == 2:
					self.image = backAttackEnemy[self.frame]
				if self.direction == -2:
					self.image = frontAttackEnemy[self.frame]
				#attack part
				if self.frame == 2:
					if self.hitbox.colliderect(activeRect):
						if state == IDLE or state == RUN and self.state == 1:#if self is attacking player
							playerHealth -= random.choice([1, 3, 2, 1, 1, 2, 1, 2])#random amount of damage to the player
							self.state = 0
						elif state == 2:#if the player is attacking
							global swordupgrade
							self.health -= (random.choice([1, 2, 3, 1, 2, 4, 3, 2, 2, 1, 1, 2, 3, 2, 1]) + swordupgrade)#chooses a random amount of damage plus how much the sword i upgraded by

def renderEnemies():#render enemies
	for enemy in enemies:#for every enemy...
		enemy.update(enemies.index(enemy))#updates enemy
		window.blit(enemy.image, (enemy.x, enemy.y))#blits enemy


#music
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(loops=-1)

#text

pygame.font.init()
minitext = pygame.font.Font(os.path.join('fonts', 'orange kid.ttf'), 25)
titletext = pygame.font.Font(os.path.join('fonts', 'yoster.ttf'), 40)
finaltext = pygame.font.Font(os.path.join('fonts', 'yoster.ttf'), 70)
title = titletext.render('zelda-ish game', False, WHITE)
infotitle= titletext.render('how to play', False, WHITE)
controlstext1= minitext.render('use the UP, LEFT, DOWN and RIGHT keys to move your character.', False, WHITE)
controlstext2= minitext.render('use the W, A, S, D keys to attack.', False, WHITE)
controlstext3 = minitext.render('hold shift to sprint.', False, WHITE)
objectivestext= minitext.render('the objective is to kill the boss without dying!', False, WHITE)
extrainfo = minitext.render('kill the smaller enemies to replenish your health and to gain money',False, WHITE)
extrainfo2 = minitext.render('purchase a sword upgrade for $30 to kill your enemies faster.', False, WHITE)
swordprice = minitext.render('$30', False, BLACK)
goodendingtext = minitext.render('over hundreds of years, the falling city was built into a utopia', False, WHITE)
badendingtitle = finaltext.render('you died...', False, BLACK)
badendingtext = minitext.render('try again?', False, BLACK)
COLOURINTENSITY = 255
red, green, blue = COLOURINTENSITY, 0, 0

#osbtacles and their rects
rock = pygame.transform.scale(pygame.image.load(os.path.join('obstacles', 'rock.png')), (98, 100))
statue = pygame.image.load(os.path.join('obstacles', 'statue.png'))
rockrect = pygame.Rect(250, 250, 55, 45)
statuerect = pygame.Rect(700, 300, 60, 40)

print(rock.get_rect().size)
print(statue.get_rect().size)

#scenes & background

background = pygame.image.load('dungeon.png').convert_alpha()#loads dungeon
introscene = []
for i in range(1, 8):
	introscene.append(pygame.image.load(os.path.join('cut_scene', 'loop 1 (' + str(i) + ').gif')))
for i in range(1, 8):
	introscene.append(pygame.image.load(os.path.join('cut_scene', 'loop 2 (' + str(i) + ').gif')))

for i in range(1, 8):
	introscene.append(pygame.image.load(os.path.join('cut_scene', 'loop 3 (' + str(i) + ').gif')))

for i in range(1, 36):
	introscene.append(pygame.image.load(os.path.join('cut_scene', 'menu loop (' + str(i) + ').gif')))

startButton = [pygame.image.load(os.path.join('gui_buttons', 'Start.png')), pygame.image.load(os.path.join('gui_buttons', 'StartPressed.png'))]
infoButton = pygame.image.load(os.path.join('gui_buttons', 'Icon_Help.png'))
okayButton = pygame.image.load(os.path.join('gui_buttons', 'Okay.png'))

winningBackground = pygame.transform.scale(pygame.image.load(os.path.join('cut_scene', 'goodending.gif')), (1132, 700))
losingBackground = pygame.transform.scale(pygame.image.load(os.path.join('cut_scene', 'cimeterybig.png')), (1132, 700))
shopPiece = pygame.image.load(os.path.join('gui_buttons', 'SHOP.png'))
boomerangIcon = pygame.image.load(os.path.join('gui_buttons', 'boomerang.png'))
swordsIcon = pygame.transform.scale(pygame.image.load(os.path.join('gui_buttons', 'swords.png')), (32, 32))
plusIcon = pygame.transform.scale(pygame.image.load(os.path.join('gui_buttons', 'Add3.png')), (16,16))
coinIcon = pygame.image.load(os.path.join('gui_buttons', 'Coin_1.png'))
healthbarback = pygame.transform.scale(pygame.image.load(os.path.join('gui_buttons', 'RedBar_Empty.png')), (300, 16))
healthbarprogress = pygame.transform.scale(pygame.image.load(os.path.join('gui_buttons', 'RedProgress.png')), (292, 8))



introFrame = 0
introCounter = 0
FRAMESPEED = 70#the lower the faster
loopCounter = 0#counts every loop
#each function is a different scene. it countshow many loops it has done using loopcounter and counts which frame it's on using introFrame
def scene1():
	global introFrame, introscene, loopCounter, title
	if introFrame > 6:#runs through animation
		introFrame = 0
	elif introFrame < 6:
		introFrame += 1
	else:
		introFrame = 0
		loopCounter += 1
	window.fill(BLACK)
	window.blit(introscene[introFrame], (0,0))#blits the background
	window.blit(title, (WIDTH/2, HEIGHT/2))#blits the title

def scene2():
	global introFrame, introscene, loopCounter, title
	if introFrame > 13:
		introFrame = 7
	elif introFrame < 13:
		introFrame += 1
	else:
		introFrame = 7
		loopCounter += 1
	window.fill(BLACK)
	window.blit(introscene[introFrame], (0,0))
	window.blit(title, (WIDTH/2, HEIGHT/2))


def scene3():
	global introFrame, introscene, loopCounter, title
	if introFrame > 20:
		introFrame = 14
	elif introFrame < 20:
		introFrame += 1
	else:
		introFrame = 14
		loopCounter += 1
	window.fill(BLACK)
	window.blit(introscene[introFrame], (0,0))
	window.blit(title, (WIDTH/2, HEIGHT/2))
#the following is repeated for each gif
while loopCounter < 2:#allows two loops of the gif
	for event in pygame.event.get():#checks for a quit event
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	introCounter += 1#counts frame..
	if introCounter % FRAMESPEED == 0:#so we can control how fast the gif runs
		scene1()
	pygame.display.update()#updates display
loopCounter = 0#puts the loop back to 0 (it's reused)

while loopCounter < 2:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	introCounter += 1
	if introCounter % FRAMESPEED == 0:
		scene2()
		introCounter += 1
	pygame.display.update()
loopCounter = 0

while loopCounter < 2:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	introCounter += 1
	if introCounter % FRAMESPEED == 0:
		scene3()
		introCounter += 1
	pygame.display.update()
loopCounter = 0
#intro variables
intro = True
introCounter = 0#sets counter back to 0 for the gif loop
introFrame = 21
startPressed = False#these check if the button is pressed
infoPressed = False
#menu loop
while intro:
	mousex, mousey = pygame.mouse.get_pos()#gets position of the cursor so we can check which button the cursor is on
	for event in pygame.event.get():#checks for quit
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.MOUSEBUTTONUP:#if the mouse button is released
			if mousex >= 502 and mousex <= 627 and mousey >=354 and mousey <= 412:#and it's on the start button
				startPressed = True#set the start button to pressed
			elif mousex >= 10 and mousex <= 74 and mousey >= 10 and mousey <=74:#and it's on the info button
				infoPressed = True
			elif mousex >= WIDTH/2-64 and mousex <=WIDTH/2+64 and mousey >=HEIGHT/2+164 and mousey <= HEIGHT/2+228:
				infoPressed = False
	introCounter += 1
	if introCounter % 10 == 0:#loops the menu gif frame 
		if introFrame <= 54:
			introFrame += 1
		elif introFrame == 55:
			introFrame = 21
	#blits graphics onto te screen (if noral menu)
	window.fill(BLACK)
	window.blit(introscene[introFrame], (0, 0))
	if infoPressed == False:
		window.blit(title, (WIDTH/2-165, HEIGHT/2-250))
	window.blit(infoButton, (10, 10))
	#blits a normal button if nothing is pressed
	if startPressed == False and infoPressed == False:
		window.blit(startButton[0], (WIDTH/2-64, HEIGHT/2))
	elif infoPressed == False and startPressed == True:#blits a pressed button if it's pressed
		window.blit(startButton[1], (WIDTH/2-64, HEIGHT/2))
		if introCounter % 20 == 0:#waits a bit so it's not as startling
			intro = False
			playing = True
	if infoPressed == True:#blits graphics onto the screen (if section)
		window.blit(infotitle, (WIDTH/2-130, HEIGHT/2-250))
		window.blit(controlstext1, (WIDTH/2-400, HEIGHT/2-140))
		window.blit(controlstext2, (WIDTH/2+60, HEIGHT/2-100))
		window.blit(objectivestext, (WIDTH/2-30, HEIGHT/2-180))
		window.blit(controlstext3, (WIDTH/2-250, HEIGHT/2-60))
		window.blit(extrainfo, (WIDTH/2-300, HEIGHT/2-10))
		window.blit(extrainfo2, (WIDTH/2-400, HEIGHT/2+40))
		window.blit(okayButton, (WIDTH/2-64, HEIGHT/2+164))
	pygame.display.update()

swordupgrade = 0
#game loop
while playing:
	frame += 1#for frame counter
	if frame == 1000:#sets it back to zero (i dont want the numbers too high)
		frame == 0
	for event in pygame.event.get():#checks for quit
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type==pygame.MOUSEBUTTONUP:#if button is released
			mousex, mousey = pygame.mouse.get_pos()#get position of cursor
			if mousex >=45 and  mousex <= 77  and mousey >= 100 and mousey <= 132 and money >= 30:#if it's on the sword part and you have enough money
				swordupgrade +=2 #upgrades the sword
				money -= 30#subtrACTS MONEY

	keys = pygame.key.get_pressed()#keys
	if keys[pygame.K_UP]:#each direction changes the state to run an the direction
		direction = 'back'
		state = RUN
	if keys[pygame.K_DOWN]:
		direction = 'front'
		state = RUN
	if keys[pygame.K_LEFT]:
		direction = 'left'
		state = RUN
	if keys[pygame.K_RIGHT]:
		direction = 'right'
		state = RUN
	if keys [pygame.K_a]:
		direction = 'left'
		state = ATTACK
	if keys [pygame.K_d]:
		direction = 'right'
		state = ATTACK
	if keys [pygame.K_w]:
		direction = 'back'
		state = ATTACK
	if keys [pygame.K_s]:
		direction = 'front'
		state = ATTACK
	if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:#changes the speed to faster if shift pressed
		speed = 13
	else:
		speed = 15

	window.blit(background, (0, 0))#blits the background
	#villain animation
	if villainState == IDLE:#if idle
		if frame % 100 == 0:
			if villainFrame == 1:#idle animation
				villainFrame = 0
				if villainHealth <= 1000:#if its low on health, make the villain attack more often
					attackVariable -= 3
			else:
				villainFrame = 1
				attackVariable -= 3#make villain attack more often
				if villainHealth <= 1000:
					attackVariable -=2#if its low on health, make the villain attack more often
		window.blit(villainIdle[villainFrame], villainCoords)#blits villain

	elif villainState == ATTACK:#if attacking
		if frame % 10 == 0:#do villain attack animation
			if villainFrame <= 8:
				villainFrame +=1
			else:
				villainState = IDLE
				villainFrame = 0
		window.blit(villainAttack[villainFrame], villainCoords)#blits villain

	elif villainState == DEATH:#if dyig
		if frame % 10 == 0:#do villain death animation
			if villainFrame <= 23:
				villainFrame += 1
			else:
				goodending = True
				playing = False
				villainframe = 0
		window.blit(villainDeath[villainFrame],villainCoords)#blits villain

	#rendering the guy
	if state == RUN:#if running...
		if direction == 'back':#for each direction...
			if frame % speed == 0:#animation
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			if charY > 20-speed:#checks for bordders
				if not pygame.Rect(charX, charY - (20-speed), 100, 100).colliderect(rockrect) and not pygame.Rect(charX , charY- (20-speed), 100, 100).colliderect(statuerect):#if not colliding with obstacles
					charY -= (20 - speed)#moves player
			window.blit(backRun[runFrame], (charX, charY))#blits the player
		elif direction == 'front':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			if charY < HEIGHT - 20-speed -150:
				if not pygame.Rect(charX, charY+ (20-speed), 100, 100).colliderect(rockrect) and not pygame.Rect(charX, charY + (20-speed), 100, 100).colliderect(statuerect):
					charY += (20 - speed)
			window.blit(frontRun[runFrame], (charX, charY))
		elif direction == 'left':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			if charX > (20-speed):
				if not pygame.Rect(charX - (20-speed),  charY, 100, 100).colliderect(rockrect) and not pygame.Rect(charX- (20-speed), charY, 100, 100).colliderect(statuerect):
					charX -= (20 - speed)
			window.blit(leftRun[runFrame], (charX, charY))
		elif direction == 'right':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			if charX < WIDTH - 20 - speed - 150:
				if not pygame.Rect(charX + (20-speed), charY, 100, 100).colliderect(rockrect) and not pygame.Rect(charX + (20-speed), charY, 100, 100).colliderect(statuerect):
					charX += (20 - speed)
			window.blit(rightRun[runFrame], (charX, charY))
	elif state == IDLE:#idle animation
		if frame % speed == 0:
			if idleFrame < 2:
				idleFrame += 1
			else:
				idleFrame = 0
		window.blit(frontIdle[idleFrame], (charX, charY))
	elif state == ATTACK:#attack animation
		if direction == 'front':
			if frame % speed == 0:
				if attackFrame <= 1:
					attackFrame += 1
				else:
					attackFrame = 0
			window.blit(frontAttack[attackFrame], (charX, charY))
		elif direction == 'back':
			if frame % speed == 0:
				if attackFrame <= 1:
					attackFrame += 1
				else:
					attackFrame = 0
			window.blit(backAttack[attackFrame], (charX, charY))
		elif direction == 'right':
			if frame % speed == 0:
				if attackFrame <= 1:
					attackFrame += 1
				else:
					attackFrame = 0
			window.blit(rightAttack[attackFrame], (charX, charY))
		elif direction == 'left':
			if frame % speed == 0:
				if attackFrame <= 1:
					attackFrame += 1
				else:
					attackFrame = 0
			window.blit(leftAttack[attackFrame], (charX, charY))
	activeRect = pygame.Rect(charX, charY, 150, 150)

	#attack!!
	if state == ATTACK:#if attacking
		if attackFrame == 1:
			if activeRect.colliderect(villainRect):#if its hitting villain
				villainHealth -= (random.choice([1, 2, 3, 1, 2, 4, 3, 2, 2, 1, 1, 2, 3, 2, 1]) + swordupgrade)#removes health

	#changing states
	if villainState ==  IDLE and frame % random.randrange(100, attackVariable) == 0:#attacks randomly (though more frequently if attackVariable is lower)
		villainState = ATTACK

	if villainState == ATTACK and frame % 2 == 0:
		if villainHealth > 600 and len(activeProjectiles) == 0:
			activeProjectiles.append(projectile(charX, charY))
		elif villainHealth <= 599 and len(activeProjectles) <= 1:
			activeProjectiles.append(projectile(charX, charY))

	if frame % 150 == 0:#spawns a new enempy evr 150 frames
		enemies.append(enemy())
	#ENEMY HEALTH BAR
	window.blit(healthbarback, (WIDTH/2-150, 20))
	if villainHealth >=5:
		window.blit(pygame.transform.scale(healthbarprogress, (round(villainHealth/1500*292), 8)),(WIDTH/2-146, 24))
	#PLAYER HEALTH BAR
	window.blit(healthbarback, (WIDTH/2-150, HEIGHT-20))
	if playerHealth >= 2:
		window.blit(pygame.transform.scale(healthbarprogress, (round(playerHealth/400*292), 8)), (WIDTH/2-146, HEIGHT-16))
	window.blit(rock,(250, 250))#blits obstacles
	window.blit(statue, (700, 300))
	window.blit(coinIcon, (WIDTH - 74, 10))
	window.blit(minitext.render('$'+str(money), False, WHITE), ((WIDTH-104, 30)))
	window.blit(shopPiece, (10, 10))
	window.blit(swordsIcon, (45, 100))	
	window.blit(swordprice, (82, 105))
	window.blit(plusIcon, (60, 115))

	if villainHealth <= 0:#dies if health is below /at0
		villainState = DEATH

	if playerHealth <= 0:#triggers bad ending if player dies
		playing = False
		badending = True
	renderProjectiles()#rendersprojectile
	renderEnemies()#renders enemy
	state = IDLE #stops player from continually moving
	pygame.display.update()

while goodending:
	for event in pygame.event.get():#checks for qut
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	window.fill(BLACK)
	window.blit(winningBackground, (0, 0))
	if red == COLOURINTENSITY and green < COLOURINTENSITY and blue == 0:#colour changing text
		green += 1
	elif red > 0 and green == COLOURINTENSITY and blue == 0:
		red -= 1
	elif red == 0 and green == COLOURINTENSITY and blue < COLOURINTENSITY:
		blue += 1
	elif red == 0 and green > 0 and blue == COLOURINTENSITY:
		green -= 1
	elif red < COLOURINTENSITY and green == 0 and blue == COLOURINTENSITY:
		red += 1
	elif red == COLOURINTENSITY and green == 0 and blue > 0:
		blue -= 1
	youwontext = finaltext.render('YOU WON!', False, (red, green, blue))#txt
	window.blit(youwontext, (WIDTH/2-100, HEIGHT/2-100))
	window.blit(goodendingtext, (WIDTH/2-100, HEIGHT/2-50))
	pygame.display.update()

while badending:
	for event in pygame.event.get():#checks for quit
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	window.fill(BLACK)
	window.blit(losingBackground, (0, 0))#text
	window.blit(badendingtitle, (WIDTH/2+60, HEIGHT/2-100))
	window.blit(badendingtext, (WIDTH/2+100, HEIGHT/2))
	pygame.display.update()