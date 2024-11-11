import pygame
import threading
import sys
import time

class PgDisp:
    def __init__(self, name):
        self.name = name
        self.WIDTH, self.HEIGHT = 800, 600
        self.running = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(self.name)

        # Запускаем метод `loop` в отдельном потоке
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        # Цикл обновления экрана и рисования
        while self.running:
            # Заливка экрана чёрным цветом
            self.screen.fill((0, 0, 0))
            
            # Обновление экрана
            pygame.display.flip()
            
            # Ограничение на 60 FPS
            time.sleep(1 / 60)

        # Завершение Pygame, когда основной цикл окончен
        pygame.quit()

    def handle_events(self):
        # Обработка событий, выполняемая в главном потоке
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.w, event.h
                self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

# Создание экземпляра PgDisp
app = PgDisp("Растягиваемый чёрный экран")

# Основной поток ждёт завершения игрового окна
try:
    while app.running:
        app.handle_events()
        time.sleep(0.01)
except KeyboardInterrupt:
    app.running = False
    app.thread.join()
