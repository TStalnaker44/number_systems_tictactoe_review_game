"""
@author: Trevor Stalnaker
File: tictactoe.py

Creates a class that models the complete tic-tac-toe game
"""

import pygame
from polybius.graphics import TextBox, Button, ProgressBar

class Board():
    """Class that models the tic-tac-toe board"""

    def __init__(self, questions, answers, size=3, boardOffset=100,
                 tileDims=20, timer=30):
        """Initializes the board and game"""

        # Make logical assertions about questions
        assert len(questions) == len(answers)
        assert size*size == len(questions)

        # Create a list to hold tiles
        self._board = []

        self._answerTime = timer
        self._questionTimer = timer

        # Create the question box
        self._questionBox = TextBox("", (boardOffset, 10 + boardOffset + tileDims*3),
                                         pygame.font.SysFont("Times New Roman",
                                                             24), (0,0,0))

        # Create the correct button
        self._correctButton = Button("Correct", (0,0), pygame.font.SysFont("Times New Roman",20), (0,0,0),
                          (0,255,0),30, 150)

        # Create the incorrect button
        self._incorrectButton = Button("Incorrect", (0,0), pygame.font.SysFont("Times New Roman",20), (0,0,0),
                          (255,0,0),30, 150)

        # Create the timer bar
        self._timer = ProgressBar((10,10), tileDims*3, timer, timer)

        # Position the correct button on the screen
        self._correctButton.center(cen_point=(1/4,None))
        self._correctButton.setPosition((self._correctButton.getX(), boardOffset+tileDims*3+50))

        # Position the incorrect button on the screen
        self._incorrectButton.center(cen_point=(3/4,None))
        self._incorrectButton.setPosition((self._incorrectButton.getX(), boardOffset+tileDims*3+50))

        # Position the timer bar on the screen
        self._timer.center(cen_point=(1/2, None))
        self._timer.setPosition((self._timer.getX(), boardOffset//2))

        # Create the tiles
        for x in range(size):
            for y in range(size):
                self._board.append(Tile((boardOffset + y*tileDims,
                                 boardOffset + x*tileDims),
                                 questions[x*size + y], answers[x*size + y],
                                 tileDims))

        # Boolean flag; True when question is on screen
        self._questionDisplayed = False

        # The current selected tile
        self._currentTile = None

        # Boolean flag; True on Player 1's turn
        self._turn = True

        # List of tiles that already have marks
        self._markedTiles = []


    def getTile(self, row, column):
        """Returns the tile at the given row and column"""
        return self._board[row][column]

    def getQuestion(self, row, column):
        """Returns the question at the given row and column"""
        return self.getTile(row, column).getQuestion()

    def getAnswer(self, row, column):
        """Returns the answer at the given row and column"""
        return self.getTile(row, column).getAnswer()

    def getTiles(self):
        """Returns a list of all tiles on the board"""
        return self._board

    def draw(self, screen):
        """Draws the board and game to the screen"""
        for t in self.getTiles():
            t.draw(screen)
        
        if self._questionDisplayed:
            self._questionBox.center(cen_point=(1/2,None))
            self._questionBox.draw(screen)
            self._correctButton.draw(screen)
            self._incorrectButton.draw(screen)
            self._timer.draw(screen)

    def handleEvent(self, event):
        """Handles events for the board and game"""
        for t in self.getTiles():
            t.handleEvent(event, self)

        if self._questionDisplayed:
            self._correctButton.handleEvent(event, self.correct)
            self._incorrectButton.handleEvent(event, self.incorrect)

    def correct(self):
        """Mark the current tile and change turns
        on a correct answer"""
        if self._turn:
            self._currentTile.mark("x")
        else:
            self._currentTile.mark("o")
        self._questionDisplayed = False
        self._questionTimer = self._answerTime
        self._turn = not self._turn

    def incorrect(self):
        """Change turns on an incorrect answer"""
        self._questionDisplayed = False
        self._questionTimer = self._answerTime
        self._turn = not self._turn

    def update(self, ticks):
        """Update the board and game based on passed time"""
        if self._questionDisplayed:
            if self._questionTimer < 0:
                self._questionTimer = self._answerTime
                self.incorrect()
            else:
                self._questionTimer -= ticks
            self._timer.setProgress(self._questionTimer)
            
          
class Tile():
    """Class modelling a tile object"""

    def __init__(self, pos, question, answer, tileDims):
        """Initialize the tile"""

        self._rect = pygame.Rect(pos[1], pos[0], tileDims, tileDims)
        self._question = question
        self._answer = answer
        self._marked = ""

    def getQuestion(self):
        """Get the question on the tile"""
        return self._question

    def getAnswer(self):
        """Get the answer on the tile"""
        return self._answer

    def getRect(self):
        """Get the collide rect for the tile"""
        return self._rect

    def draw(self, screen):
        """Draw the tile to the screen"""
        pygame.draw.rect(screen, (0,120,120),self.getRect(),1)
        if self._marked == "x":
            pygame.draw.line(screen, (0,120,120), self._rect.topleft,
                             self._rect.bottomright, 2)
            pygame.draw.line(screen, (0,120,120), self._rect.topright,
                             self._rect.bottomleft, 2)
        if self._marked == "o":
            pygame.draw.circle(screen, (0,120,120), self._rect.center,
                               self._rect.width//3,2)

    def handleEvent(self, event, game):
        """Handle events on the tile"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and \
           self._rect.collidepoint(event.pos):
            if self._marked == "":
                game._questionBox.setText(self.getQuestion())
                print(self.getAnswer()) # Print the answer to the console for checking
                game._questionDisplayed = True
                game._currentTile = self
                

    def mark(self, sym):
        """Mark the tile with a provided symbol"""
        self._marked = sym

        
                
        
            
