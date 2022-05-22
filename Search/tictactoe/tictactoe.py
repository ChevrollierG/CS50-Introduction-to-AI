"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X=0
    count_O=0
    count_EMPTY=0
    for i in board:
        count_EMPTY+=i.count(EMPTY)
        count_X+=i.count(X)
        count_O+=i.count(O)
    if(count_EMPTY==9):
        return X
    elif(count_X==count_O):
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result=set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j]==EMPTY):
                result.add((i,j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if(action[0]<0 or action[1]>2 or action[1]<0 or action[1]>2 or board[action[0]][action[1]]!=EMPTY):
        raise NameError("Action invalid")
    else:
        result=copy.deepcopy(board)
        result[action[0]][action[1]]=player(board)
        return result
                    
    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    count1=0
    count2=0
    for i in range(len(board)):
        if(board[i].count(X)==3):
            return X
        elif(board[i].count(O)==3):
            return O
        if(board[i][i]==X):
            count1+=1
        elif(board[i][i]==O):
            count1-=1
        if(board[len(board)-1-i][len(board)-1-i]==X):
            count2+=1
        if(board[len(board)-1-i][len(board)-1-i]==O):
            count2-=1
    if(count1==3):
        return X
    elif(count1==-3):
        return O
    elif(count2==3):
        return X
    elif(count2==-3):
        return O
    count3=0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[j][i]==X):
                count3+=1
            elif(board[j][i]==O):
                count3-=1
        if count3==3:
            return X
        elif count3==-3:
            return O
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    test=False
    if(winner(board)!=None):
        test=True
    count1=0
    for i in board:
        count1+=i.count(EMPTY)
    if(count1==0):
        test=True
    return test


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result=winner(board)
    if(result==X):
        return 1
    elif(result==O):
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board)):
        return None
    else:
        list1=[]
        for i in actions(board):
            list1.append((i,MinValue(result(board,i))))
        list1.sort(key=lambda x:x[1])
        return list1[0][0]
    

def MinValue(board):
    if(terminal(board)):
        return utility(board)
    else:
        v=1000
        for i in actions(board):
            v=min(v,MaxValue(result(board,i)))
        return v


def MaxValue(board):
    if(terminal(board)):
        return utility(board)
    else:
        v=-1000
        for i in actions(board):
            v=max(v,MinValue(result(board,i)))
        return v
    
