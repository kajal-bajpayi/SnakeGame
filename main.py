import pygame
from pygame.locals import *
import time
import random
HOR_RES = 800
VER_RES = 400
SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.fruit = pygame.image.load("apple.jpg")
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.fruit, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, int(HOR_RES/SIZE-1))*SIZE
        self.y = random.randint(0, int(VER_RES/SIZE-1))*SIZE
        self.draw();


class Snake:

    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.x = [random.randint(1, int(HOR_RES/SIZE-1))*SIZE]*length
        self.y = [random.randint(1, int(VER_RES/SIZE-1))*SIZE]*length
        self.block = pygame.image.load("block.jpg")
        self.direction = 'UP'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = "UP"

    def move_down(self):
        self.direction = "DOWN"

    def move_right(self):
        self.direction = "RIGHT"

    def move_left(self):
        self.direction = "LEFT"

    def slither(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "UP":
            self.y[0] -= 40
        if self.direction == "DOWN":
            self.y[0] += 40
        if self.direction == "LEFT":
            self.x[0] -= 40
        if self.direction == "RIGHT":
            self.x[0] += 40
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load("logo.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("THE FAKE FRIEND")
        pygame.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((HOR_RES, VER_RES))
        self.render_background()
        pygame.display.flip()
        length = 1
        self.snake = Snake(self.surface, length)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True;

        return False

    def render_background(self):
        background = pygame.image.load("background.jpg")
        self.surface.blit(background, (0, 0))

    def play_background_music(self):
        pygame.mixer.music.load("bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.slither()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        # when collide with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
        # when collide with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0],self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"
        # when out of boundary
        if self.snake.x[0] >= HOR_RES or self.snake.x[0] < 0 or self.snake.y[0] >= VER_RES or self.snake.y[0] < 0:
            self.play_sound("crash")
            raise "Game over"


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Helvetica', 50)
        line1 = font.render(f" Game is over!\n Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (HOR_RES/6, VER_RES/6))
        line2 = font.render(f" Press ENTER to Retry", True, (255, 255, 255))
        self.surface.blit(line2, (HOR_RES / 6, VER_RES / 6 -50))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (HOR_RES-100, 0))

    def run(self):
        # define a variable to control the main loop
        running = True
        pause = False
        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_UP and self.snake.direction != "DOWN":
                            self.snake.move_up()
                            self.snake.direction = "UP"
                        if event.key == K_DOWN and self.snake.direction != "UP":
                            self.snake.move_down()
                            self.snake.direction = "DOWN"
                        if event.key == K_LEFT and self.snake.direction != "RIGHT":
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != "LEFT":
                            self.snake.move_right()
                            self.snake.direction = "RIGHT"
                # only do something if the event is of type QUIT
                if event.type == QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.1)


def main():
    game = Game()
    game.run()




# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    main()
