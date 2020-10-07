"""
@author: Trevor Stalnaker
File: main.py

The main loop for running Tic-Tac-Toe Quiz Game
"""

import pygame, copy, random
from polybius.graphics import *
from tictactoe import Board

# Character mapping between alphabet characters and their respective
# base 10 number values
charMap = {10:"a",11:"b",12:"c",13:"d",14:"e",15:"f",16:"g",17:"h"}

def decToBase(num, base):
    """Convert a decimal number to a given base"""
    retString = ""
    while num > 0:
        div, rem = divmod(num, base)
        retString = str(charMap.get(rem, rem)) + retString
        num = div
    return retString

def makeQuestions(tilesPerRow):
    """Creates the questions for the board"""

    # Set the possible bases and their probabilities
    bases = [2, 2, 2, 2, 4, 5, 8, 8, 12, 16, 16, 18]

    # Set the range of numbers for conversion (in base 10)
    dec_numbers = [x for x in range(1,1000)]

    # Initiate the questions and answers lists
    questions = []
    answers = []

    # Generate enough questions to fill the board
    for x in range(tilesPerRow*tilesPerRow):

       # Choose a base and a target number
       base = random.choice(bases)
       num = random.choice(dec_numbers)

       # 50% chance of converting from another base to decimal
       # or converting between binary and hexadecimal
       if random.random() > .5:

           # If the other base is binary or hexadecimal
           if base in (2, 16):

               # 25% chance of converting directly between the two
               if random.random() > .75:

                   # Handle the base two case
                   if base == 2:
                       questions.append(decToBase(num, base) + " in base " + str(base) + \
                                        " to base 16")
                       answers.append(decToBase(num, 16))
                       continue

                   # Handle the base sixteen case
                   else:
                       questions.append(decToBase(num, base) + " in base " + str(base) + \
                                        " to base 2")
                       answers.append(decToBase(num, 2))
                       continue
                    
           questions.append(decToBase(num, base) + " in base " + str(base))
           answers.append(num)

       # 50% chance of converting from decimal to another base
       else:
           questions.append(str(num) + " to base " + str(base))
           answers.append(decToBase(num, base))

    # Return the list of questions and answers
    return (questions, answers)

def main():
   """
   Main loop for the program
   """
   # Initialize the module
   pygame.init()
   pygame.font.init()

   # Set the title of the window
   pygame.display.set_caption('Tic-Tac-Toe')

   # Set the tile dimensions and the margins around the board
   tileDims = 150
   boardMargin = 100

   # Specify the number of tiles per row / column
   tilesPerRow = 3

   # Set the amount of time players have to answer questions
   timer = 10#180

   # Calculate an appropriate window size
   dim = tileDims * tilesPerRow + boardMargin * 2
   
   # Get the screen to display the game
   screen = pygame.display.set_mode((dim,dim)) #, pygame.FULLSCREEN)

   # Create an instance of the game clock
   gameClock = pygame.time.Clock()

   # Create the questions and answers for the board
   questions, answers = makeQuestions(tilesPerRow)

   # Create an instance of the Board object
   game = Board(questions,answers,boardOffset=boardMargin, tileDims=tileDims,
                size=tilesPerRow, timer=timer)

   # Set RUNNING to True; the game stops when False
   RUNNING = True

   # Main game loop
   while RUNNING:

      # Increment the clock
      gameClock.tick()

      # Color the screen background
      screen.fill((150,240,255))

      # Execute the game's draw method
      game.draw(screen)

      # Flip the display to the screen
      pygame.display.flip()

      # Event handling, gets all event from the eventqueue
      for event in pygame.event.get():
          
         # Quit the game if the event is of type QUIT
         if (event.type == pygame.QUIT):
            RUNNING = False

         # Allow the game to handle events
         game.handleEvent(event)
      
      # Calculate ticks
      ticks = gameClock.get_time() / 1000

      # Update the game
      game.update(ticks)
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

