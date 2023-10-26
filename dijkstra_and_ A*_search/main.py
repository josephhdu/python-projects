import time
from search.algorithms import State
from search.map import Map
import getopt
import sys
import heapq


def main():
    """
    Function for testing your A* and Dijkstra's implementation. 
    Run it with a -help option to see the options available. 
    """
    optlist, _ = getopt.getopt(sys.argv[1:], 'h:m:r:', ['testinstances', 'plots', 'help'])

    plots = False
    for o, a in optlist:
        if o in ("-help"):
            print("Examples of Usage:")
            print("Solve set of test instances and generate plots: main.py --plots")
            exit()
        elif o in ("--plots"):
            plots = True

    test_instances = "test-instances/testinstances.txt"
    
    # Dijkstra's algorithm and A* should receive the following map object as input
    gridded_map = Map("dao-map/brc000d.map")
    
    nodes_expanded_dijkstra = []  
    nodes_expanded_astar = []

    time_dijkstra = []  
    time_astar = []

    start_states = []
    goal_states = []
    solution_costs = []
       
    file = open(test_instances, "r")
    for instance_string in file:
        list_instance = instance_string.split(",")
        start_states.append(State(int(list_instance[0]), int(list_instance[1])))
        goal_states.append(State(int(list_instance[2]), int(list_instance[3])))
        
        solution_costs.append(float(list_instance[4]))
    file.close()
        
    for i in range(0, len(start_states)):   
    #for i in range(1): 
        start = start_states[i]
        goal = goal_states[i]
    
        time_start = time.time()
        cost, expanded_diskstra = dijkstra(gridded_map, start, goal) # replace None, None with the call to your Dijkstra's implementation
        time_end = time.time()
        nodes_expanded_dijkstra.append(expanded_diskstra)
        time_dijkstra.append(time_end - time_start)

        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by Dijkstra and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()    
            
        #gridded_map.plot_map(expanded_diskstra, start, goal, 'Dtest.png') # printing map for debug

        start = start_states[i]
        goal = goal_states[i]
    
        time_start = time.time()
        cost, expanded_astar = aStar(gridded_map, start, goal) # replace None, None with the call to your A* implementation
        time_end = time.time()

        nodes_expanded_astar.append(expanded_astar)
        time_astar.append(time_end - time_start)

        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by A* and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()
            
        #gridded_map.plot_map(expanded_astar, start, goal, 'Atest.png')

    if plots:
        from search.plot_results import PlotResults
        plotter = PlotResults()
        plotter.plot_results(nodes_expanded_astar, nodes_expanded_dijkstra, "Nodes Expanded (A*)", "Nodes Expanded (Dijkstra)", "nodes_expanded")
        plotter.plot_results(time_astar, time_dijkstra, "Running Time (A*)", "Running Time (Dijkstra)", "running_time")


def dijkstra(map, startState, goalState):
    openList = [] # creating openlist, min heap structure
    closedList = {} # creating closedlist, hash table structure
    cost = 0 #g value
    
    # adding initial state to both lists
    heapq.heappush(openList, startState)
    closedList[startState.state_hash()] = startState
    
    while len(openList) > 0:
        n = heapq.heappop(openList)
        if n == goalState:
            #map.plot_map(closedList, startState, goalState, 'Dtest.png')
            cost = n.get_cost()
            return cost, len(closedList)
        
        children = map.successors(n) #getting the nodes around n
        for child in children:
            hashVal = child.state_hash()
            if hashVal not in closedList:
                child.set_g(child.get_g() + map.cost(child.get_x(), child.get_y()) - map.cost(n.get_x(), n.get_y()))
                child.set_cost(child.get_g())
                heapq.heappush(openList, child)
                
                closedList[hashVal] = child
                
            elif hashVal in closedList:
                if (child.get_g() + map.cost(child.get_x(), child.get_y()) - map.cost(n.get_x(), n.get_y())) < (closedList[hashVal].get_g()):

                    #remove the old child
                    while child in openList:
                        openList.remove(child)
                    
                    child.set_g(child.get_g() + map.cost(child.get_x(), child.get_y()) - map.cost(n.get_x(), n.get_y())) # insert the new cheaper path
                    child.set_cost(child.get_g())
                    heapq.heappush(openList, child)
                        
                    #closedList[hashVal].set_g(child.get_g() + map.cost(child.get_x(), child.get_y()))#******
        
        heapq.heapify(openList)
    
    cost = -1
    #map.plot_map(closedList, startState, goalState, 'Dtest.png')
    return cost, len(closedList)

def aStar(map, startState, goalState):
    openList = [] # creating openlist, min heap structure
    closedList = {} # creating closedlist, hash table structure
    cost = 0 #g value
    
    # adding initial state to both lists
    heapq.heappush(openList, startState)
    closedList[startState.state_hash()] = startState
    
    while len(openList) > 0:
        n = heapq.heappop(openList)
        if n == goalState:
            #map.plot_map(closedList, startState, goalState, 'Atest.png')
            cost = n.get_cost()
            return cost, len(closedList)
        
        children = map.successors(n) #getting the nodes around n
        for child in children:
            hashVal = child.state_hash()
            
            childH = h(child.get_x(), child.get_y(), goalState.get_x(), goalState.get_y())
            
            if hashVal not in closedList:
                child.set_g(child.get_g() + map.cost(child.get_x(), child.get_y()) - map.cost(n.get_x(), n.get_y()))
                childF = child.get_g() + childH #calculates F
                child.set_cost(childF)
                heapq.heappush(openList, child)
                
                closedList[hashVal] = child
                
            elif hashVal in closedList:
                #calculates F and compares with previous F
                if (child.get_g() + map.cost(child.get_x(), child.get_y()) - map.cost(n.get_x(), n.get_y()) + childH) < (closedList[hashVal].get_cost()):

                    #remove the old child
                    while child in openList:
                        openList.remove(child)
                    
                    child.set_g(child.get_g() + map.cost(child.get_x(), child.get_y()) - map.cost(n.get_x(), n.get_y()))# insert the new cheaper path
                    childF = child.get_g() + childH
                    child.set_cost(childF) #calculates F
                    heapq.heappush(openList, child)
                        
                    #closedList[hashVal].set_g(child.get_g() + map.cost(child.get_x(), child.get_y()))
        
        heapq.heapify(openList)
    
    #map.plot_map(closedList, startState, goalState, 'Atest.png')
    cost = -1
    return cost, len(closedList)


def h(startX, startY, goalX, goalY):
    deltaX = abs(startX - goalX)
    deltaY = abs(startY - goalY)
    
    return (1.5 * min(deltaX, deltaY) + abs(deltaX - deltaY))
    
def min(a, b):
    if a < b:
        return a
    else:
        return b

if __name__ == "__main__":
    main()