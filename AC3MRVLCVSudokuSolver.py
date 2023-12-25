from AC3 import *
from random import choice
from collections import defaultdict
from SudokuCSP import SudokuCSP
import numpy as np

# AC3 filtering with Minimum Remaining Values and Least Constraining Value
# ordering
class AC3MRVLCVSudokuSolver():
    def __addEdge__(self, i, j, adjList):
        k = i // 3 * 3 + j // 3
        for num in range(9):
            # bel 3ard
            if num != i:
                adjList[(i, j)].add((num, j))
            # bel tool
            if num != j:
                adjList[(i, j)].add((i, num))
            row = num//3 + k//3 * 3
            col = num%3 + k%3 * 3
            # boxes 
            if row != i or col != j:
                adjList[(i, j)].add((row, col))

    def buildCspProblem(self, board):
        adjList = defaultdict(set)
        # contraints : boxes , row we collumn
        for i in range(9):
            for j in range(9):
                self.__addEdge__(i, j, adjList)
        # list of coordinates (i,j) if i,j wasnt assigned
        variables = []
        assigned = []

        # dict : key = coordinate, val = set of available numbers
        domains = defaultdict(set)
        for i in range(9):
            for j in range(9):
                if board[i][j] == '0':
                    domains[(i, j)] = set(range(9))
                    variables.append((i, j))
                else:
                    domains[(i, j)] = set([int(board[i][j]) - 1])
                    assigned.append((i, j))
        return SudokuCSP(variables, adjList, domains), assigned

    def count_conflict(self, csp, Xi, x):
        cnt = 0
        for X in csp.adjList[Xi]:
            if x in csp.domains[X]:
                cnt += 1
        return cnt

    def popMin(self, array, key):
        minimum, idx = float("inf"), 0
        for i in range(len(array)):
            if key(array[i]) < minimum:
                idx = i
                minimum = key(array[i])
        array[idx], array[-1] = array[-1], array[idx]
        return array.pop()

    def solveSudoku(self, board):
        # 2d array of strings
        #board = board.tolist()
        for i in range(9):
            for j in range(9):
                board[i][j] = str(board[i][j])
        # Build CSP problem
        csp, assigned = self.buildCspProblem(board)
        # csp obj : variables, assigned, domains


        # Enforce AC3 on initial assignments
        if not AC3(csp, makeArcQue(csp, assigned)):
            return False
        # If there's still uncertain choices
        uncertain = []
        for i in range(9):
            for j in range(9):
                if len(csp.domains[(i, j)]) > 1:
                    uncertain.append((i, j))
        # Search with backtracking
        if not self.backtrack(csp, uncertain):
            return False
        # Fill answer back to input table
        for i in range(9):
            for j in range(9):
                if board[i][j] == '0':
                    assert len(csp.domains[(i, j)]) == 1
                    board[i][j] = str(csp.domains[(i, j)].pop() + 1)
        for i in range(9):
            for j in range(9):
                board[i][j] = int(board[i][j])
        
        # 2d array of int
        return True

    def backtrack(self, csp, uncertain):
        if not uncertain:
            return True
        
        # MRV
        X = self.popMin(uncertain, key=lambda X: len(csp.domains[X]))
        
        # X is coord of the Min Rem Poss Vals in Dom

        removals = defaultdict(set)

        # LCV
        domainlist = list(csp.domains[X])
        domainlist.sort(key=lambda x: self.count_conflict(csp, X, x))

        for x in domainlist:
            # first iter x is the LCV -> 0 : 8
            domainX = csp.domains[X]
            csp.domains[X] = set([x])
            # hina ba2a bafdal ashta8al AC3 : remove from domain
            if AC3(csp, makeArcQue(csp, [X]), removals):
                # then backtrack le7ad materga3 min el recursion
                solved = self.backtrack(csp, uncertain)
                if solved:
                    return True
            csp.restore_domains(removals)
            csp.domains[X] = domainX
        uncertain.append(X)
        return False
