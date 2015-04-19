import pygame as p
import sys


size = (width,height) = 640,480
run = 1

pieceArray = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0]]

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
 
def place(newPiece):
    lastline = pieceArray[0]
    for line in pieceArray:
        if line[newPiece.pos] != 0:
            break
        else:
            lastline = line
            
    lastline[newPiece.pos] = 2
        
     
        
class Scene():
    def __init__(self):
    
        p.init()
        p.font.init()
        
        self.playerTurn = 1
        
        self.background = p.image.load("res/board640.png")
        self.background = p.transform.scale(self.background, (width,height))
        self.backgroundRect = self.background.get_rect()
        
        self.screen = p.display.set_mode(size)
        
        pieceSetup(self.screen)
        while run:
            p.time.Clock().tick(60)
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.display.quit()
                    sys.exit()
            self.newPiece = NewPiece()
            while self.playerTurn:
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
                            place(self.newPiece)
                            pieceSetup(self.screen)
                        elif event.key == p.K_ESCAPE: self.pause = True
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
        return
        
#if __name__ == '__main__':
s = Scene()
