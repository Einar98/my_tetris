# Implementing a tetris game. 
import random
import pygame

pygame.init()

# ROTATION: Upper arrow key 
# MOVE LEFT: Left arrow key 
# MOVE RIGHT: Right arrow key

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure: 
    figures = [[[1, 5, 9, 13], [4, 5, 6, 7]], 
                [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
                [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
                [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], 
                [[1, 2, 5, 6]],
                [[0, 1, 5, 6], [1, 4, 5, 8], [4, 5, 9, 10], [2, 5, 6, 9]]]

    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y 
        self.color = random.randint(1, len(colors) - 1)
        self.type = random.randint(0, len(self.figures) - 1)    
        self.rotation = 0 

    def image(self) -> None:
        return self.figures[self.type][self.rotation] 

    def rotate(self) -> None:
        self.rotation = (1 + self.rotation) % (len(self.figures[self.type])) 

class Tetris:
    level = 2 
    score = 0
    state = "start"
    field = [] 
    height = 0 
    width = 0 
    x = 100 
    y = 60 
    zoom = 20 
    figure = None 
    def __init__(self, height, width) -> None:
        self.height = height 
        self.width = width 
        self.update_field()
    
    def update_field(self) -> None:
        for i in range(self.height):
            row = [] 
            for j in range(self.width):
                row.append(0)
            self.field.append(row)

    def new_figure(self) -> None:
        self.figure = Figure(3, 0) 
    
    def check_if_intersects(self) -> bool:
        intersection = False
        # Loop through each grid of the current image. 
        for i in range(4):
            for j in range(4):
                # Check if this value is in the current image (list of numbers) of the figure. 
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or j + self.figure.x > self.width - 1 or j + self.figure.x < 0 or self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True 
        return intersection 
    
    def freeze(self) -> None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines() 
        self.new_figure() 
        if self.check_if_intersects():
            self.state = "gameover"  
    
    def break_lines(self) -> None:
        # Check for horizontal lines with no zeros. 
        lines = 0 
        for i in range(1, self.height):
            zeros = self.field[i].count(0) # Counts the number of zeros in the row. 
            if zeros == 0:
                lines += 1 
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1-1][j] 
                
        self.score += lines**2
        # score is updated, but wont be shown 
        # print(self.score)

    def go_space(self) -> None:
        while not self.check_if_intersects():
            self.figure.y += 1 
        # If it intersects some boundary or other piece. 
        self.figure.y -= 1 
        self.freeze()  
    
    def go_down(self) -> None:
        self.figure.y += 1 
        if self.check_if_intersects():
            self.figure.y -= 1 
            self.freeze()
    
    def go_sideways(self, dx) -> None:
        previous_x = self.figure.x 
        self.figure.x += dx 
        if self.check_if_intersects():
            self.figure.x = previous_x 
    
    def rotate(self) -> None:
        previous_rotation = self.figure.rotation 
        self.figure.rotate() 
        if self.check_if_intersects():
            self.figure.rotation = previous_rotation 
            
class Game_view:
    WHITE = (255, 255, 255) 
    BLACK = (0, 0, 0) 
    GRAY = (125, 125, 125)
    def __init__(self, game:Tetris) -> None:
        self.game = game
        self.window_height = 500 
        self.window_width = 400 
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.FPS = 25 
        self.counter = 0 
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.font1 = pygame.font.SysFont('Calibri', 65, True, False) 
        self.text_game_over = self.font1.render("Game Over :( ", True, (255, 0, 0))
    
    def update_counter(self) -> None:
        self.counter += 1 
        if self.counter > 100000:
            self.counter = 0

    def draw_score_text(self) -> None:
        txt = self.font.render("Score: " + str(self.game.score), True, self.BLACK) 
        self.window.blit(txt, [0, 0])

    def draw_figure(self) -> None:
        if self.game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.game.figure.image():
                        pygame.draw.rect(self.window, colors[self.game.figure.color],
                                        [self.game.x + self.game.zoom * (j + self.game.figure.x) + 1,
                                        self.game.y + self.game.zoom * (i + self.game.figure.y) + 1,
                                        self.game.zoom - 2, self.game.zoom - 2]) 
    
    def draw_game_grid(self) -> None:
        for i in range(self.game.height):
            for j in range(self.game.width):
                pygame.draw.rect(self.window, self.GRAY, [self.game.x + self.game.zoom * j, self.game.y + self.game.zoom * i, 
                self.game.zoom, self.game.zoom], 1)
                if self.game.field[i][j] > 0:
                    pygame.draw.rect(self.window, colors[self.game.field[i][j]],
                                 [self.game.x + self.game.zoom * j + 1, self.game.y + self.game.zoom * i + 1, 
                                 self.game.zoom - 2, self.game.zoom - 1]) 
    
    def run_game(self) -> None:
        running = True 
        pressing_down = False 
        while running:
            # Initialize new figure. 
            if self.game.figure == None:
                self.game.new_figure()
            
            self.update_counter()
            if self.counter % (self.FPS // self.game.level // 2) == 0 or pressing_down:
                if self.game.state == "start":
                    self.game.go_down()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.rotate() 
                    if event.key == pygame.K_DOWN:
                        pressing_down = True 
                    if event.key == pygame.K_RIGHT:
                        self.game.go_sideways(1) 
                    if event.key == pygame.K_LEFT:
                        self.game.go_sideways(-1) 
                    if event.key == pygame.K_SPACE:
                        self.game.go_space() 
                if event.type ==  pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        pressing_down = False 
            # Fill the window
            self.window.fill(self.WHITE) 
            # Draw stuff here: 
            self.draw_game_grid() 
            self.draw_figure() 
            self.draw_score_text()
            # Check if game is over. 
            if self.game.state == "gameover":
                self.window.blit(self.text_game_over, [10, 200]) 
            
            pygame.display.update() 
            self.clock.tick(self.FPS) 

# CONSTANTS 
height = 20 
width = 10 

tetris = Tetris(height, width)
tetris_game = Game_view(tetris) 
tetris_game.run_game()
