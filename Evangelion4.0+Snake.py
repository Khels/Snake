import tkinter as tk
from random import randint


HEIGHT = 600
WIDTH = 600
SEG_SIZE = 20
IN_GAME = True


def main():
    global IN_GAME

    if IN_GAME:
        snake.move()

        head = cnvs_field.coords(snake.segments[-1].rect)
        x1, y1, x2, y2 = head

        if x1 < 0 or y1 < 0 or x2 > WIDTH or y2 > HEIGHT:
            IN_GAME = False

        elif head == cnvs_field.coords(CORE):
            snake.eat()
            cnvs_field.delete(CORE)
            spawn_core()

        else:
            for i in range(len(snake.segments)-1):
                if head == cnvs_field.coords(snake.segments[i].rect):
                    IN_GAME = False
        root.after(100, main)
    else:
        cnvs_field.create_text(WIDTH/2, HEIGHT/2,
                               text='HUMANITY IS DOOMED.',
                               font='Arial 20',
                               fill='DarkOrange1')


def spawn_core():
    global CORE
    posx = SEG_SIZE * randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    CORE = cnvs_field.create_oval(posx, posy,
                                  posx+SEG_SIZE,
                                  posy+SEG_SIZE,
                                  outline='red4',
                                  fill='red2')


class Segment:

    def __init__(self, x, y):
        self.rect = cnvs_field.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE,
                                                fill='green3')


class Snake:

    def __init__(self):
        self.segments = [Segment(20, 280), Segment(40, 280)]
        self.mapping = {
            'Up': (0, -1),
            'Down': (0, 1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }
        self.direction = self.mapping['Right']

    def move(self):
        for i in range(len(self.segments) - 1):
            segment = self.segments[i].rect
            x1, y1, x2, y2 = cnvs_field.coords(self.segments[i+1].rect)
            cnvs_field.coords(segment, x1, y1, x2, y2)

        head = cnvs_field.coords(self.segments[-1].rect)
        x = head[0]+self.direction[0]*SEG_SIZE
        y = head[1]+self.direction[1]*SEG_SIZE
        cnvs_field.coords(self.segments[-1].rect, x,
                          y, x+SEG_SIZE, y+SEG_SIZE)

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.direction = self.mapping[event.keysym]

    def eat(self):
        back = cnvs_field.coords(self.segments[0].rect)
        self.segments.insert(0, Segment(back[0], back[1]))


root = tk.Tk()
root.title('Evangelion: 4.0+Snake')

cnvs_field = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black')
cnvs_field.grid()
cnvs_field.focus_set()

snake = Snake()
spawn_core()
cnvs_field.bind('<KeyPress>', snake.change_direction)

main()

root.mainloop()
