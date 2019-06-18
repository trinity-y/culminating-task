import pygame
import os
import random
import time
import math
pygame.init()
print('declaring variables...')

#font

#window
WIDTH = 1132
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

#sections
intro = False
playing = True

#colours
WHITE = (249, 246, 244)
BLACK = (35, 35, 34)
#main 
frame = 0
introFrame = 0


print('preparing sprites and rectangles..')

healthBar = pygame.image.load('healthbar.png')

#rect
activeRect = ''

#sorcerer load
IDLE = 0
RUN = 1
ATTACK = 2
villainAttack = []
villainDeath = []
villainIdle = []
villainHealth = 1500

for i in range(10):
	villainAttack.append(pygame.transform.scale(pygame.image.load(os.path.join('villainanimations', 'attack0' + str(i) + '.png')), (300, 300)))
for i in range(25):
	villainDeath.append(pygame.transform.scale(pygame.image.load(os.path.join('villainanimations', 'death' + str(i) + '.png')), (300, 300)))
for i in range(2):
	villainIdle.append(pygame.transform.scale(pygame.image.load(os.path.join('villainanimations', 'death' + str(i) + '.png')), (300, 300)))

villainState = IDLE
villainFrame = 0
villainCoords = (450, -30)
attackVariable = 2300
villainRect = (450, -30, 300, 300)

#bcakground
background = pygame.image.load('dungeon.png').convert_alpha()

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
frontIdle = []
money = 0
for i in range(1, 4):
	frontIdle.append(pygame.transform.scale(pygame.image.load(os.path.join('character\\idle', ' (' + str(i) + ').png')), (150, 150)))

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

#enemy load
frontAttackEnemy = []
leftAttackEnemy = []
rightAttackEnemy = []
backAttackEnemy = []

for i in range(1, 5):
	frontAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'attack front (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	leftAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'attack left (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	rightAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'attack right (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	backAttackEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'attack back (' + str(i) + ').png')), (100, 100)))

frontRunEnemy = []
leftRunEnemy = []
rightRunEnemy = []
backRunEnemy = []
for i in range(1, 5):
	frontRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'run front (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	leftRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'run left (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	rightRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'run right (' + str(i) + ').png')), (100, 100)))
for i in range(1, 5):
	backRunEnemy.append(pygame.transform.scale(pygame.image.load(os.path.join('enemy chars', 'run back (' + str(i) + ').png')), (100, 100)))

print('compiling classes...')

#projectiles
activeProjectiles = []
fireballimage = []
PROJECTILESPEED = 6
for i in range(1, 6):
	fireballimage.append(pygame.transform.scale(pygame.image.load(os.path.join('fireball', 'fireball (' + str(i) + ').gif')), (110, 110)))

#enemy
enemies = []

class enemy:
	def __init__(self):
		self.x = random.choice([0 + 100, WIDTH -100])
		self.y = random.randrange(300, HEIGHT - 50)
		self.frame = 0
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
		global playerHealth, state
		self.directionCounter += 1
		if self.x >= WIDTH or self.x <= 0 or self.y >= HEIGHT or self.y <= 0 or self.health <= 0:
			global enemies, villainHealth, playerHealth
			if self.health <=0:
				villainHealth -= 5
				playerHealth += 20
			enemies.pop(index)

		if self.directionCounter % 300 == 0:
			self.direction = random.choice([1, -1, 2, -2])
			directionCounter = 0

		self.hitbox = pygame.Rect(self.x, self.y, 100, 100)

		if self.directionCounter % 40:
			if self.hitbox.colliderect(activeRect) and self.attackCounter <= 20: #timer so it doesnt constantly attack
				self.state=1
				self.attackCounter += 1
			elif self.attackCounter <= 40 and self.attackCounter > 20:
				self.state= 0
				self.attackCounter +=1
			else:
				self.attackCounter = 0


			if self.frame < 3:#animates
				self.frame += 1
			else:
				self.frame = 0

			if self.state == 0:
				if self.direction == -1:
					self.image = leftRunEnemy[self.frame]
					self.x -= 3
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
						if state == IDLE or state == RUN and self.state == 1:
							playerHealth -= random.choice([1, 3, 2, 1, 1, 2, 1, 2])
							self.state = 0
						elif state == 2:
							self.health -= random.choice([1, 2, 3, 1, 2, 4, 3, 2, 2, 1, 1, 2, 3, 2, 1])

def renderEnemies():
	for enemy in enemies:
		enemy.update(enemies.index(enemy))
		window.blit(enemy.image, (enemy.x, enemy.y))

