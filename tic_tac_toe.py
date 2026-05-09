#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 17:37:32 2018

@author: sabbir
"""
# %% Data Structre

import random

board = {'topL': ' ', 'topM': ' ', 'topR': ' ', 'midL': ' ', 'midM': ' ', 'midR': ' ', 'botL': ' ', 'botM': ' ', 'botR': ' '}

positions = [['topL', 'topM', 'topR'], ['midL', 'midM', 'midR'], ['botL', 'botM', 'botR']]
corner_positions = ['topL', 'topR', 'botL', 'botR']
ldiag_positions = ['topL', 'midM', 'botR']
rdiag_positions = ['topR', 'midM', 'botL']

c_position = []
u_position = []

# %% Output Section

def printboard(board):
    print('\n')
    print(board['topL'], ' | ', board['topM'], ' | ', board['topR'])
    print('=-=-=-=-=-=-=-')
    print(board['midL'], ' | ', board['midM'], ' | ', board['midR'])
    print('=-=-=-=-=-=-=-')
    print(board['botL'], ' | ', board['botM'], ' | ', board['botR'])
    print('\n')
    
    
# %% Winner Detection 

def is_winner():
    def decision(plc1, plc2, plc3):
        if board[plc1] == board[plc2] == board[plc3] != ' ':
            return True
        else:
            return False
       
    for i in range(3):
        if decision(*positions[i]):
            return True
        if decision(positions[0][i], positions[1][i], positions[2][i]):
            return True
    if decision(*ldiag_positions):
        return True
    if decision(*rdiag_positions):
        return True
    return False


# %% Check whether a position is empty or not
       
def is_empty(location):
    if board[location] != ' ':
        return False
    else:
        return True

     
# %% Choice Section

def critical_position(position):
     def how_many(location):
          num = 0
          for loc in location:
               if loc in position:
                    num += 1
          if num == 2:
               unique_place = set(location) - set(position)
               unique_place = unique_place.pop()
               if is_empty(unique_place):
                    return unique_place          
     # Checking any critical position for rows & columns
     for ind in range(3):
          critical = how_many(positions[ind])
          if critical:
               return critical
          critical = how_many([positions[0][ind], positions[1][ind], positions[2][ind]])
          if critical:
               return critical   
     # Checking critical position for left diagonal
     critical = how_many(ldiag_positions)
     if critical:
          return critical
     # Checking critical position for right diagonal
     critical = how_many(rdiag_positions)
     if critical:
          return critical
     
         
# %% Main Code

print('First player will play for "X", while the second player will play for "O"')     
print('Enter position as - topL, topM, topR, midL, midM, midR, botL, botM, botR')
while True:
     player = input('Who will play first? (type "c" for computer or "u" for you): ')
     if player == 'c' or player == 'u':
          break
     print('Wrong selection!')
     player = input('Who will play first? (type "c" for computer or "u" for you): ')
     
turn = 'X'

for i in range(9):
    printboard(board)
    
# Computer Choice Section
    if player == 'c':
        choiceNo = len(c_position) + 1
        critical_u = critical_position(u_position)
        critical_c = critical_position(c_position)
        if choiceNo == 1 and i != 0 and is_empty('midM'):
            place = 'midM'
        elif choiceNo == i == 2 or choiceNo == i == 3 or choiceNo == i == 4:
             if c_position[-1] in ldiag_positions:
                  for place in set(corner_positions) - set(ldiag_positions):
                       if is_empty(place) and critical_position(c_position + [place]):
                            break
                            
             else:
                  for place in set(corner_positions) - set(rdiag_positions):
                       if is_empty(place) and critical_position(c_position + [place]):
                            break
        else:
            if critical_c:
                 place = critical_c
            else:
                 if critical_u:
                      place = critical_u
                 elif not corner_positions:
                      place = random.choice(set(board.keys()) - set(c_position) - set(u_position))
                 else:
                      place = random.choice(corner_positions)
                
        c_position.append(place)
        print('Computer has made its choice.')
        player = 'u'
        
# User Choice Section
    else:
        while True:
            print('Which place do you select? ')
            place = input()
            if place in board.keys():
                if is_empty(place):
                    break
                print('The position is not empty. Choose another position.')
            else:    
                print('The position you choose is not defined. Please type correct position.')            

        u_position.append(place)
        player = 'c'
        
# Updating corner position available for computer         
    if place in corner_positions:
        corner_positions.remove(place)   

# Updating the board and alternate the turn        
    board[place] = turn
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X' 
        
# Checking for winner        
    if i >= 4:
        if is_winner():
            if turn == 'X':
                winner = 'O'
            else:
                winner = 'X'
            printboard(board)
            print('{} wins the game!'.format(winner))
            break     
    
else:
    printboard(board)
    print('The match is drawn!')

