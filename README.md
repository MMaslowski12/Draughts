## Introduction
In this repository you can find:

- Rupert: AI model playing checkers better than humans
- Modules needed for Rupert to run properly, that is: Board.py, Engine.py, Game.py, Graphics.py, Neurals(in progress).py, Piece.py, Position.py
- archives.txt automatically saving every move to help Rupert run more efficently
- handwritten digits.ipynb, which is the independent sideproject focusing o creating a neural network distinguishing handwritten digits and 96handwriter - a trained model distinguishing digits with 96% accuracy

## Installation

## Instructions
How to play a game against Rupert:
In order to play against Rupert, you need to run the Rupert.ipynb program
Then, an interface will appear:
![](./pictures/UI.png)
You need to specify your move. To do so, insert four digits sperated with a space:
- First two digits specify the starting position of a piece You want to move
- Another pair of digits specify the ending position of a piece You want to move
- Please specify the position using y and x coordinates(in that specific order), where the upper left corner of a board has coordinates 0 0, the upper right corner - 0 9, lower left corner - 9 0, and the lower right corner - 9 9. Please note the coordinates of those points has been specified by y x notation, the same way they should be inserted.
- Should You be able to capture more than one opponent's piece and therefore do a more complex move, please specify it by insering pairs of y and x coordinates of every 'turning point', including the beginning and the end of the move

Program is set so that bot plays with white pieces by default. Should you want to play as white pieces yourself, please change the True argument to False in a game.play_human() function located at the end of the code.

The AI works with depth four to save time. Should you want to increase its accuracy at the expense of response time, please change it to six in the underlined part of the code below.
![You can change depth to six here](./pictures/depth.png)