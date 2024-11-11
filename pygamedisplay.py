import pygame
import threading
import sys
import time
from random import randint

class PgDisp:
    def __init__(self, name):
        self.name = name
        self.WIDTH, self.HEIGHT = 800, 600
        self.running = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(self.name)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.sym_size = self.font.size("#")
        #self.thread = threading.Thread(target=self.loop, daemon=True)
        #self.thread.start()

    def loop(self):
        while self.running:
            try:
                self.screen.fill((randint(0,255), 0, 0))
                self.setstr('center',0,0)
                
                pygame.display.flip()            
                time.sleep(1 / 60)
            except:pass
        pygame.quit()
    
    def setstr(self,text:str,x:int|float,y:int|float):
        temp=self.font.render(text,True, (255,255,255))
        self.screen.blit(temp, dest=(x,y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.w, event.h
                self.screen.fill((0,0,0))
                for y in range(0,self.HEIGHT,self.sym_size[1]):
                    for x in range(0,self.WIDTH,self.sym_size[0]):
                        app.setstr(f"#",x,y)
                #self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.flip()

app = PgDisp("test")

try:
    while app.running:
        app.handle_events()
        time.sleep(.001)
except KeyboardInterrupt:
    app.running = False
    app.thread.join()
