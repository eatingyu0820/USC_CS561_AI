import time
import heapq
import math
import re
from collections import deque

def BFSearch(graph, startPt, endPt):
    # keep track of explored nodes
    #explored = []
    explored = set()
    #explored.add(startPt)
    #print('startPt=', startPt)
    # track all steps to check
    queue = deque()
    queue.append([startPt])# [trail, node]
    while queue:
        # pop the first step from queue
        # step = queue.pop(0) # TO(n)
        step = queue.popleft()
        # get the last node from the step
        node = step[-1]
        if node == endPt:
            bfsOutput(step, True)
            return step
        else:
            if node not in explored:
                neighborPts = graph[node]
                # create a new path for unexplored node
                for neighborPt in neighborPts:
                    newStep = list(step)
                    newStep.append(neighborPt)
                    # newStep=[step, neighborPt]
                    queue.append(newStep)
                # record explored node
                #explored.append(node) # take TO(n)
                #print('node=', node)
                explored.add(node)
    bfsOutput(None, False)

def bfsOutput(step, boo):
    with open("output.txt", 'w') as output:
        if not boo:
            output.write("FAIL")
        else:
            output.write(str(len(step)-1)+'\n')
            output.write(str(len(step))+"\n")
            output.write(" ".join([str(i) for i in step[0]]) +" 0\n")
            for path in (step[1:]):
                output.write(" ".join([str(i) for i in path])+" 1\n")

def UCSearch(graph, startPt, endPt):
    # 1. dict = when find children then save {key:children value:parent}
    # 2. queue save distance + node
    parentDict = {}
    queue = [[0, startPt]]
    heapq.heapify(queue)
    #explored = [startPt]
    explored = set(startPt)
    # calc for output
    totalCost = 0
    stepsCount = 0
    parentDict[startPt] = (startPt,0)
    while queue:
        # pop the first step from queue
        # cost, node = heapq.heappop(queue)
        curCost, node = heapq.heappop(queue)
        if node == endPt:
            while node != startPt:
                # print(node, parentDict[node][1])
                totalCost = totalCost + parentDict[node][1]
                stepsCount+=1
                node = parentDict[node][0]
            # print(node) # only startpoint
            ucsNastarOutput(totalCost, stepsCount, parentDict, True)
        else:
            children = graph[node]
            for child in children:

                if child not in explored:
                    # calculate cost if two planes move cost(14) if only one cost(10)
                    # costCal = abs(child[0]-node[0])+abs(child[1]-node[1])+abs(child[2]-node[2])
                    if (abs(child[0]-node[0])+abs(child[1]-node[1])+abs(child[2]-node[2])) == 2:
                        cost = 14
                    else:
                        cost = 10

                    # dict[key] = value (key:parent/value:child)
                    # Add cost into each node(child point) in dictionary
                    parentDict[child] = (node, cost)
                    # function: heappush(heap, element)
                    heapq.heappush(queue, [curCost+cost, child])
                    #explored.append(child)
                    explored.add(child)

# A* search
def AstarSearch(graph, startPt, endPt):
    # 1. dict = when find children then save {key:children value:parent}
    # 2. queue save distance + node
    parentDict = {}
    parentDict[startPt] = (startPt,0)
    #explored = [startPt]
    explored = set(startPt)
    predictCost = math.sqrt((startPt[0]-endPt[0])**2 + (startPt[1]-endPt[1])**2 + (startPt[1]-endPt[1])**2)
    queue = [[0 + predictCost, startPt]]
    # calc for output
    totalCost = 0
    stepsCount = 0
    while queue:
        # pop the first step from queue
        currCost, node = heapq.heappop(queue)
        predictCost = math.sqrt((node[0]-endPt[0])**2 + (node[1]-endPt[1])**2 + (node[1]-endPt[1])**2)
        # we already added the predictCost at startpoint (prevent duplicate
        currCost -= predictCost
        if node == endPt:
            while node != startPt:
                totalCost = totalCost + parentDict[node][1]
                stepsCount += 1
                node = parentDict[node][0]
            ucsNastarOutput(totalCost, stepsCount, parentDict, True)
            return queue
        else:
            children = graph[node]
            for child in children:
                if child not in explored:
                    # calculate cost if two planes move cost(14) if only one cost(10)
                    if (abs(child[0] - node[0]) + abs(child[1] - node[1]) + abs(child[2] - node[2])) == 2:
                        cost = 14
                    else:
                        cost = 10
                    predictCost = math.sqrt((node[0] - endPt[0]) ** 2 + (node[1] - endPt[1]) ** 2 + (node[1] - endPt[1]) ** 2)
                    # Add cost into each node(child point) in dictionary
                    parentDict[child] = (node, cost)
                    # function: heappush(heap, element)
                    heapq.heappush(queue, [currCost+cost+predictCost, child])
                    #explored.append(child)
                    explored.add(child)

