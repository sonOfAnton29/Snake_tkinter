import sys
import os
import tkinter as tkr
import random   
import pyglet


GAME_WIDTH = 1500
GAME_HEIGHT = 600
SPEED = 0.2
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#33F0FF"
FOOD_COLOR = "#FF0000"
EXTRA_COLOR = "#4FD121"
BACKGROUND_COLOR = "#000000"
score = 0

def score_save(score):
    with open('scores.txt', 'a') as f:
        f.write(str(score) + '\n')


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.ovals = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            # square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            # self.squares.append(square)
            oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.ovals.append(oval)

class Food:
    def __init__(self):
        margin = 2
        self.x = random.randint(margin, (GAME_WIDTH/SPACE_SIZE)-1 - margin) * SPACE_SIZE
        self.y = random.randint(margin, (GAME_HEIGHT/SPACE_SIZE)-1 - margin) * SPACE_SIZE
        
        self.coordinates = [self.x, self.y]

    def normal(self):
        '''
        1 point
        '''
        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")
    def extra(self):
        '''
        2 points
        '''
        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill = EXTRA_COLOR, tag = "food")


def next_turn(snake, food):
    
    x, y = snake.coordinates[0]
    
    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    # square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    # snake.squares.insert(0, square)
    oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    snake.ovals.insert(0, oval)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        canvas.delete("food")
        food = Food()
        
        global score
        # added extra food that has 2 points
        if (score%5 == 4):
            score += 1
            food.extra()
        elif (score%5 == 0) and (score != 0):
            score += 2
            food.normal()
        else:
            score += 1
            food.normal()
        
        label.config(text = f"score: {score}")
        
        # increase speed every time scored
        global SPEED
        SPEED += 0.02

    else:
        del snake.coordinates[-1]
        # canvas.delete(snake.squares[-1])
        # del snake.squares[-1]
        canvas.delete(snake.ovals[-1])
        del snake.ovals[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(int(10*(1/SPEED)), next_turn, snake, food)

def check_collision(snake):

    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
        
    return False
    

def change_direction(new_direction):
    
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    if new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    if new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    if new_direction == 'down':
        if direction != 'up':
            direction = new_direction
        

def game_over():
    with open('scores.txt', 'w') as f:
        f.write('')
    score_save(score=score)

    canvas.delete(tkr.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consolas", 65), text="GAME OVER BITCH!", fill="red", tag = "gameover")

def restart_program(): # TODO: not a good approach, restart just the game
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


def background_music(song):# TODO: don't know how this library works
    '''
    loads and plays given song
    '''
    player = pyglet.media.Player()
    src = pyglet.media.load(song, streaming=False)
    player.queue(src)
    return player

player = background_music(song="bcg.mp3")


window = tkr.Tk()
window.title("Snake game")
window.resizable(False, False)

direction = "down"

label = tkr.Label(window, text=f"Score:{score}", font=("consolas", 40))

label.pack()

canvas = tkr.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)

canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
# to restart
window.bind('<Escape>', lambda event: restart_program())

snake = Snake()
food = Food()
food.normal()

player.play() # for music

next_turn(snake, food)

window.mainloop()
