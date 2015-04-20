# Gregory Perkins
# CS 472 - Term Project
# Connect 4 - Minimax, Alpha Beta search

import pygame as p
import sys


size = (width,height) = 640,480
run = 1
winnerFound = False
blackWin = False
redWin = False

pieceArray = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0]]

firstRowAvailable = [5,5,5,5,5,5,5]

class Piece(p.sprite.Sprite):
    def __init__(self, pType, x, y):
        self.black = p.image.load("res/pieceB.png")
        self.red = p.image.load("res/pieceR.png")
        p.sprite.Sprite.__init__(self)
        self.pos = [x,y]
        if (pType == 1): self.image = self.black
        elif (pType == 2): self.image = self.red
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        
    def update(self, screen):
        screen.blit(self.image, self.pos)
        
class NewPiece(p.sprite.Sprite):
    def __init__(self):
        self.image = p.image.load("res/pieceR.png")
        p.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x=10
        self.pos = 0
        self.direction = ""
        
    def update(self):
        if (self.direction =="right" and self.pos <6):
            self.pos += 1
            self.direction = ""
        elif (self.direction =="left" and self.pos > 0):
            self.pos -= 1
            self.direction = ""
        self.rect.x = 10 + self.pos*91.5
        #screen.blit(self.image, self.rect)
        

Pieces = p.sprite.Group()      
    
def pieceSetup(screen):
    ypos = 68.6
    for line in pieceArray:
        xpos = 10
        for piece in line:
            if (piece != 0):
                Pieces.add(Piece(piece, xpos, ypos))
            xpos += 91.5
        ypos+=68.6
 
def place(col, pieceType):
    row = firstRowAvailable[col]
    if row<0: print("Column is full!")
    else:
        pieceArray[row][col] = pieceType
        firstRowAvailable[col] -=1
        #print firstRowAvailable
#     lastline = pieceArray[0]
#     for line in pieceArray:
#         if line[newPiece.pos] != 0:
#             break
#         else:
#             lastline = line
#             
#     lastline[newPiece.pos] = 2

def dePlace(col):
    row = firstRowAvailable[col]
    if row >= 6: print("Column is already empty!")
    firstRowAvailable[col] +=1
    row = firstRowAvailable[col]
    pieceArray[row][col] = 0   
        
def getWinner():
    global winnerFound
    redCount = 0
    blackCount = 0
    for row in range(0,6):
        for col in range(3,7):
            redCount = 0
            blackCount = 0
            for val in range(0,4):
                if pieceArray[row][col-val] == 2:
                    redCount +=1
                elif pieceArray[row][col-val] == 1:
                    blackCount +=1
            if redCount == 4:
                winnerFound = True
                return 2
            elif blackCount == 4:
                winnerFound = True
                return 1   
    for col in range(0,7):
        for row in range(3,6):
            redCount = 0
            blackCount = 0
            for val in range(0,4):
                if pieceArray[row-val][col] == 2:
                    redCount +=1
                elif pieceArray[row-val][col] == 1:
                    blackCount +=1
            if redCount == 4:
                winnerFound = True
                print("win")
                return 2
            elif blackCount == 4:
                winnerFound = True
                return 1  

increment = [0,1,4,32,128,512]
def getIncrement(redCount, blackCount, pieceType):
    if redCount == blackCount:
        if pieceType == 2:
            return -1
        return 1
    elif redCount < blackCount:
        if pieceType == 2:
            return increment[blackCount] - increment[redCount]
        return increment[blackCount+1] - increment[redCount]
    else:
        if pieceType == 2:
            return -increment[redCount+1] + increment[blackCount]
        return -increment[redCount] + increment[blackCount]
    
    
    
def getHeuristic(pieceType, col, depth, maxDepth):
    score = 0
    row = firstRowAvailable[col] + 1
    global redWin
    global blackWin
    
    ####### ROW
    redWin = False
    blackWin = False
    redCount =0
    blackCount = 0
    boardRow = pieceArray[row]
    cStart = col-3
    colStart = cStart if cStart>=0 else 0
    colEnd = 4 - (colStart - cStart)
    for c in range(colStart, colEnd):
        redCount=0
        blackCount=0
        for val in range(0,4):
            if boardRow[c+val] == 2: redCount +=1
            elif boardRow[c+val]== 1: blackCount +=1
        if redCount == 4:
            redWin = True
            if depth <=2: return -sys.maxint - 1
        elif blackCount ==4:
            blackWin = True
            if depth <= 2: return sys.maxint -1
        score += getIncrement(redCount, blackCount, pieceType)
        
    ######## COLUMN
    redCount= 0
    blackCount = 0
    rowEnd = min(6, row+4)
    for r in range(row, rowEnd):
        if pieceArray[r][col] == 2: redCount += 1
        elif pieceArray[r][col] == 1: blackCount += 1
    if redCount == 4:
        redWin = True
        if depth <=2: return -sys.maxint - 1
    elif blackCount ==4:
        blackWin = True
        if depth <= 2: return sys.maxint -1    
    score += getIncrement(redCount, blackCount, pieceType)
    
    ######## major diagonal
    minValue = min(row,col)
    rowStart = row - minValue
    colStart = col-minValue
    c = colStart
    for r in range(rowStart, 3):
        if c > 3: break
        redCount = 0
        blackCount = 0
        for val in range(0,4):
            if pieceArray[r+val][c+val] == 2: redCount +=1
            elif pieceArray[r+val][c+val] == 1: blackCount +=1
        if redCount == 4:
            redWin = True
            if depth <=2: return -sys.maxint - 1
        elif blackCount ==4:
            blackWin = True
            if depth <= 2: return sys.maxint -1    
        score += getIncrement(redCount, blackCount, pieceType)
        c+=1
    
    ####### minor diagonal
    minValue = min(5-row, col)
    rowStart = row+minValue
    colStart = col - minValue
    for c in range(colStart, 4):
        if r < 3: break
        redCount = 0
        blackCount = 0
        for val in range(0,4):
            if pieceArray[r-val][c+val] == 2: redCount +=1
            elif pieceArray[r-val][c+val] == 1: blackCount +=1
        if redCount == 4:
            redWin = True
            if depth <=2: return -sys.maxint - 1
        elif blackCount ==4:
            blackWin = True
            if depth <= 2: return sys.maxint -1    
        score += getIncrement(redCount, blackCount, pieceType)
        r-=1
    return score

