import os
import math
from copy import deepcopy
from collections import deque
import time

# Function that reads the input and writes the output to the file.

allNodes = {}
inputParams = {}
count = 0

def startGameMoveDecision():
	inputFile = open('input.txt', 'r')
	inputArray = inputFile.readlines()

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
	#startGame(pawnPosition, boardPosition, 0)
	position = {}
	for pawns in pawnPosition:
		position[pawns] = {}
		position[pawns].update(getNeighbors(pawns, inputParams['board']))
	value = minimaxSearch(position)
	print (value)
	print (count)

def minimaxSearch(position):
	board = inputParams['board']
	alpha = -1500
	beta = 1500
	depth = 0
	marker = inputParams['color']
	minimaxValue = 0
	tempList = []
	for children in position:
		maximumVal = 0
		for child in position[children]:
			minimaxValue, x, y = children
			minimaxValue = max(minimaxValue, maxValue(child, board, alpha, beta, marker, depth))
			maximumVal = max(maximumVal, minimaxValue)
		tempList.append({(maximumVal): position[children]})
	return tempList

def maxValue(position, board, alpha, beta, marker, depth):
	# Returns a utility value
	# Terminal Test (could be depth or could be goal state)
	global count
	if depth == 3:
		tempList = list(position)
		tempList[0] = evalFunction(position, marker)
		position = tuple(tempList)
		return evalFunction(position, marker)
	neighborsList = getNeighbors(position, board)
	for neighbors in neighborsList:
		count += 1
		board[position[1]][position[2]] = '.'
		if marker == 'WHITE':
			board[neighbors[0]][neighbors[1]] = 'W'
		else:
			board[neighbors[0]][neighbors[1]] = 'B'
		tempList = list(position)
		tempList[0] = minValue(neighbors, board, alpha, beta, marker, depth + 1)
		position = tuple(tempList)
		alpha = max(alpha, position[0])
		if alpha >= beta:
			return beta
	return alpha

def minValue(position, board, alpha, beta, marker, depth):
	global count
	if depth == 3:
		tempList = list(position)
		tempList[0] = evalFunction(position, marker)
		position = tuple(tempList)
		return evalFunction(position, marker)
	neighborsList = getNeighbors(position, board)
	for neighbors in neighborsList:
		count += 1;
		board[position[1]][position[2]] = '.'
		if marker == 'WHITE':
			board[neighbors[0]][neighbors[1]] = 'B'
		else:
			board[neighbors[0]][neighbors[1]] = 'W'
		tempList = list(position)
		tempList[0] = maxValue(neighbors, board, alpha, beta, marker, depth + 1)
		position = tuple(tempList)
		beta = min(beta, position[0])
		if beta <= alpha:
			return alpha
	return beta

def evalFunction(position, marker):
	if marker == 'WHITE':
		goal = (0,0)
	else:
		goal = (15,15)
	xDiff, yDiff = abs(position[0] - goal[0]), abs(position[1] - goal[1])
	euclideanDistance = math.sqrt((math.pow(xDiff, 2) + math.pow(yDiff, 2)))
	return euclideanDistance

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
				tempDict[(0, x1, y1)] = pathString
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