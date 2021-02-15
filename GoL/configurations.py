from enum import Enum
from io import TextIOWrapper
import numpy as np



class Configurations(Enum):
    """[Enumerator to specify Configuration types]
    """
    Block, Beehive, Loaf, Boat, Tub, Blinker, Toad, Beacon, Glider, Spaceship = range(10)

class Configuration:
    """[Configuration class for a Universe]
    """

    def __init__(self, grid: np.ndarray):
        """[Class Initializer]

        Args:
            grid (np.ndarray): [Universe of the configuration]

        Properties:
            grid (np.ndarray): [Universe of the configuration]
            generation (int): [last generation]
            generationConfigurations (int): [amount of configurations in the last generation]
            configurations (diccionary): [Dictionary with the distribution of each configuration]
            configurationForms (list of 2D objects): [A list than contains the info of each configuration's form]
        """

        self.grid = grid
        self.generation = 0
        self.generationConfigurations = 0
        
        self.configurations = {
            "Block":0, "Beehive":0, "Loaf":0, "Boat":0, "Tub":0,
            "Blinker":0, "Toad":0, "Beacon":0,
            "Glider":0, "Spaceship":0
            }

        self.Block = [[0,0], [1,0],
                      [0,1], [1,1]]
        
        self.Beehive = [[0,0], [1,0],
                   [-1,1],         [2,1],
                        [0,2], [1,2]]
        
        self.Loaf = [[0,0], [1,0],
                [-1,1],         [2,1],
                     [0,2],     [2,2],
                            [1,3]]
        
        self.Boat = [[0,0], [1,0],
                     [0,1],     [2,1],
                            [1,2]]

        self.Tub = [[0,0],
              [-1,1],   [1,1],
                    [0,2]]
        
        self.Blinker1 = [[0,0],
                        [0,1],
                        [0,2]]

        self.Blinker2 = [[0,0], [1,0], [2,0]]

        self.Toad1 = [[0,0],
           [-2,1],       [1,1],
           [-2,2],       [1,2],
                [-1,2]]
        
        self.Toad2 = [[0,0], [1,0], [2,0],
               [-1,1],[0,1], [1,1]]

        self.Beacon1 = [[0,0], [1,0],
                        [0,1], [1,1],
                                   [2,2], [3,2],
                                   [2,3], [3,3]]
        
        self.Beacon2 = [[0,0], [1,0], [0,1],[3,2],[2,3], [3,3]]

        self.Glider1 = [[0,0],
                            [1,1],
                [-1,2],[0,2],[1,2]]
        
        self.Glider2 = [[0,0],    [2,0],
                            [1,1],[2,1],
                            [1,2]]
        
        self.Glider3 = [[0,0],
            [-2,1],     [0,1],
                 [-1,2],[0,2]]

        self.Glider4 = [[0,0],
                            [1,1],[2,1],
                        [0,2],[1,2]]

        self.Spaceship1 = [[0,0],          [3,0],
                                                 [4,1],
                           [0,2],                [4,2],
                               [1,3],[2,3],[3,3],[4,3]]
        
        self.Spaceship2 = [
                        [0, 0], [1,0],
        [-2,1], [-1,1],         [1,1], [1,2],
        [-2,2], [-1,2], [0,2],  [1,2],
                [-1,3], [0,3]
        ]

        self.Spaceship3 = [
                [0,0], [1,0], [2,0], [3,0],
        [-1,1],                      [3,1],
                                     [3,2],
        [-1,3],               [2,3]

        ]

        self.Spaceship4 = [
                [0,0], [1,0],
        [-1,1], [0,1], [1,1], [2,1],
        [-1,2], [0,2],        [2,2], [3,2],
                       [1,3], [2,3]
        ]
                        

        
        self.configurationsForms = [[self.Block], [self.Beehive], [self.Loaf], [self.Boat], [self.Tub],
                                    [self.Blinker1, self.Blinker2], [self.Toad1, self.Toad2], [self.Beacon1, self.Beacon2],
                                    [self.Glider1, self.Glider2, self.Glider3, self.Glider4], [self.Spaceship1, self.Spaceship2, self.Spaceship3, self.Spaceship4]]

    def update(self ,file: TextIOWrapper, grid: np.ndarray):
        """[update the configuration to the last generations data]

        Args:
            file (TextIOWrapper): [File to there the data will be written]
            grid (np.ndarray): [new Universe grid]
        """
        self.grid = grid
        toWrite = ' {} {}'.format(str(self.generation).ljust(12), str(self.generationConfigurations).ljust(17))
        
        for c in self.configurations:
            percentage = "{:02.1f}%".format(self.configurations[c] / float (self.generationConfigurations) * 100.0).zfill(5)
            
            toWrite += '{} {} {}'.format("".ljust(len(c)+1), str(self.configurations[c]).ljust(8), percentage.ljust(13))
            self.configurations[c] = 0
        self.generationConfigurations = 0
        toWrite += "\n{}\n".format("-"*len(toWrite))
        file.write(toWrite)


    def isConfiguration(self, x: int, y: int, configuration: int) -> list[bool, list[list]]:
        """[Check wheter the value belongs to a Configuration]

        Args:
            x (int): [x position in Universe]
            y (int): [y position in Universe]
            configuration (int): [number of the configuration to be compared]

        Returns:
            [bool]: [Returns wether it is a configuration or not]
            [list[list]]: [The form of the configuration that belongs to the position in Universe]
        """
        # set initial values for return variables
        flag = True
        toPaint = [0,0]

        # get configuration to be compared to and compare it
        toCompareList = self.configurationsForms[configuration]
        for toCompare in toCompareList:
            flag = True
            for cell in toCompare:
                toPaint = toCompare
                newY = y + cell[1]
                newX = x + cell[0]
                if (0 <= newY < self.grid.shape[0]) and (0 <= newX < self.grid.shape[1]):
                    
                        if self.grid[newY, newX] != 255:
                            flag = False
                            toPaint = [0,0]
                            break
                else:
                    flag = False
                    toPaint = [0,0]
                    break
            if flag:
                return [flag, toPaint]
        
                
        return [flag, toPaint]
    
    

        



