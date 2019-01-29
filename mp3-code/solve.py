import numpy as np
import copy
import time

def reduceRows(rows,columns):
    out_rows = []
    for row in rows:
        num_row = row[0]
        pos_rows = row[1]
        for curr_row_idx,curr_row in enumerate(pos_rows):
            for row_idx, row_val in enumerate(curr_row):
                curr_col_options = columns[row_idx]
                pos_cols = False
                for col_idx, curr_col in enumerate(curr_col_options):
                    if curr_col[num_row] == row_val:
                        pos_cols = True
                        break
                if not pos_cols:
                    pos_rows[curr_row_idx] = None
                    break
        reduced_rows = [x for x in pos_rows if x != None]
        out_rows.append((num_row,reduced_rows))
    return out_rows

def getKey(item):
    return len(item[1])

def format(thing):
    sorted_thing = sorted(thing)
    formatted = []
    for row in sorted_thing:
        formatted.append(row[1])
    return formatted

def solve(constraints):
    starttime = time.time()
    possible_row = []
    for idx, x in enumerate(constraints[0]):
        oldSeq = [None] * len(constraints[1])
        out= []
        out = make_combs(out,oldSeq, len(constraints[1]),0,0,0,x)
        possible_row.append((idx,out))
    sorted_possible_row = sorted(possible_row,key=getKey)
    possible_col = []
    for idx, x in enumerate(constraints[1]):
        oldSeq = [None] * len(constraints[0])
        out = []
        out = make_combs(out,oldSeq, len(constraints[0]),0,0,0,x)
        possible_col.append(out)
    for idx,curr in enumerate(possible_col):
        if curr == []:
            possible_col[idx] = [[0]*len(possible_col)]
    rowsSoFar = []
    target = len(possible_row)
    to_be_formatted = solveR(rowsSoFar,sorted_possible_row,possible_col,target)
    endtime = time.time()
    print(endtime-starttime)
    sol = np.array(format(to_be_formatted))
    return sol

def solveR(rowsSoFar, sorted_possible_row, possible_col,target): #recursive
    if len(rowsSoFar) == target:
        return rowsSoFar
    sorted_possible_row_copy = copy.deepcopy(sorted_possible_row)
    sum = 0
    sorted_possible_row_copy = reduceRows(sorted_possible_row_copy,possible_col)
    sorted_possible_row_copy = sorted(sorted_possible_row_copy,key=getKey)
    curr_row_set = sorted_possible_row_copy[0]
    num_row = curr_row_set[0]
    for curr_row in curr_row_set[1]:
        rowsSoFar.append((num_row,curr_row))
        ret = isSafe(rowsSoFar, possible_col)
        if ret[0]:
            child_ret = solveR(copy.deepcopy(rowsSoFar),sorted_possible_row_copy[1:],ret[1],target)
            if child_ret[0]:
                return child_ret
        rowsSoFar = rowsSoFar[:-1]
    return False, None


def isSafe(rowsSoFar, given_possible_col):
    possible_col = copy.deepcopy(given_possible_col)
    if len(rowsSoFar) == 0:
        return True, possible_col
    for row in rowsSoFar:
        num_row = row[0]
        curr_row = row[1]
        for row_idx, row_val in enumerate(curr_row):
            curr_col_options = possible_col[row_idx]
            for col_idx, curr_col in enumerate(curr_col_options):
                if curr_col[num_row] != row_val:
                    curr_col_options[col_idx] = None
            curr_col_options = [x for x in curr_col_options if x != None]
            if len(curr_col_options) == 0:
                return False, None
            possible_col[row_idx] = curr_col_options
    return True, possible_col




    """
    Implement me!!!!!!!
    This function takes in a set of constraints. The first dimension is the axis
    to which the constraints refer to. The second dimension is the list of constraints
    for some axis index pair. The third demsion is a single constraint of the form
    [i,j] which means a run of i js. For example, [4,1] would correspond to a block
    [1,1,1,1].

    The return value of this function should be a numpy array that satisfies all
    of the constraints.


	A puzzle will have the constraints of the following format:


	array([
		[list([[4, 1]]),
		 list([[1, 1], [1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
		 list([[2, 1]]),
		 list([[1, 1], [1, 1]])],
        [list([[2, 1]]),
		 list([[1, 1], [1, 1]]),
		 list([[3, 1], [1, 1]]),
         list([[1, 1], [1, 1]]),
		 list([[5, 1]])]
		], dtype=object)

	And a corresponding solution may be:

	array([[0, 1, 1, 1, 1],
		   [1, 0, 1, 0, 1],
		   [1, 1, 1, 0, 1],
		   [0, 0, 0, 1, 1],
		   [0, 0, 1, 0, 1]])



	Consider a more complicated set of constraints for a colored nonogram.

	array([
	   [list([[1, 1], [1, 4], [1, 2], [1, 1], [1, 2], [1, 1]]),
        list([[1, 3], [1, 4], [1, 3]]),
		list([[1, 2]]),
        list([[1, 4], [1, 1]]),
		list([[2, 2], [2, 1], [1, 3]]),
        list([[1, 2], [1, 3], [1, 2]]),
		list([[2, 1]])],
       [list([[1, 3], [1, 4], [1, 2]]),
        list([[1, 1], [1, 4], [1, 2], [1, 2], [1, 1]]),
        list([[1, 4], [1, 1], [1, 2], [1, 1]]),
		list([[1, 2], [1, 1]]),
        list([[1, 1], [2, 3]]),
		list([[1, 2], [1, 3]]),
        list([[1, 1], [1, 1], [1, 2]])]],
		dtype=object)

	And a corresponding solution may be:

	array([
		   [0, 1, 4, 2, 1, 2, 1],
		   [3, 4, 0, 0, 0, 3, 0],
		   [0, 2, 0, 0, 0, 0, 0],
		   [4, 0, 0, 0, 0, 0, 1],
		   [2, 2, 1, 1, 3, 0, 0],
		   [0, 0, 2, 0, 3, 0, 2],
		   [0, 1, 1, 0, 0, 0, 0]
		 ])


    """

def make_combs(out, oldSeq, lineLength, lastColor, offSet, index, constraints):
    if offSet < lineLength:
        if index < len(constraints):
            curr_constraint = constraints[index]
            color = curr_constraint[1]
            size = curr_constraint[0]

            notSame = lastColor != color
            fitToTheGrid = (offSet + size - 1) < lineLength

            if notSame and fitToTheGrid:
                #add run
                for i in range(size):
                    oldSeq[offSet+i] = color

                out = make_combs(out,oldSeq,lineLength,color,offSet+size,index+1,constraints)

                #remove run
                for i in range(size):
                    oldSeq[offSet+i] = 0
        oldSeq[offSet] = 0
        out = make_combs(out,oldSeq,lineLength,0,offSet+1,index,constraints)
    else:
        if len(constraints) <= index:
            out.append(copy.deepcopy(oldSeq))
    return out
