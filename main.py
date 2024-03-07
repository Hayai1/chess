
import pygame
import sys


class Square:
    def __init__(self, colour, rect) -> None:
        self.colour = colour
        self.square = pygame.Surface((48,48))
        self.rect = rect
        self.piece = None
        self.relationShips = { 'up': None, 'down': None}
    def draw(self, board):
        
        pygame.draw.rect(self.square, self.colour, (0,0, 48, 48))
        board.blit(self.square, (self.rect.x, self.rect.y))

    def setPiece(self, piece):
        self.piece = piece

class Board:
    def __init__(self,width, height) -> None:
        self.size = (width, height)
        self.squares = []
        self.board = self.createBoard(48)
        self.pieces = []
        self.getPieces()
        self.hoveringSquare = None
        self.pickedUpPiece = None
        self.pieceHome = None
    def getPieces(self):
        pawn = Pawn('black', self.squares[0].rect.x,self.squares[0].rect.x)
        self.squares[0].setPiece(pawn)
        self.pieces.append(pawn)
    def createBoard(self, squareSize):
        board = pygame.Surface(self.size)
        white = True
        for row in range(0,self.getHeight, squareSize):
            white = not white
            for collumn in range(0, self.getWidth, squareSize):
                rect = pygame.Rect(collumn, row, squareSize, squareSize)
                if not white:
                    square = Square((118,150,86), rect)#black
                elif white:
                    square = Square((238,238,210), rect)#white
                white = not white              
                self.squares.append(square)
                square.draw(board)      
        return board
    
    def update(self, cursorRect):
        for square in self.squares:
            if pygame.Rect.colliderect(cursorRect, square.rect):
                self.hoveringSquare = square
            square.draw(self.board)
            
        if self.pickedUpPiece != None:
            self.pickedUpPiece.rect.x,self.pickedUpPiece.rect.y = cursorRect.x, cursorRect.y
        for piece in self.pieces:
            piece.draw(self.board)
            


    def draw(self,screen):
        screen.blit(self.board, (0,0))

    def pickUpPiece(self):
        piece = self.hoveringSquare.piece
        if piece != None:
            self.pickedUpPiece = piece
        self.pieceHome = self.hoveringSquare

    def putDownPiece(self):
        location = self.hoveringSquare
        location.setPiece(self.pickedUpPiece)
        self.pickedUpPiece.setPostion(location.rect.x, location.rect.y)
        self.pickedUpPiece = None
        self.pieceHome = None

    @property
    def getWidth(self):
        return self.size[0]
    @property
    def getHeight(self):
        return self.size[1]

class Piece:
    def __init__(self, colour, x, y):
        self.colour = colour
        self.rect = pygame.Rect(48/4+x,48/4+y,48/2,48/2)
    def draw(self, board):
        pygame.draw.rect(board, self.colour, self.rect)
    def update():
        pass
    def setX(self, x):
        self.rect.x = x
    def setY(self, y):
        self.rect.y = y
    def setPostion(self,squareX,squareY):
        self.rect.x, self.rect.y = 48/4+squareX,48/4+squareY


class Pawn(Piece):
    def __init__(self, colour, x, y):
        super().__init__(colour, x, y)
        self.direction = self.getDirection(colour)
        self.possibleTravelSquares = []
    def getDirection(self,colour):
        if colour == 'white':
            direction = 'forward'
        elif colour == 'black':
            direction = 'backwards'
        return direction
    def setPossibleTravelSquares(self, *kwags):
        for square in kwags:
            self.possibleTravelSquares.append(square)

class Cursor:
    def __init__(self):
        self.rect = pygame.Rect(0,0,10,10)
    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
    def draw(self,board):
        pygame.draw.rect(board, (255,0,0), self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.board = Board(48*8,48*8)
        self.cursor = Cursor()
        self.gameLoop()

    def gameLoop(self):
        # -------- Main Program Loop -----------
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.pickUpPiece()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.board.putDownPiece()
                    
            self.screen.fill((0,0,0))

            self.board.update(self.cursor.rect)
            self.board.draw(self.screen)
            
            self.cursor.update()
            self.cursor.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()