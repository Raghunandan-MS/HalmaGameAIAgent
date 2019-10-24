import os
import math
from copy import deepcopy
from collections import deque
import time
from collections import defaultdict

# Function that reads the input and writes the output to the file.

allNodes = {}
inputParams = {}
fixedBlackPawns = [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0),(1,1),(1,2),(1,3), (1,4),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(4,0),(4,2)]
fixedWhitePawns = [(11,14), (11,15), (12,13),(12,14),(12,15), (13,12), (13,13),(13,14),(13,15), (14,11),(14,12),(14,13),(14,14),(14,15),(15,11),(15,12),(15,13),(15,14),(15,15)]
count = 0
bestMove = ''

def startGameMoveDecision():
	inputFile = open('input.txt', 'r')
	inputArray = inputFile.readlines()

	inputFile.close()
	gameType = inputArray[0].rstrip('\n')
	playingColor = inputArray[1].rstrip('\n')
	remPlayingTime = inputArray[2].rstrip('\n')
	boardPosition = list(map(list, zip(*createBoardPosition(inputArray[3:]))))

	inputParams['time'] = remPlayingTime
	inputParams['color'] = playingColor
	inputParams['depth'] = 0
	inputParams['game'] = gameType
	inputParams['board'] = boardPosition

	pawnPosition = getPawnsPosition(boardPosition, inputParams['color'])

	position = {}
	tempList = []
	for pawns in pawnPosition:
		position[pawns] = []
		position[pawns].append(getNeighbors(pawns, inputParams['board']))
	'''
	d = defaultdict(list)
	for k, *v in value:
		d[k].append(v)
	print ((list(d.items())))
	outputValue = ''.join((list(d.items())[0][-1][-1]))
	'''
	print (position)
	value = sorted(minimaxSearch(position), key = lambda x: x[0])
	print (value)
	'''
	for i in range(len(value) - 1):
		if (value[i][0] >= value[i+1][0]):
			outputValue = value[i-1][1]
			#print (outputValue)
		else:
			break;
	'''
	#print (outputValue)
	#outputValue = sorted(value, key = lambda x: x[0], reverse = True)[0][1]
	'''
	output_file = open('output.txt', 'w')
	if 'E' in outputValue:
		# Single move and can dump the value to the file as it is!
		output_file.write(outputValue)
	else:
		string = ''
		jumps = outputValue.split(' ')
		for i in range(len(jumps) - 1):
			if i == len(jumps) - 2:
				string = string + 'J' + ' ' + jumps[i] + ' ' + jumps[i+1]
			else:
				string = string + 'J' + ' ' + jumps[i] + ' ' + jumps[i+1] + '\n'
		output_file.write(string)
	output_file.close()
	'''
	'''
	if outputValue.split(' ')[0] == 'E':
		output_file.write(outputValue)
	else:
		string = ''
		jumps = outputValue.split(' ')
		for i in range(len(jumps) - 1):
			if i == len(jumps) - 2:
				string = string + 'J' + ' ' + jumps[i] + ' ' + jumps[i+1]
			else:
				string = string + 'J' + ' ' + jumps[i] + ' ' + jumps[i+1] + '\n'
		output_file.write(string)
	'''
	
def minimaxSearch(position):
	board = inputParams['board']
	alpha = float('-inf')
	beta = float('inf')
	depth = 1
	marker = inputParams['color']
	minimaxValue = 0
	tempList = []
	for children in position:
		minimaxValue, x, y = maxValue(children, board, alpha, beta, marker, depth)
		tempList.append((minimaxValue, position[(0, x, y)][0]))
	return tempList

def maxValue(position, board, alpha, beta, marker, depth):
	# Returns a utility value
	# Terminal Test (could be depth or could be goal state)
	global count
	global bestMove
	if depth == 3:
		evaluationValue = evalFunction(position, board, marker)
		return (evaluationValue, position[1], position[2])
	# Get all white pawn positions.
	# Find the children for all the pawns.
	pawnPosition = getPawnsPosition(board, marker)
	for pawn in pawnPosition:
		neighbors = getNeighbors(pawn, board)
		for neighbor in neighbors:
			count += 1
			tempVal = board[pawn[1]][pawn[2]]
			board[pawn[1]][pawn[2]] = '.'
			if marker == 'WHITE':
				board[neighbor[1]][neighbor[2]] = 'W'
			else:
				board[neighbor[1]][neighbor[2]] = 'B'
			alpha = max(alpha, minValue(neighbor, board, alpha, beta, marker, depth + 1)[0])
			tempList = list(pawn)
			tempList[0] = alpha
			pawn = tuple(tempList)
			board[neighbor[1]][neighbor[2]] = '.'
			board[pawn[1]][pawn[2]] = tempVal
			if alpha >= beta:
				return (beta, neighbor[1], neighbor[2])
	return (alpha, pawn[1], pawn[2])

