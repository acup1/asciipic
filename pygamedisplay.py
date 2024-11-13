import pygame
import threading
import sys
import time
from random import randint

class PgDisp:
    def __init__(self, name: str, font_size: int):
        self.name = name
        self.WIDTH, self.HEIGHT = 800, 600
        self.running = True
        self.is_active = False
        self.is_minimized = False
        self.minimized_time = 0
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('logo.png'))
        pygame.display.set_caption(self.name)
        #self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        self.font = pygame.font.Font("consola.ttf", font_size)
        #print(pygame.font.get_default_font())
        self.sym_size = self.font.size("#")
        #self.thread = threading.Thread(target=self.loop, daemon=True)
        #self.thread.start()

    
    def size(self) -> tuple[int,int]:
        "size of text grid in format (height,width)"
        return (self.HEIGHT//self.sym_size[1],self.WIDTH//self.sym_size[0])

    def set_text(self,text:str,x:float,y:float, color:tuple[int]=(255,255,255), bg_color:tuple[int]=(0,0,0)):
        "just setting the text"
        temp=self.font.render(text,True, color,bg_color)
        self.screen.blit(temp, dest=(x,y))

    def set_aligned_text(self,text:str,x:int,y:int, color:tuple[int]=(255,255,255), bg_color:tuple[int]=(0,0,0)):
        "set text on a grid"
        self.set_text(text,
                      x*self.sym_size[0]+(self.WIDTH%self.sym_size[0])//2,
                      y*self.sym_size[1]+(self.HEIGHT%self.sym_size[1])//2,
                      color,
                      bg_color)        

    def clear(self,color:tuple[int]=(0,0,0)):
        "clear the screen"
        self.screen.fill(color)


    def handle_events(self):
        "EVENTS!!!"
        #self.clear()
        #for y in range(0,self.size()[0]):
        #    for x in range(0,self.size()[1]):
        #        self.set_aligned_text(f"#",x,y,bg_color=(255,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.w, event.h
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 0:  # Если gain = 0, окно потеряло активность
                    self.is_active = False
                else:
                    self.is_active = True
            elif event.type == pygame.WINDOWMINIMIZED:
                self.is_minimized=True
                print(1)
                self.minimized_time=time.time()
            elif event.type == pygame.WINDOWMAXIMIZED:
                self.is_minimized=False
            elif event.type == pygame.WINDOWRESTORED:
                self.is_minimized=False
            else:
                pass#print(event.type)
            
            #elif event.type == pygame.WINDOWMINIMIZED:
                
        pygame.display.flip()
        self.clock.tick(60)

if __name__=="__main__":
    app = PgDisp("test")

    try:
        while app.running:
            app.handle_events()
            time.sleep(.001)
    except KeyboardInterrupt:
        app.running = False
        app.thread.join()