column = 0
        
def evaluateRed(depth, maxDepth, col, alpha, beta):
    global column
    minimum = sys.maxint
    score = 0
    if col != -1:
        score = getHeuristic(1, col, depth, maxDepth)
        if blackWin:
            return score
    if depth == maxDepth: return score
    
    for c in range(0,7):
        if firstRowAvailable[col] != -1:
            place(c, 2)
            value = evaluateBlack(depth+1, maxDepth,c,alpha,beta)
            dePlace(c)
            if value < minimum:
                minimum = value
                if depth == 0: column = c
            if value < beta: beta = value
            if alpha >= beta: return beta
            
    if minimum == sys.maxint: return 0
    return minimum

def evaluateBlack(depth, maxDepth, col, alpha, beta):
    global column
    maximum = -sys.maxint-1
    score = 0
    if col != -1:
        score = getHeuristic(2, col, depth, maxDepth)
        if redWin:
            return score
    if depth == maxDepth: return score
    
    for c in range(0,7):
        if firstRowAvailable[col] != -1:
            place(c, 1)
            value = evaluateRed(depth+1, maxDepth,c,alpha,beta)
            dePlace(c)
            if value > maximum:
                maximum = value
                if depth == 0: column = c
            if value > alpha: alpha = value
            if alpha >= beta: return alpha
            
    if maximum == -sys.maxint-1: return 0
    return maximum

def alphaBeta(maxDepth):
    global redWin
    global blackWin
    redWin = False
    blackWin = False
    evaluateBlack(0,1,-1,-sys.maxint, sys.maxint-1)
    if blackWin: return column
    redWin = False
    blackWin = False
    evaluateRed(0,1,-1,-sys.maxint, sys.maxint-1)
    if redWin: return column
    evaluateBlack(0,maxDepth,-1, -sys.maxint,sys.maxint-1)
    return column

def agentMove():
    col = alphaBeta(8)
    place(col, 1)
    
    
       
class Scene():
    def __init__(self):
    
        p.init()
        p.font.init()
        
        self.playerTurn = True
        
        self.background = p.image.load("res/board640.png")
        self.background = p.transform.scale(self.background, (width,height))
        self.backgroundRect = self.background.get_rect()
        
        self.screen = p.display.set_mode(size)
        self.newPiece = NewPiece()
        
        pieceSetup(self.screen)
        while run:
#             p.time.Clock().tick(60)
#             for event in p.event.get():
#                 if event.type == p.QUIT:
#                     p.display.quit()
#                     sys.exit()
            
            #while self.playerTurn:
            if not self.playerTurn:
                agentMove()
                Pieces.empty()
                pieceSetup(self.screen)
                self.playerTurn = True
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.display.quit()
                    sys.exit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_RIGHT:
                        self.newPiece.direction= "right"
                        self.newPiece.update()
                    elif event.key == p.K_LEFT:
                        self.newPiece.direction= "left"
                        self.newPiece.update()
                    elif event.key == p.K_SPACE:
                        place(self.newPiece.pos, 2)
                        Pieces.empty()
                        pieceSetup(self.screen)
                        getWinner()
                        self.playerTurn = False

                    elif event.key == p.K_ESCAPE:
                        dePlace(self.newPiece.pos)
                        Pieces.empty()
                        pieceSetup(self.screen)
                    elif event.key == p.K_TAB: self.example = True
            self.draw()
            self.screen.blit(self.newPiece.image, self.newPiece.rect)
            p.display.flip()
            self.update()
            
            #self.update()
            
    def draw(self):
        self.screen.fill([255,255,255])
        Pieces.draw(self.screen)
        self.screen.blit(self.background, self.backgroundRect)
        p.display.flip()
        
    def update(self):
        val = getWinner()
        if winnerFound:
            if val == 2:
                print("Red Wins!")
            elif val == 1:
                print("Black Wins!")
            sys.exit()
            
        
#if __name__ == '__main__':
s = Scene()