def minValue(position, board, alpha, beta, marker, depth):
	global count
	global bestMove
	if depth == 3:
		evaluationValue = evalFunction(position, board, marker)
		return (evaluationValue, position[1], position[2])
	# Get all white pawn positions.
	# Find the children for all the pawns.
	if marker == 'WHITE':
		pawnPosition = getPawnsPosition(board, 'BLACK')
	else:
		pawnPosition = getPawnsPosition(board, marker)
	for pawn in pawnPosition:
		neighbors = getNeighbors(pawn, board)
		for neighbor in neighbors:
			count += 1
			tempVal = board[pawn[1]][pawn[2]]
			board[pawn[1]][pawn[2]] = '.'
			if marker == 'WHITE':
				board[neighbor[1]][neighbor[2]] = 'B'
			else:
				board[neighbor[1]][neighbor[2]] = 'W'
			alpha = max(alpha, minValue(neighbor, board, alpha, beta, marker, depth + 1)[0])
			tempList = list(neighbor)
			tempList[0] = alpha
			neighbor = tuple(tempList)
			board[neighbor[1]][neighbor[2]] = '.'
			board[pawn[1]][pawn[2]] = tempVal
			if alpha >= beta:
				return (beta, pawn[1], neighbor[2])
	return (alpha, pawn[1], pawn[2])

def evalFunction(position, board, marker):
	global fixedWhitePawns
	global fixedBlackPawns
	white = getPawnsPosition(board, 'WHITE')
	black = getPawnsPosition(board, 'BLACK')
	totalDistance = 0
	if marker == 'WHITE':
		pawnCount = 0
		# GOAL State Checking
		for pawn in white:
			if (pawn[1], pawn[2]) in fixedBlackPawns:
				pawnCount += 1
		if pawnCount == 19:
			# Goal State. Return the maximum possible value to the node at root.
			return -10
		else:
			for pawns in fixedBlackPawns:
				# Compute distance of this pawn to all pawns.
				# MAKE A CHANGE OVER HERE TO CONTROL THE CENTRAL BOARD POSTION.
				# Give it a higher priority over all other pawns.
				if board[pawns[0]][pawns[1]] == '.':
					totalDistance = totalDistance + (abs(pawns[0] - position[1]) + abs(pawns[1] - position[2]))
					totalDistance = 1.5 * totalDistance
		return totalDistance
	else:
		pawnCount = 0
		for pawn in black:
			if (pawn[1], pawn[2]) in fixedBlackPawns:
				pawnCount += 1
		if pawnCount == 19:
			# Goal State. Return the maximum possible value to the node at root.
			return 1000
		else:
			for pawns in fixedBlackPawns:
				# Compute distance of this pawn to all pawns.
				# MAKE A CHANGE OVER HERE TO CONTROL THE CENTRAL BOARD POSTION.
				# Give it a higher priority over all other pawns.
				if board[pawns[0]][pawns[1]] == '.':
					totalDistance = totalDistance + (abs(pawns[0] - position[1])) + abs(pawns[1] - position[2])
					totalDistance = 1.5 * totalDistance
		return totalDistance

def getNeighbors(position, board):
	# Should return a list of all possible legal moves available.
	tempDict = {}
	visited = set()
	minimaxValue, x, y = position
	visited.add((x, y))
	path = str(x) + ',' + str(y)
	for x1 in range(x-1, x+2):
		for y1 in range(y-1, y+2):
			if ((x != x1 or y != y1) and (0 <= x1 < 16 and 0 <= y1 < 16) and ((x1, y1) not in visited) and board[x1][y1] == '.'):
				pathString = path + ' ' + str(x1) + ',' + str(y1)
				tempDict[(0, x1, y1)] = 'E' + ' ' + pathString
			else:
				if ((x != x1 or y != y1) and (0 <= x1 < 16 and 0 <= y1 < 16) and ((x1, y1) not in visited) and (board[x1][y1] != '.')):
					jumpMoves((0, x, y), board, path, visited, tempDict)
	return tempDict

def jumpMoves(value, board, string, visited, tempDict):
	minimaxValue, x, y = value
	parent = string.split(' ')
	cordinates = parent[0].split(',')
	xPos, yPos = int(cordinates[0]), int(cordinates[1])
	visited.add((x, y))
	for x1 in range(x-2, x+4, 2):
		for y1 in range(y-2, y+4, 2):
			if ((x != x1 or y != y1) and ((x1, y1) not in visited) and (0 <= x1 < 16 and 0 <= y1 < 16) and (board[x1][y1] == '.')):
				if ((board[(x+x1) // 2][(y+y1) // 2] != '.')):
					pathString = string + ' ' + str(x1) + ',' + str(y1)
					tempDict[(0, x1, y1)] = pathString
					jumpMoves((0, x1, y1), board, pathString, visited, tempDict)

def createBoardPosition(values):
	board = []
	for value in values:
		board.append(list(value.rstrip('\n')))
	return board


def getPawnsPosition(board, playColor):
	# Takes a state of the board and returns the position of the respective 
	# White (W) and Black (B) pawns.
	pawnPosition = []
	for x in range(len(board)):
		for y in range(len(board[x])):
			if playColor == 'WHITE' and board[x][y] == 'W':
				pawnPosition.append((0, x, y))
			elif playColor == 'BLACK' and board[x][y] == 'B':
				pawnPosition.append((0, x, y))
	return pawnPosition

if __name__ == "__main__":
	start = time.time()
	startGameMoveDecision()
	end = time.time()
	print ("Total time of execution is : ", abs(end - start))