from sudoku_csp import *

b8 = [[1,0,5,0,0,4,0,0,0],
      [0,9,0,0,0,5,0,0,0],
      [0,3,6,0,0,0,0,9,7],
      [7,8,0,1,0,0,3,0,0],
      [0,0,0,0,7,0,0,0,0],
      [0,0,3,0,0,9,0,7,6],
      [6,5,0,0,0,0,8,1,0],
      [0,0,0,8,0,0,0,6,0],
      [0,0,0,3,0,0,4,0,2]]

b9 = [[0,0,7,4,0,0,0,9,3],
      [0,6,0,9,7,0,0,2,0],
      [0,0,2,0,0,0,0,0,0],
      [5,0,0,6,2,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,4,1,0,0,5],
      [0,0,0,0,0,0,2,0,0],
      [0,4,0,0,8,9,0,5,0],
      [3,1,0,0,0,6,8,0,0]]

b10 = [[0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0]]

b11 = [[1,2,3,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,4,5,6],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,7,0,0,0,0,0,0],
       [0,0,8,0,0,0,0,0,0],
       [0,0,9,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0]]

if __name__ == '__main__':
    boards = [b8, b9, b10, b11]
    for b in boards:
        print("Solving board m{}".format(boards.index(b)))
        for row in b:
            print(row)
        print("--------------------------------------------")
        print "GAC reduced domains from MODEL 1"
        sol1 = sudoku_enforce_gac_model_1(b)
        for row in sol1:
            print row
        print "GAC reduced domains from MODEL 2"
        sol2 = sudoku_enforce_gac_model_2(b)
        for row in sol2:
            print row
        print("============================================")