# UCS & Astar Output
def ucsNastarOutput(totalCost, stepsCount, parentDict, boo):
    with open("output.txt", 'w') as output:
        if not boo:
            output.write("FAIL")
        else:
            # 1st line output - total cost
            output.write(str(totalCost) + '\n')
            # 2nd line output - total steps
            output.write(str(stepsCount+1) + "\n")
            # create path for print
            node = endPt
            path = []
            while node != startPt:
                path.append([node, parentDict[node][1]])
                node = parentDict[node][0]
            path.append([startPt, 0])
            path = path[::-1] # print reverse
            for i in path:
                # Removing punctuations in string - Using regex
                res = re.sub(r'[^\w\s]', '', str(i[0]))
                # Nth lines output - step and cost
                output.write(str(res) + ' ' + str(i[1]) + "\n")

# Input file
if __name__ == '__main__':
    # diagonal-move action dictionary
    # straight move(code):
    # X+(1), X-(2), Y+(3), Y-(4), Z+(5), Z-(6)
    # XY: X+Y+(7), X+Y-(8), X-Y+(9), X-Y-(10)
    # XZ: X+Z+(11), X+Z-(12), X-Z+(13), X-Z-(14)
    # YZ: Y+Z+(15), Y+Z-(16), Y-Z+(17), Y-Z-(18)
    actionDict = {1:[1,0,0], 2:[-1,0,0], 3:[0,1,0], 4:[0,-1,0],
                  5:[0,0,1], 6:[0,0,-1], 7:[1,1,0], 8:[1,-1,0],
                  9:[-1,1,0], 10:[-1,-1,0], 11:[1,0,1], 12:[1,0,-1],
                  13:[-1,0,1], 14:[-1,0,-1], 15:[0,1,1], 16:[0,1,-1],
                  17:[0,-1,1], 18:[0,-1,-1]}
    # create an empty dictionary with list type to store the move
    graph = {}
    # open file then python interpreter clean up after its use
    with open('input.txt') as input:
        # 1st line: which algorithm to use (BFS, UCS, A*)
        # strip - removes all leading & trailing whitespace e.g '\n' from a string
        algorithmUse = input.readline().strip()
        # 2nd line: Maze size X-Y-Z dimenssions (separated by one space)
        # Split - seperate into single word (w/ whitespace)
        mazeX, mazeY, mazeZ = input.readline().strip().split()
        mazeX, mazeY, mazeZ = int(mazeX), int(mazeY), int(mazeZ)
        # 3rd line: entrance grid location (3 non-negative int)
        enterX, enterY, enterZ = input.readline().strip().split()
        enterX, enterY, enterZ = int(enterX), int(enterY), int(enterZ)
        startPt = enterX, enterY, enterZ
        # 4th line: exit grid location (3 non-negative int)
        exitX, exitY, exitZ = input.readline().strip().split()
        exitX, exitY, exitZ = int(exitX), int(exitY), int(exitZ)
        endPt = exitX, exitY, exitZ
        # 5th line: number(N) of grids in maze where actions avaliable
        numOfGrid = input.readline().strip()
        numOfGrid = int(numOfGrid)
        # Next N lines: depends on N (number of grids)
        #               follow by the list of valid actions at set-up grid
        for val in range(numOfGrid):
            tempList = input.readline().strip().split()
            tempX, tempY, tempZ = tempList[0:3]
            tempX, tempY, tempZ = int(tempX), int(tempY), int(tempZ)
            actionsOfTemp = tempList[3:numOfGrid]
            actionsOfTemp = [int(i) for i in actionsOfTemp] # convert string into int
            for actionCode in actionsOfTemp:
                move = actionDict[actionCode]
                currentPt = (tempX, tempY, tempZ)
                nextPt = (tempX+move[0], tempY+move[1], tempZ+move[2])
                # set type(list) for graph dictionary
                if tuple(currentPt) not in graph:
                    graph[tuple(currentPt)] = []
                graph[currentPt].append(nextPt)
    # Test CPU time
    startTime = time.time()
    if algorithmUse == "BFS":
        print("Use BFS:")
        BFSearch(graph, startPt, endPt)
    elif algorithmUse == "UCS":
        print("Use UCS:")
        UCSearch(graph, startPt, endPt)
    elif algorithmUse == "A*":
        print("Use A*:")
        AstarSearch(graph, startPt, endPt)
    endTime = time.time()
    print("\nCPU time: ", endTime - startTime)







