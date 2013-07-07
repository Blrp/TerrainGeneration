import numpy
from PIL import Image
from random import randrange

class World:
	def __init__(self):
		global size
		global points
		size = (2**9)+1
		points = []
		points = self.createPoints()

	def printPoints(self):
		count = 0
		for p in points:
			print(p.h),
			count+=1
			if(count == size):
				print("")
				count = 0

	def normalizePoints(self, shades):
		shades = shades-1
		section = 255/shades
		bot = 0
		top = section
		
		while(top < 255):
			for point in points:
				if(point.h > bot and point.h <= top):
					point.h = top

			bot = top
			top = top + section

	def writePoints(self, name):
		f = open(str(name)+".txt", "w+")
		count = 0
		for p in points:
			f.write(str(p.h)+"\t")
			count+=1
			if(count == size):
				f.write("\n")
				count = 0

	def writeImage(self, name):
		im = Image.new("RGB", (size,size))
		for y in range(im.size[1]):
			for x in range(im.size[0]):
				point = self.getPoint(x,y)
				amt = point.h
				if(amt < 100):
					im.putpixel((x,y), (0,0,amt+20))
				else:
					im.putpixel((x,y), (0,amt-100,0))

		im.save(str(name)+".png")

	def createPoints(self):
		points = []

		for y in range(size):
			for x in range(size):
				points_x = []
				points_x.append(Point(x, y, 150))
				points.extend(points_x)

		return points

	@staticmethod
	def getPoint(x, y):
		if(x < 0 or x >= size or y < 0 or y >= size):
			return Point(x,y,0)

		point = points[(size * y) + x]

		return point

	def getSize(self):
		return size


class Point:
	def __init__(self, x, y, h=0.0):
		self.x = x
		self.y = y
		self.h = h

	def setHeight(self, new_h):
		self.h = new_h

	def __str__(self):
		return str(self.x)+","+str(self.y)

class Square:
	def __init__(self, tl, tr, bl, br):
		self.mod = 2
		self.tl = tl
		self.tr = tr
		self.bl = bl
		self.br = br

	def getAverageHeight(self):
		return (self.tl.h+self.tr.h+self.bl.h+self.br.h)/4

	def getCenter(self):
		return Main.getMidpoint(self.tl,self.br)

	def modCenter(self):
		center = self.getCenter()
		avg = self.getAverageHeight()
		center.setHeight(avg+randrange(-avg/self.mod,avg/self.mod,1))
		#center.setHeight(avg+randrange(0,avg/self.mod,1))
		self.mod = self.mod/6

	def getDiamondChildren(self):
		center = self.getCenter()

		top_d = Diamond(World.getPoint(center.x, self.tl.y+(self.tl.y-center.y)), center, self.tl, self.tr)
		bot_d = Diamond(center, World.getPoint(center.x, self.bl.y+(self.bl.y-center.y)), self.bl, self.br)
		left_d = Diamond(self.tl, self.bl, World.getPoint(self.tl.x+(self.tl.x-center.x), center.y), center)
		right_d = Diamond(self.tr, self.br, center, World.getPoint(self.tr.x+(self.tr.x-center.x), center.y))

		return [top_d, bot_d, left_d, right_d]

	def getSize(self):
		size_x = self.br.x-self.tl.x
		size_y = self.br.y-self.tl.y

		return size_x*size_y

	def tooSmall(self):
		return self.getSize()<=1

	def getSquareChildren(self):
		top = Main.getMidpoint(self.tl,self.tr)
		bot = Main.getMidpoint(self.bl,self.br)
		left = Main.getMidpoint(self.tl,self.bl)
		right = Main.getMidpoint(self.tr,self.br)
		center = Main.getMidpoint(self.tl, self.br)
		
		square_tl = Square(self.tl, top, left, center)
		square_tr = Square(top, self.tr, center, right)
		square_bl = Square(left, center, self.bl, bot)
		square_br = Square(center, right, bot, self.br)

		return [square_tl, square_tr, square_bl, square_br]

	def __str__(self):
		return "TopLeft: \n"+str(self.tl)+"\nTopRight: \n"+str(self.tr)+"\nBotLeft: \n"+str(self.bl)+"\nBotRight:\n "+str(self.br)

class Diamond:
	def __init__(self, top, bot, lef, rig):
		self.mod=2
		self.top = top
		self.bot = bot
		self.lef = lef
		self.rig = rig

	def getAverageHeight(self):
		return (self.top.h+self.bot.h+self.lef.h+self.rig.h)/4

	def getCenter(self):
		return Main.getMidpoint(self.top, self.bot)

	def modCenter(self):
		center = self.getCenter()
		avg = self.getAverageHeight()
		center.setHeight(avg+randrange(-avg/self.mod,avg/self.mod,1))
		#center.setHeight(avg+randrange(0,avg/self.mod,1))
		self.mod = self.mod/6

	def getSquare(self):
		tl = Main.getMidpoint(self.top, self.lef)
		tr = Main.getMidpoint(self.top, self.rig)
		bl = Main.getMidpoint(self.bot, self.lef)
		br = Main.getMidpoint(self.bot, self.rig)

		return Square(tl, tr, bl, br)

	def __str__(self):
		return "Top: \n"+str(self.top)+"\nBot: \n"+str(self.bot)+"\nLeft: \n"+str(self.lef)+"\nRight: \n"+str(self.rig)

class Main:
	def __init__(self):
		global world
		global count
		global seed
		seed = randrange(100,160,1)
		count = 1
		world = World()
		size = world.getSize()-1

		tl = world.getPoint(0,0)
		tl.setHeight(seed)
		tr = world.getPoint(size,0)
		tr.setHeight(seed)
		bl = world.getPoint(0,size)
		bl.setHeight(seed)
		br = world.getPoint(size,size)
		br.setHeight(seed)

		root_square = Square(tl, tr, bl, br)

		#Recursion
		self.diamondSquareAlgorithm(root_square)

		#Normalization
		world.normalizePoints(5)

		#Print
		#world.printPoints()

		#Image
		world.writeImage("img")

	def diamondSquareAlgorithm(self, root_square):
		count = 0
		root_square.modCenter()
		c_squares = root_square.getSquareChildren()
		c_diamonds = root_square.getDiamondChildren()

		while(True):
			#Mod children diamonds
			for di in c_diamonds:
				di.modCenter()

			#Mod children squares
			for sq in c_squares:
				if(sq.tooSmall()):
					return
				sq.modCenter()

			#Get new children
			temp_squares = []
			temp_diamonds = []
			for sq in c_squares:
				temp_diamonds.extend(sq.getDiamondChildren())
				temp_squares.extend(sq.getSquareChildren())

			c_diamonds = temp_diamonds
			c_squares = temp_squares
			
			count = count + 1

	@staticmethod
	def getMidpoint(point1, point2):
		return world.getPoint((point2.x+point1.x)/2, (point2.y+point1.y)/2)
		
main = Main()