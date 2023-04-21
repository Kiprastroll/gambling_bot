import random

import pyautogui
import time
import imagehash
from PIL import Image
import threading

# x, y, width, height, difference

previousDimensions = [461, 227, 32, 32, 8]
checkRoll = [1126, 574, 11, 15, 0]
currentRoll = [900, 400, 100, 100, 0]
chances = [7, 2, 1]  # out of 15
examples = ["exbb", "exbf", "exgb", "exrb", "exrf"]
naming = ["prevRoll", "check", "current", "undefined"]
lastRolls = []
lastShort = []
x = y = width = height = diff = genCycle = sinceGreen = 0
doCheck = True
did10 = doComm = doCalc = False
answer = None
targetRed = {}
targetBlack = {}
targetGreen = {}
prevBet = {}
balance = {}
seed = "002001234567890123456789012345678901234567890123456789012345678901234567890"  # num(3), bet(1), values(18 * n)
ifBet = False


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
	global x, y, width, height, diff, doCheck, doCalc, genCycle
	x, y, width, height, diff = checkl
	grabimages(1, 2)
	if checkimages("check1.png", "ex7.png") or checkimages("check1.png", "exC7.png"):
		doCheck = False
		doCalc = True
		print("Same Image")
		x, y, width, height, diff = prevl
		grabimages(10, 1)
		genCycle += 1
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


def start_threads(n):
	for thr in range(1, n+1):
		thread_name = "simulationThread" + str(thr)
		t = threading.Thread(name=thread_name, target=thread_function, args=(thr,))
		t.start()
		t.join()


def thread_function(num):
	global targetRed, targetGreen, targetBlack, probabilityOtherCol, probabilityGreen, balance, prevBet, last2col,\
		genCycle
	print("Thread Number " + str(num) + " ----------------- \n")
	if not genCycle == 1:
		if last2col[0] == "b" or last2col[0] == "r":
			if prevBet[num] == last2col[0]:
				balance[num] += 0.1
				print("previous bet was right, balance is: " + str(balance[num]))
			else:
				balance[num] += -0.1
				print("previous bet was not right, balance is: " + str(balance[num]))
		elif last2col[0] == "g":
			if prevBet[num] == last2col[0]:
				balance[num] += 1.3
				print("previous bet was right, balance is: " + str(balance[num]))
			else:
				balance[num] += -0.1
				print("previous bet was not right, balance is: " + str(balance[num]))
		else:
			print("no bet was submitted")
	print("\n")
	if last2col[0] == "g":
		print("last roll was green")
		prevBet[num] = "skip"
	elif last2col[0] == "r":
		print("last roll was red")
		if targetBlack[num] < probabilityOtherCol and not targetGreen[num] < probabilityGreen:
			print("next roll is probably going to be black")
			prevBet[num] = "b"
		elif targetBlack[num] < probabilityOtherCol and targetGreen[num] < probabilityGreen or\
			targetBlack[num] > probabilityOtherCol and targetGreen[num] < probabilityGreen:
			print("next roll is probably going to be green")
			prevBet[num] = "g"
		else:
			print("no target was met")
			prevBet[num] = "skip"
	elif last2col[0] == "b":
		print("last roll was black")
		if targetRed[num] < probabilityOtherCol and not targetGreen[num] < probabilityGreen:
			print("next roll is probably going to be red")
			prevBet[num] = "r"
		elif targetRed[num] < probabilityOtherCol and targetGreen[num] < probabilityGreen or\
			targetRed[num] > probabilityOtherCol and targetGreen[num] < probabilityGreen:
			print("next roll is probably going to be green")
			prevBet[num] = "g"
		else:
			print("no target was met")
			prevBet[num] = "skip"
	print("\n")






def get_top_keys(dictionary, number):
	sorted_items = sorted(dictionary.items(), key=lambda lst: lst[1], reverse=True)
	top_items = sorted_items[:number]
	top_keys = [item[0] for item in top_items]
	return top_keys



out100 = reqs("show last 100 basic? (y/n) ")
comb100 = reqs("show combined? (y/n) ")  # TODO
loadSeed = reqs("load a seed? (y/n) ")
if not loadSeed:
	numSimulations = int(input("Number of threads: (int) "))
	for o in range(1, numSimulations + 1):
		targetRed[o] = round(random.uniform(0, 1), 4)
		targetBlack[o] = round(random.uniform(0, 1), 4)
		targetGreen[o] = round(random.uniform(0, 1), 4)
else:
	numSimulations = int(seed[:3])
	for o in range(1, numSimulations + 1):
		targetRed[o] = int(seed[(4 + (o - 1) * 18):][:(6 + (1 - 1) * 18)]) / 100000
		targetBlack[o] = int(seed[(10 + (o - 1) * 18):][:(6 + (1 - 1) * 18)]) / 100000
		targetGreen[o] = int(seed[(16 + (o - 1) * 18):][:(6 + (1 - 1) * 18)]) / 100000
cyclesGeneration = int(input("Cycles per generation: (int) "))
startBal = int(input("Starting balance (each bet uses 0.1): (int) "))
for m in range(numSimulations):
	balance[m + 1] = startBal


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
		for ind, value in enumerate(lastRolls):
			if value[0] == "g":
				sinceGreen = ind + 1
				break
			elif ind + 1 == len(lastRolls):
				sinceGreen = len(lastRolls)
		print(str(last2col))  # last 2 colors
		if last2col[0] == last2col[1]:
			lastam = lastam + int(lastShort[1][:1])
		print(str(lastam))  # last roll amount

		# Probability calculations

		if last2col[0] != "g":
			probabilitySameCol = (chances[0] / 15) ** lastam
		else:
			probabilitySameCol = chances[0] / 15
		probabilityGreen = pow((1 - ((15 - chances[2]) / 15)), sinceGreen)
		probabilityOtherCol = 1 - probabilityGreen - probabilitySameCol
		print("probability Green: " + str(probabilityGreen))  # TODO
		print("probability Other color: " + str(probabilityOtherCol))

		# generation instances

		if genCycle <= cyclesGeneration:
			start_threads(numSimulations)
		else:
			print("generation end")
			# get_top_keys()


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
