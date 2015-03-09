from cspbase import *
import itertools

def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then 
       enforce GAC on them pruning values from the variables in the scope of
       these constraints. Return False if a DWO is detected. Otherwise, return True. 
       The pruned values will be removed from the variable object's cur_domain.
       enforce_gac modifies the variable objects that are in the scope of
       the constraints passed to it.'''

    GACQueue = list(constraint_list)
    while GACQueue:
        c = GACQueue.pop(0)
        for v in c.scope:
            for d in v.cur_domain():
                support = c.has_support(v, d)
                if support == False:
                    v.prune_value(d)
                    if v.cur_domain_size() == 0:
                        return False
                    else:
                        for constraint in constraint_list:
                            if v in constraint.scope and constraint not in GACQueue:
                                GACQueue.append(constraint)
    return True

def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       In model_1 you should create a variable for each cell of the
       board, with domain equal to {1-9} if the board has a 0 at that
       position, and domain equal {i} if the board has a fixed number i
       at that cell. 
       
       Model_1 should create BINARY CONSTRAINTS OF NOT-EQUAL between all
       relevant variables (e.g., all pairs of variables in the same
       row, etc.), then invoke enforce_gac on those constraints. All of the
       constraints of Model_1 MUST BE binary constraints (i.e.,
       constraints whose scope includes two and only two variables).

       After creating all variables and constraints you can invoke
       your enforce_gac routine to obtain the GAC reduced current domains
       of the variables.
       
       The ouput should have the same layout as the input: a list of
       nine lists each representing a row of the board. However, now the
       numbers in the positions of the input list are to be replaced by
       LISTS which are the corresponding cell's pruned domain (current
       domain) AFTER gac has been performed.
       
       For example, if GAC failed to prune any values the output from
       the above input would result in an output would be: NOTE I HAVE
       PADDED OUT ALL OF THE LISTS WITH BLANKS SO THAT THEY LINE UP IN
       TO COLUMNS. Python would not output this list of lists in this
       format.
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8]],
       [[1,2,3,4,5,6,7,8,9],[                7],[1,2,3,4,5,6,7,8,9],[                4],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3]],
       [[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9],[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6]],
       [[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                5],[                7],[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9]],
       [[                6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains SO THIS WOULD
       NOT BE the outputted list.
       
       '''

    # Initialize variables
    variables = sudoku_initialize_variables(initial_sudoku_board)

    # Create constraints
    constraints = []

    # Row constrains
    for i in range(9):
        row = sudoku_board_get_row(variables, i)
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                v1 = row[c1]
                v2 = row[c2]
                constr = Constraint(v1.name + v2.name, [v1, v2])
                constr.add_satisfying_tuples(sudoku_gen_satisfying_tuples_model1(v1.cur_domain(), v2.cur_domain()))
                constraints.append(constr)

    # Column constraints
    for i in range(9):
        column = sudoku_board_get_column(variables, i)
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                v1 = column[c1]
                v2 = column[c2]
                constr = Constraint(v1.name + v2.name, [v1, v2])
                constr.add_satisfying_tuples(sudoku_gen_satisfying_tuples_model1(v1.cur_domain(), v2.cur_domain()))
                constraints.append(constr)

    # Sub-square constraints
    for i in range(9):
        subsquare = sudoku_board_get_subsquare(variables, i)
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                v1 = subsquare[c1]
                v2 = subsquare[c2]
                constr = Constraint(v1.name + v2.name, [v1, v2])
                constr.add_satisfying_tuples(sudoku_gen_satisfying_tuples_model1(v1.cur_domain(), v2.cur_domain()))
                constraints.append(constr)

    gac_result = enforce_gac(constraints)

    results = [[None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None]]

    for row in range(9):
        for column in range(9):
            results[row][column] = variables[row][column].cur_domain()

    return results

##############################

