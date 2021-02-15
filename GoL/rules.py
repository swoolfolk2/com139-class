
neighbours = [
    (-1,-1), (0,-1), (1,-1),
    (-1, 0),         (1, 0), 
    (-1, 1), (0, 1), (1, 1)
    ] 

def checkNeighbours(grid, x, y):
    counter = 0
    for neighbour in neighbours:
        newY = y + neighbour[1]
        newX = x + neighbour[0]
        if (0 <= newY < grid.shape[0]) and (0 <= newX < grid.shape[1]):
            if grid[newY, newX] == 255: counter += 1

    #print(counter, x, y)
    return counter

def checkRules(grid, x, y):
    n = checkNeighbours(grid, x, y)
    if (((grid[y,x] == 255) and (2 <= n <= 3)) or (grid[y,x] == 0 and n == 3)): 
        return True
    else:
        return False

    