import pygame
import random
class Board:
    def __init__(self,width, height) -> None:
        self.size = (width, height)
        self.board = self.createBoard()
    def createBoard(self):
        board = pygame.Surface(self.size)
        squareSize = self.getWidth//8
        self.squares = []
        for row in range(0,self.getHeight, 8):
            for collumn in range(0, self.getWidth, 8):
                rect = pygame.Rect(collumn, row, 8, 8)
                self.squares.append(rect)
                pygame.draw.rect(board, (random.randint(0,245),random.randint(0,245),random.randint(0,245)))
        return board
    def drawBoard(self,screen):
        screen.blit(self.board, (100,100))
                       

    @property
    def getWidth(self):
        return self.size[0]
    @property
    def getHeight(self):
        return self.size[1]