def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists
    specifying the board, and generates the same format output as
    sudoku_enforce_gac_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''

    # Initialize variables
    variables = sudoku_initialize_variables(initial_sudoku_board)

    # Create constraints
    constraints = []

    # Row constraints
    for i in range(9):
        scope = row = sudoku_board_get_row(variables, i)
        constr = Constraint('r' + str(i), scope)  
        domains = [var.cur_domain() for var in scope]        
        constr.add_satisfying_tuples(sudoku_gen_satisfying_tuples_model2(domains))
        constraints.append(constr)

    # Column constraints
    for i in range(9):
        scope = row = sudoku_board_get_column(variables, i)
        constr = Constraint('c' + str(i), scope)  
        domains = [var.cur_domain() for var in scope]        
        constr.add_satisfying_tuples(sudoku_gen_satisfying_tuples_model2(domains))
        constraints.append(constr)

    # Subsquare constraints
    for i in range(9):
        scope = row = sudoku_board_get_subsquare(variables, i)
        constr = Constraint('s' + str(i), scope)  
        domains = [var.cur_domain() for var in scope]        
        constr.add_satisfying_tuples(sudoku_gen_satisfying_tuples_model2(domains))
        constraints.append(constr)

    gac_result = enforce_gac(constraints)

    results = [[None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None, None]]

    for row in range(9):
        for column in range(9):
            results[row][column] = variables[row][column].cur_domain()

    return results

##############################
def sudoku_initialize_variables(sudoku_board):
    variables = [[None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None]]

    for row in range(9):
        for column in range(9):
            value = sudoku_board[row][column]
            if value == 0:
                var = Variable('c' + str(row) + str(column), range(1,10))
                variables[row][column] = var
            else:
                var = Variable('c' + str(row) + str(column), [value])
                variables[row][column] = var

    return variables

def sudoku_board_get_row(sudoku_board, i):
    return sudoku_board[i]

def sudoku_board_get_column(sudoku_board, i):
    return [sudoku_board[j][i] for j in range(9)]

def sudoku_board_get_subsquare(sudoku_board, i):
    first_row = (i // 3) * 3
    first_col = (i % 3) * 3
    subsquare = [None] * 9
    for j in range(9):
        subrj = j // 3
        subcj = j % 3
        subsquare[j] = sudoku_board[first_row + subrj][first_col + subcj]
    return subsquare

def sudoku_gen_satisfying_tuples_model1(dom1, dom2):
    tuples = []
    for elem in dom1:
        [tuples.append([elem, x]) for x in dom2 if x != elem]

    return tuples

def sudoku_gen_satisfying_tuples_model2(domains):
    #all_combos = list(itertools.product(*domains))
    #return filter(tuple_unique_elems, all_combos)
    
    for v0 in domains[0]:
        all_vars_domain = set(range(1,10)).difference([v0])
        for v1 in set(domains[1]).intersection(all_vars_domain):
            all_vars_domain = set(all_vars_domain).difference([v1])
            for v2 in set(domains[2]).intersection(all_vars_domain):
                all_vars_domain = set(all_vars_domain).difference([v2])
                for v3 in set(domains[3]).intersection(all_vars_domain):
                    all_vars_domain = set(all_vars_domain).difference([v3])
                    for v4 in set(domains[4]).intersection(all_vars_domain):
                        all_vars_domain = set(all_vars_domain).difference([v4])
                        for v5 in set(domains[5]).intersection(all_vars_domain):
                            all_vars_domain = set(all_vars_domain).difference([v5])
                            for v6 in set(domains[6]).intersection(all_vars_domain):
                                all_vars_domain = set(all_vars_domain).difference([v6])
                                for v7 in set(domains[7]).intersection(all_vars_domain):
                                    all_vars_domain = set(all_vars_domain).difference([v7])
                                    for v8 in set(domains[8]).intersection(all_vars_domain):
                                        tuples.append((v0,v1,v2,v3,v4,v5,v6,v7,v8))
    return tuples

def tuple_unique_elems(t):
    uniq = []
    for elem in t:
        if elem not in uniq:
            uniq.append(elem)
        else:
            return False
    return True

    