#projectile
class projectile:#fix rect with sizes
	def __init__(self, aimX, aimY):#when activating a projectile do projectile(charactersX, chractersY)
		global fireballimage
		self.animation = fireballimage
		self.frame = 0
		self.x = 595
		self.y = 35
		self.goalX = aimX
		self.goalY = aimY
		self.rect = pygame.Rect(self.x, self.y, 110, 110)
		self.rise = self.goalY - self.y
		self.run = self.goalX - self.x
		self.hypotenuse = math.sqrt(self.rise*self.rise + self.run*self.run)
		self.speedX = self.run/self.hypotenuse * PROJECTILESPEED
		self.speedY = self.rise/self.hypotenuse * PROJECTILESPEED
		self.hit = False

	def update(self, index):
		global activeRect, PROJECTILESPEED, activeProjectiles, playerHealth, state
		self.x = int(round(self.x + self.speedX))
		self.y = int(round(self.y + self.speedY))
		self.rect = pygame.Rect(self.x, self.y, 110, 110)
		if self.frame >= 3:
			self.frame += 1
		else:
			self.frame == 0
		if self.rect.colliderect(activeRect) and self.hit == False:
			if state != 2:
				playerHealth -= 50
				self.hit = True
			else:
				activeProjectiles.pop(index)
		if self.x >= WIDTH or self.x <= 0 or self.y >= HEIGHT or self.y <= 0 or self.hit == True:
			activeProjectiles.pop(index)
		window.blit(pygame.transform.rotate(self.animation[self.frame], math.degrees(math.atan2(-(self.y-self.goalY), self.x-self.goalX))+180), (self.x, self.y))

def renderProjectiles():
	for projectile in activeProjectiles:
		projectile.update(activeProjectiles.index(projectile))

print('done!')
while intro:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	introrame += 1

#game loop
while playing:
	frame += 1
	if frame == 1000:
		frame == 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.MOUSEBUTTONUP:
			print('clicked')
	keys = pygame.key.get_pressed()#keys
	if keys[pygame.K_UP]:
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
	if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
		speed = 15
	else:
		speed = 17

	#window.fill(BLACK)
	window.blit(background, (0, 0))
	#villain animation
	if villainState == IDLE:
		if frame % 100 == 0:
			if villainFrame == 1:
				villainFrame = 0
			else:
				villainFrame = 1
				attackVariable -= 3
		window.blit(villainIdle[villainFrame], villainCoords)

	elif villainState == ATTACK:
		if frame % 10 == 0:
			if villainFrame <= 8:
				villainFrame +=1
			else:
				villainState = IDLE
				villainFrame = 0
		window.blit(villainAttack[villainFrame], villainCoords)

	elif villainState == 'death':
		if frame % 10 == 0:
			if villainFrame <= 23:
				villainFrame += 1
			else:
				villainframe = 0
		window.blit(villainDeath[villainFrame],villainCoords)

	#rendering the guy
	if state == RUN:
		if direction == 'back':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			charY -= (20 - speed)
			window.blit(backRun[runFrame], (charX, charY))
		elif direction == 'front':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			charY += (20 - speed)
			window.blit(frontRun[runFrame], (charX, charY))
		elif direction == 'left':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			charX -= (20 - speed)
			window.blit(leftRun[runFrame], (charX, charY))
		elif direction == 'right':
			if frame % speed == 0:
				if runFrame <= 3:
					runFrame += 1
				else:
					runFrame = 0
			charX += (20 - speed)
			window.blit(rightRun[runFrame], (charX, charY))
	elif state == IDLE:
		if frame % speed == 0:
			if idleFrame < 2:
				idleFrame += 1
			else:
				idleFrame = 0
		window.blit(frontIdle[idleFrame], (charX, charY))
	elif state == ATTACK:
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
	if state == ATTACK:
		if attackFrame == 1:
			if activeRect.colliderect(villainRect):
				villainHealth -= random.choice([1, 2, 3, 1, 2, 4, 3, 2, 2, 1, 1, 2, 3, 2, 1])
				print(villainHealth)

	#changing states
	if villainState ==  IDLE and frame % random.randrange(100, attackVariable) == 0:
		villainState = ATTACK

	if villainState == ATTACK and len(activeProjectiles) == 0 and frame % 3:
		activeProjectiles.append(projectile(charX, charY))

	if frame % 150 == 0:
		enemies.append(enemy())
		print(playerHealth)
	renderProjectiles()
	renderEnemies()
	state = IDLE #stops player from continually moving
	pygame.display.update()