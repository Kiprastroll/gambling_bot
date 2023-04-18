import pyautogui
import time
import imagehash
from PIL import Image

# import threading

# x, y, width, height, difference

previousDimensions = [461, 227, 32, 32, 8]
checkRoll = [1126, 574, 11, 15, 0]
currentRoll = [900, 400, 100, 100, 0]
chances = [7, 2, 1]  # out of 15
examples = ["exbb", "exbf", "exgb", "exrb", "exrf"]
naming = ["prevRoll", "check", "current", "undefined"]
lastRolls = []
lastShort = []
x = y = width = height = diff = 0
doCheck = True
did10 = doComm = doCalc = False
answer = None


def reqs(arg):
	inp = input(arg)
	if inp.lower() == "y":
		return True
	else:
		return False


def grabimages(a, b):
	cycle = 1
	global naming
	while cycle <= a:
		screenshot = pyautogui.screenshot(region=(x + ((cycle - 1) * (diff + width)), y, width, height))
		screenshot.save(naming[b - 1] + str(cycle) + ".png")
		cycle += 1


def checkimages(file1, file2):
	hash1 = imagehash.average_hash(Image.open(file1))
	hash2 = imagehash.average_hash(Image.open(file2))
	return hash1 == hash2


def checkforcycle(checkl, prevl):
	global x, y, width, height, diff, doCheck, doCalc
	x, y, width, height, diff = checkl
	grabimages(1, 2)
	if checkimages("check1.png", "ex7.png") or checkimages("check1.png", "exC7.png"):
		doCheck = False
		doCalc = True
		print("Same Image")
		x, y, width, height, diff = prevl
		grabimages(10, 1)
	else:
		time.sleep(0.3)


def shorten():
	global lastRolls, lastShort
	lastShort = []
	bulk = 0
	for k in range(len(lastRolls)):
		if k == 0:
			bulk = 1
		elif lastRolls[k] == lastRolls[k - 1]:
			bulk += 1
		else:
			lastShort.append(str(bulk) + lastRolls[k - 1])
			bulk = 1
	lastShort.append(str(bulk) + str(lastRolls[-1]))


out100 = reqs("show last 100 basic? ")
comb100 = reqs("show combined? ")  # TODO

while True:

	if doCheck:
		checkforcycle(checkRoll, previousDimensions)
	elif doCalc:
		print("Calculations n other shit")

		# last roll list creation
		if not did10:
			for i in range(10):
				for j in range(5):
					if checkimages("prevRoll" + str(i + 1) + ".png", examples[j] + ".png"):
						lastRolls.insert(len(lastRolls), examples[j][-2:])
			did10 = True
		else:
			for j in range(5):
				if checkimages("prevRoll1.png", examples[j] + ".png"):
					lastRolls.insert(0, examples[j][-2:])
		if len(lastRolls) > 100:
			del lastRolls[-1]

		# Parameter calculations

		shorten()
		lastam = int(lastShort[0][:1])
		last2col = [lastShort[0][:2][1:], lastShort[1][:2][1:]]
		print(str(last2col))  # last 2 colors
		if last2col[0] == last2col[1]:
			lastam = lastam + int(lastShort[1][:1])
		print(str(lastam))  # last roll amount

		# Probability calculations

		if last2col[0] != "g":
			probabilitySameCol = (chances[0] / 15) ** lastam
			print(str(probabilitySameCol))

		time.sleep(1)
		doCalc = False
		doComm = True
	elif doComm:
		print("Command stuff")
		if out100:
			print(*lastShort, sep=", ")
		time.sleep(2)
		doCheck = True
		doComm = False
