from selenium import webdriver
from time import sleep
from datetime import date

#This is a function that completes all 3 daily Sudoku puzzles (in order of easy, medium, and hard difficulties) on the New York Times website.

#This function will scrape the website for the unsolved board, use a MRV backtracking algorithm to solve the puzzle, and manually input the solution into the puzzle on the website
#After solving each puzzle, the program will note the time on the puzzle timer on the website and continue solving the next puzzle
#After completing all 3 daily puzzles, the program will print the original and solved boards for each puzzles along with the time it took to solve and input the answers onto the webstie puzzle itseldf
#The printed unsolved and solved puzzles, as well as the timers, will put compiled in 'sudokuLog.txt'

#test.py: collection of all relevant functions and a driver to run proper code (main src)

#blank grid to be filled and later solved
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]

#function to print board as 9x9 matrix with dilineations between each 3x3 box
#(from 'optimAlgo.py')
def print_board(grid, openF):
    for i in range (len(grid)):
        if i%3 == 0 and i!= 0:
            openF.write('- - - - - - - - - -\n')#print horizontal borders
        for j in range(len(grid[0])):
            if j%3 == 0 and j!=0:
                openF.write('|') #print vertical borders
            if j == 8:
                openF.write(str(grid[i][j])+'\n') #print the last column value in the current row and go to the next line
            else:
                openF.write(str(grid[i][j])+' ') #print the current row and current column value

#function to scrape board from website (from 'scraper.py')
#returns a string list where the i+1-th string reprsents the i+1-th row of the board and the j+1-th character in the string is the digit in the j+1-th column of the i+1-th row
def scrape_board(driver, difficulty):
    boardArray = []
    link = "https://www.nytimes.com/puzzles/sudoku/"+difficulty #URL depending on difficulty level (easy, medium, hard)
    driver.get(link) #navigate to above URL
    stringRep = ''
    for i in range(1, 82):
        elem = driver.find_element_by_xpath(
            '//*[@id="pz-game-root"]/div[2]/div/div[1]/div/div/div/div[' + str(i) + ']').get_attribute('aria-label') #get numeric value of each cell on the board
        digit = '0' #use '0' to represent an empty cell
        if elem != 'empty':
            digit = elem
        stringRep += digit #append each digit in a row to a string
        if i % 9 == 0: #once done reading all row values, add it to the final string list and reset the string reprsentation of each row
            boardArray.append(stringRep)
            stringRep = ''
    return boardArray

#function to load the values from the string list from scrape_board into grid
def load_board(grid, boardArray, difficulty, openF):
    allCaps = difficulty.upper() #using the difficulty level in all caps to print out
    for i in range (0,9):
        row = boardArray[i]
        for j in range(0,9):
            grid[i][j] = int(row[j]) #read the j+1-th character from the i+1th string and put it in the i-th row and j-th column as an int
    openF.write(allCaps+': ORIGINAL BOARD\n')
    print_board(grid, openF)

#function to check if the current value being tried at 'pos' is a valid move
#return True if the value being tried is a valid move, else return False
#(from 'optimAlgo.py')
def is_valid(grid, val, pos):
    #row check: check if value being tested already exists in the row of 'pos'
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == val and pos[1] != i:
            return False
    #col check: check if value being tested already exists in the column of 'pos'
    for i in range(len(grid)):
        if grid[i][pos[1]] == val and pos[0] != i:
            return False
    #box check: check if value being tested already exists in the smaller 3x3 'box' that 'pos' is located in
    colBox = pos[1]//3 # 0:(ind 0,1,2); 1:(ind 4,5,6); 2:(int 7,8,9)
    rowBox = pos[0]//3 # 0:(ind 0,1,2); 1:(ind 4,5,6); 2:(int 7,8,9)
    for i in range(rowBox*3, rowBox*3+3):
        for j in range(colBox*3, colBox*3+3):
            if grid[i][j] == val and (i,j) != pos:
                return False
    return True

#get all candidates in each row (same for each cell in the row)
#return dict with i:canList where i is the i+1-th row of the board and canList is the list of candidates in each row
#(from 'optimAlgo.py')
def rowCandidates(grid):
    rows = {}
    for i in range(len(grid)):
        canList = []
        for j in range (1,10):
            canList.append(j)
        for j in range (len(grid[0])):
            if grid[i][j] != 0:
                canList.remove(grid[i][j])
        rows[i] = canList
    return rows

#get all candidates in each row (same for each cell in the column)
#return dict with j:canList where j is the j+1-th column of the board and canList is the list of candidates in each column
#(from 'optimAlgo.py')
def colCandidates(grid):
    cols = {}
    for i in range(len(grid[0])):
        canList = []
        for j in range(1, 10):
            canList.append(j)
        for j in range(len(grid)):
            if grid[j][i] != 0:
                canList.remove(grid[j][i])
        cols[i] = canList
    return cols

