"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

from io import TextIOWrapper
import sys, argparse
import numpy as np
from matplotlib.image import AxesImage as aximg
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from rules import checkRules
from configurations import Configuration
from configurations import Configurations

ON = 255
OFF = 0
BLOCK = 1
vals = [ON, OFF]
PATH = "files/"


def createGrid(N: int, M: int) -> np.ndarray: 
    """[Creates a grid given the measures]

    Args:
        N (int): [Number of rows to create]
        M (int): [Number of columns to create]

    Returns:
        np.ndarray: [returns a grid with N rows and M columns]
    """ 
    return np.zeros(N*M).reshape(N,M)
    #return np.random.choice(vals, N*M, p=[0.2, 0.8]).reshape(N, M)

def randomGrid(N: int, M: int) -> np.ndarray:
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*M, p=[0.2, 0.8]).reshape(N, M)

def update(frameNum: int, img: aximg, grid: np.ndarray, config: Configuration, output: TextIOWrapper) -> aximg:
    """[Updates the Universe with the set of rules and detecs the configurations that exist]

    Args:
        frameNum (int): Number of the current generation
        img (aximg): Image to display the Universe
        grid (np.ndarray): Universe in for of a 2D space
        config (Configuration): Configuration of the Universe
        output (TextIOWrapper): File to where write the data of the current Universe's generation

    Returns:
        aximg: img updated
    """
    
    config.generation = frameNum + 1
    # copy grid since we require 8 neighbors for calculation
    newGrid = grid.copy()
    
    n, m = grid.shape
    visitedGrid = np.zeros(n*m).reshape(n,m)
    
    for y in range(n):
        for x in range(m):
            # First we check how many configurations exist
            if grid[y, x] == ON and visitedGrid[y,x] != 255:
                for c in reversed (Configurations):
                    flag, toPaint = config.isConfiguration(x, y, c.value)
                    if flag:
                        #print("found {}".format(c.name))
                        config.configurations[c.name] += 1
                        config.generationConfigurations += 1
                        for cell in toPaint:
                            newY = y + cell[1]
                            newX = x + cell[0]
                            visitedGrid[newY, newX] = 255
                        break
            #  We apply the set of rules to know wich cells live 
            if checkRules(grid, x, y):
                newGrid[y, x] = ON
            else:
                newGrid[y, x] = OFF

               
    # update data
    config.update(output, newGrid)
    img.set_data(newGrid)
    grid[:] = newGrid[:]

    return img,

# main() function
def main():
    # sys.argv[0] is the script name itself and can be ignored
    # sys.argv[1] is the name of the INPUT_FILE
    N, M, FRAMES = [0,0,0]
    fileName = "RandomGrid"
    try:
        fileName =  sys.argv[1]
        input = open(PATH+fileName)

        # set grid size
        N, M, FRAMES = [int(x) for x in input.readline().split()]    
        
        grid = createGrid(N, M) 

        # Set initial CONFIGURATIONS
        for line in input:
            line = line.strip("\n")

            x, y = [int(x) for x in line.split()]
            grid[y, x] = ON

        print("Running simulation using INPUT FILE: {}".format(fileName))
        print("Universe size: x: {} y: {}".format(N,M))
        print("GENERATIONS: {}".format(FRAMES))

        
    except:
        print("No such file in INPUT PATH, running with default input")
        fileName = "RandomGrid"
        # declare grid
        grid = np.array([])
        # populate grid with random on/off - more off than on
        N, M, = [100,100]
        grid = randomGrid(N,M)
        FRAMES = 200

        print("Running simulation using Random Grid")
        print("Universe size: x: {} y: {}".format(100,100))
        print("GENERATIONS: {}".format(200))
        
    
    # set header of file
    output = open(PATH+'{}.out'.format(fileName.strip(".txt")), 'w+')
    toWrite = ' GENERATION | CONFIGURATIONS | '
    for c in Configurations:
        toWrite += '{}: AMOUNT - PERCENTAGE | '.format(c.name)
    output.write('{}GAME OF LIFE OUTPUT FILE{}\n'.format(" "*int(len(toWrite)/2)," "*int(len(toWrite)/2)))
    output.write(' UNIVERSE SIZE -> ROWS:{} COLUMNS:{}\n'.format(N,M))
    output.write(' NUMBER OF GENERATIONS: {}\n'.format(FRAMES))
    toWrite +='\n{}\n'.format("="*len(toWrite))
    output.write(toWrite)
        
    # set animation update interval
    updateInterval = 50
    configuration = Configuration(grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, configuration, output),
                                  frames = FRAMES,
                                  interval= updateInterval,
                                  save_count=50,
                                  repeat = False)

    plt.show()

# call main
if __name__ == '__main__':
    main()