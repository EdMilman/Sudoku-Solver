"""
Edward Milman - emilma01@dcs.bbk.ac.uk
a program to solve simple sudoku problems. user will be prompted to enter a filename of a file
containing a sudoku problem in the form of a list of lists.
"""
import sys
import time


def main():
    # establish loop if more than 1 problem needs to be solved
    loop = True
    while loop:
        # open file
        try:
            file = input("Please enter file name to open (Q to quit):\n")
            if file in {"Q", "q"}:
                sys.exit(0)
            problem = read_sudoku(file)
            # error handling
        except FileNotFoundError as e:
            print("File not found - please try again or enter Q to quit.")
        else:
            print("You have input the following problem:")
            # print input problem
            print_sudoku(problem)
            print("The computer will now attempt to solve the problem...")
            time.sleep(2)
            print("Still thinking about it...")
            time.sleep(2)
            print("I think have it!!")
            time.sleep(1)
            # convert to sets an check if problem can be solved
            sets = convertToSets(problem)
            if solve(sets):
                print("It's solved - I'm a genius!")
            else:
                print("OK - I don't have it :(")
                print("Sorry, the best I could do is this:")
            # convert back to format accepted by printing function
            problem = convertToInts(sets)
            print_sudoku(problem)
            # offer to restart
            print("\nLet's see if I can solve another.")


# function to read a sudoku problem in the form of a 2d array from a file
# param: file - string name of the file
# return: eval - contents of the file
def read_sudoku(file):
    stream = open(file)
    data = stream.readlines()
    stream.close()
    return eval("".join(data))


# creates a 2d array of sets from a 2d array of integers
# if the integer is 0, the set will be {1-9)
# if integer is not 0, the set will contain just that integer
# param: problem - 2d array of integers
# return: converted - a 2d array containing sets
def convertToSets(problem):
    converted = []
    for row in range(len(problem)):
        temp = []
        for col in range(len(problem[row])):
            if problem[row][col] == 0:
                temp.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
            else:
                temp.append({problem[row][col]})
        converted.append(temp)
    return converted


# creates a 2d array of integers from a 2d array of sets
# if the set contains more than 1 element, integer created is 0
# if set containts 1 element, that element is created as an integer
# compliment to convertToSets
# param: problem - 2d array containing sets
# return: converted - 2d array containing integers
def convertToInts(problem):
    converted = []
    for row in range(len(problem)):
        temp = []
        for col in range(len(problem[row])):
            if len(problem[row][col]) == 1:
                for item in problem[row][col]:
                    temp.append(item)
            else:
                temp.append(0)
        converted.append(temp)
    return converted


# given a row number, will return a list of all row/column pairs for that row
# param: rownumber - integer representing the rownumber
# return: list containing tuples representing row/column coordinates
def getRowLocations(rowNumber):
    return [(rowNumber, i) for i in range(9)]


# given a column number, will return a list of all row/column pairs for that row
# param: column - integer representing the column number
# return: list containing tuples representing row/column coordinates
def getColumnLocations(columnNumber):
    return [(i, columnNumber) for i in range(9)]


# given a location tuple, will return the surrounding 8 location tuples
# param: location - integer pair representing a location
# return: box data - list of integer pairs representing locations
def getBoxLocations(location):
    coord = {
        0: (0, 3),
        1: (0, 3),
        2: (0, 3),
        3: (3, 6),
        4: (3, 6),
        5: (3, 6),
        6: (6, 9),
        7: (6, 9),
        8: (6, 9)}
    box_data = []
    for row in range(*coord.get(location[0])):
        for col in range(*coord.get(location[1])):
            box_data.append((row, col))
    return box_data


# given a location of a single element set in an array of sets will removed that element from every
# location provided
# param: problem - 2d array of sets
# param: location - integer pair representing the location of a single element set in problem
# return: count - integer representing the amount of elements removed from problem
def eliminate(problem, location, listOfLocations):
    lst = convertToInts(problem)
    remove_int = lst[location[0]][location[1]]
    count = 0
    for pair in listOfLocations:
        if pair != location and remove_int in problem[pair[0]][pair[1]] and len(problem[pair[0]][pair[1]]) > 1:
            problem[pair[0]][pair[1]].discard(remove_int)
            count += 1
    return count


# will check if an argument is a solved sudoku puzzle
# param: problem - 2d array of sets
# return: boolean - True if puzzle is solved, false otherwise
def isSolved(problem):
    count = 0
    for row in range(len(problem)):
        for col in range(len(problem[row])):
            if len(problem[row][col]) == 1:
                count += 1
    return count == len(problem) * len(problem[0])


# given a 2d array of sets will try and solve the puzzle
# param: problem - 2d array of sets
# return: boolean from isSolved
def solve(problem):
    loop = True
    while loop:
        count = 0
        for row in range(len(problem)):
            for col in range(len(problem[row])):
                elim_locs = getBoxLocations((row, col))
                elim_locs.extend(getRowLocations(row))
                elim_locs.extend(getColumnLocations(col))
                count += eliminate(problem, (row, col), elim_locs)
        if count == 0:
            loop = False
    return isSolved(problem)


# will print to screen a user friendly representation of the problem input
# param: problem - 2d integer array
def print_sudoku(problem):
    sections = len(problem) // 3
    rows = len(problem)
    columns = len(problem[0])
    for row in range(rows):
        if row % 3 == 0:
            print_bar(sections)
        for col in range(columns):
            if col % 3 == 0:
                print("| .", end=" ") if problem[row][col] == 0 else print("| " + str(problem[row][col]), end=" ")
            else:
                print(".", end=" ") if problem[row][col] == 0 else print(problem[row][col], end=" ")
        print("|")
    print_bar(sections)


# helper function for print_sudoku, prints a 'bar' to separate boxes
# param: sections - integer to divide up the problem
def print_bar(sections):
    for i in range(9):
        print("+", end="") if i == 0 or i == 8 else print("-", end="")
    for x in range(sections - 1):
        for x in range(8):
            print("+", end="") if x == 7 else print("-", end="")
    print()


if __name__ == "__main__":
    main()
