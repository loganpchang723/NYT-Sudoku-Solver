#an optimimization of the naive backtracking algorithm by usinig an MRV approach

#NOTE: this was used for unit-testing...all final code was copy and pasted into 'test.py' and some code later changed for debugging purposes

grid = [[0, 5, 9, 1, 8, 0, 7, 0, 6],
          [0, 7, 2, 0, 0, 0, 4, 0, 1],
          [8, 0, 0, 7, 6, 2, 0, 0, 9],
          [7, 0, 1, 0, 0, 5, 8, 4, 0],
          [0, 3, 0, 6, 1, 7, 0, 9, 0],
          [2, 0, 5, 0, 0, 3, 6, 1, 0],
          [9, 2, 0, 4, 0, 0, 0, 3, 8],
          [0, 8, 0, 0, 2, 6, 1, 0, 4],
          [1, 0, 7, 3, 5, 0, 0, 6, 0]]
def print_board(grid):
    for i in range (len(grid)):
        if i%3 == 0 and i!= 0:
            print('- - - - - - - - - -')
        for j in range(len(grid[0])):
            if j%3 == 0 and j!=0:
                print('|', end='')
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j])+' ', end = '')

def is_valid(grid, val, pos):
    #row check
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == val and pos[1] != i:
            return False
    #col check
    for i in range(len(grid)):
        if grid[i][pos[1]] == val and pos[0] != i:
            return False
    #box check
    colBox = pos[1]//3 # 0:(ind 0,1,2); 1:(ind 4,5,6); 2:(int 7,8,9)
    rowBox = pos[0]//3 # 0:(ind 0,1,2); 1:(ind 4,5,6); 2:(int 7,8,9)
    for i in range(rowBox*3, rowBox*3+3):
        for j in range(colBox*3, colBox*3+3):
            if grid[i][j] == val and (i,j) != pos:
                return False
    return True

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

def getCandidates(grid):
    allCans = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                row = rowCandidates(grid)[i]
                col = colCandidates(grid)[j]
                box = boxCandidates(grid)[(i//3,j//3)]
                pos = (i,j)
                allCans[pos] = list(set(row) & set(col) & set(box))
    allCans_sorted = {}
    for coord in sorted(allCans, key = lambda x: len(allCans[x])):
        allCans_sorted[coord] = allCans[coord]
    return allCans_sorted

def empty(grid):
    stack = []
    empties = getCandidates(grid)
    # print(list(empties.keys()))
    for coord in reversed(list(empties.keys())):
        stack.append(coord)
    return stack

def solve(grid, stack, empties):
    if not stack:
        return True
    else:
        (x,y) = stack.pop()
        print((x,y))
    for i in empties[(x,y)]:
        if is_valid(grid,i, (x,y)):
            grid[x][y] = i
            if solve(grid, stack, empties):
                return True
            stack.append((x,y))
    return False


if __name__ == '__main__':
    print('orginal')
    print_board(grid)
    print(getCandidates(grid))
    solve(grid, empty(grid), getCandidates(grid))
    print_board(grid)