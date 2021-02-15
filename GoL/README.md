# Conway's Game of Life Simulator

A simulator of life based on Conway's Game of Life. Implemented using Python. The simulator runs with 3 basic concepts:
- Rules of life
- Graphic Simulation
- Configurations

## Instructions

To run the simiulator, you must give an input file with .txt as its extension. If no input file is detected, the simulation will use its predetermined values:
- Universe size: 100 Rows x 100 Columns
- Number of Generations: 200

## Input File

The input file consist of 3 parts:
- The first line has 3 int numbers separated by spaces in the current order:
	- N: Number of Rows
	- M: Number of Columns
	- F: Number of Generations
- The next lines are the cells that are initially alive, creating configurations if in the right position.

The file must be placed in the Files folder and just be given the name of the file when running the simulation:

	python conway.py exampleInput.txt

## Output File

The output file will be placed in the Files folder with the extension .out. The output file will have a header with the data titles:
- Generation
- Number of total Configurations
- For each Configuration its amount and percentage of the total Configuration