#get all candidates in each 'box' (same for each cell in the box)
#return dict with (i,j):canList where each box is the i+1th from the left and the j+1th from the top and canList is the list of candidates in each row
#(from 'optimAlgo.py')
def boxCandidates(grid):
    boxs = {}
    canList = []
    for boxX in range (0,3):
        for boxY in range(0,3):
            canList = [1,2,3,4,5,6,7,8,9]
            for i in range (boxX*3, boxX*3+3):
                for j in range(boxY * 3, boxY*3 + 3):
                    if grid[i][j] != 0:
                        canList.remove(grid[i][j])
            boxs[(boxX, boxY)] = canList
    return boxs

#gets candidates for each open space by taking intersection of row, column, and box candidates of each empty cell
#returns a dict in from (x,y):cans where the empty cell is in position (x+1, y+1) and cans is the list of candidates for that empty cell
# (the returned dict is sorted by cells with the least candidates to cells with the most candidates)
#(from 'optimAlgo.py')
def getCandidates(grid):
    allCans = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                row = rowCandidates(grid)[i] #row candidates for empty cell
                col = colCandidates(grid)[j] #column candidates for empty cell
                box = boxCandidates(grid)[(i//3,j//3)] #box candidates for empty cell
                pos = (i,j)
                allCans[pos] = list(set(row) & set(col) & set(box)) #get intersection of all 3 candidate lists
    allCans_sorted = {}
    for coord in sorted(allCans, key = lambda x: len(allCans[x])):
        allCans_sorted[coord] = allCans[coord] #sorted by cells with least to most candidates
    return allCans_sorted

#solves the original board via an MRV backtracking algorithm
#If empty cells exist, the program tries to fill empty cells with the least number of candidates at each step (branch) of the backtracking/solving
#return True if puzzle is solved, False if puzzle cannot be solved (invalid board)
#(from 'optimAlgo.py')
def solve(grid):
    empties = getCandidates(grid)
    stack = list(empties.keys())
    if len(stack) == 0: #if no empty cells remain, puzzle is solved
        return True
    else:
        (x,y) = stack[0] # else, take the cell which currently has the least number of candidates in left-to-right, top-to-bottom order
    for i in empties[(x,y)]: #try each candidate for the cell trying to be solved
        if is_valid(grid,i, (x,y)): #check if tried value is valid or not
            grid[x][y] = i
            if solve(grid): #recursively check if tried value creates a valid board
                return True
            grid[x][y] = 0 #if tried value is incorrect, reset its value in grid so it gets retried for solving
    return False #if none of the current cells candidates work, the current board is invalid and a previously-filled cell must be changed, or if all possible candidates were tried, the board is invalid

#using the solved board, click on the input panel on the website to fill in the missing values
#(from solutionEnterer.py)
def fill_solution(grid):
    for i in range(1, 82):
        box = driver.find_element_by_xpath(
            '//*[@id="pz-game-root"]/div[2]/div/div[1]/div/div/div/div[' + str(i) + ']')
        fill = box.get_attribute('aria-label')
        if fill == 'empty': #if the cell is empty on the game board on the website
            ind = i-1
            fillValue = grid[ind//9][ind%9]
            button = driver.find_element_by_xpath( #click on the input pad on the game website corresponding to the value in the now-solved 'grid'
                '//*[@id="pz-game-root"]/div[2]/div/div[3]/div/div[2]/div['+str(fillValue)+']')
            driver.execute_script("arguments[0].click()", box)
            driver.execute_script("arguments[0].click()", button)

#checks if original board was solved (doesn't contain any 0's)
#if solved, will print solved board on 'sodukuLog.txt' and fill it in on the website
def is_solved(grid, difficulty, openF):
    allCaps = difficulty.upper()
    if solve(grid) and not any(0 in sublist for sublist in grid):
        openF.write(allCaps+': SOLVED!\n')
        print_board(grid, openF)
        fill_solution(grid)
    else:
        openF.write("NO SOLUTION\n")

#driver; executable script
if __name__ == '__main__':
    difficulties = ['easy', 'medium', 'hard']
    times = []
    driver = webdriver.Chrome() #start a driver on Chrome
    openF = open('sudokuLog.txt', 'a') #begin writing to 'sudokuLog.txt'
    openF.write('NEW YORK TIMES SUDOKU PUZZLES AND SOLUTIONS FOR '+str(date.today())+'\n') #heading which includes the date
    openF.write('\n')
    for difficulty in difficulties: #for each difficulty (easy, medium, hard)....
        scraped = scrape_board(driver, difficulty) #scrape the board from the website
        load_board(grid, scraped, difficulty, openF) #load the scraped board into 'grid' and onto 'sudokuLog.txt'
        openF.write('\n')
        is_solved(grid, difficulty, openF) #solve the board; if solvable, input the solution on the website and onto 'sudokuLog.txt'
        timer = driver.find_element_by_class_name('su-timer__value') #scrape the timer value from the website
        times.append(timer.text) #add timer value to a list which will hold all 3 timer values
        openF.write('\n')
        sleep(3)
    driver.quit()
    for i in range(0,3):
        diff = difficulties[i].upper()
        openF.write('SOLVED '+diff+' PUZZLE IN '+str(times[i])+'\n') #print out how long it took to solve each difficulty onto 'sudokuLog.txt'
    openF.write('\n')
    openF.close()