import tkinter as tk
from random import randint


HEIGHT = 570
WIDTH = 570
SEG_SIZE = 30
HEIGHT_MENU = HEIGHT
WIDTH_MENU = 450
IN_GAME = True
PAUSED = False
VICTORY = False
FREE_SPACES = []
DIFFICULTY = 100


def main():
    global IN_GAME

    if IN_GAME:
        if not PAUSED:
            snake.move()
            change_free_spaces()

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

            root.after(DIFFICULTY, main)

    else:
        if not VICTORY:
            set_state(txt_game_over, 'normal')
        if not PAUSED:
            set_state(txt_difficulty, 'normal')
            set_state(txt_pathetic, 'normal')
            set_state(txt_warrior, 'normal')
            set_state(txt_martyr, 'normal')
        set_state(txt_restart, 'normal')


def spawn_core():
    global CORE, FREE_SPACES, IN_GAME, VICTORY
    if FREE_SPACES:
        posx, posy = FREE_SPACES[randint(0, len(FREE_SPACES)-1)]
        CORE = cnvs_field.create_oval(posx, posy,
                                      posx + SEG_SIZE,
                                      posy + SEG_SIZE,
                                      outline='red4',
                                      fill='red2')
    else:
        IN_GAME = False
        VICTORY = True
        set_state(txt_victory, 'normal')


class Segment:

    def __init__(self, x, y):
        self.rect = cnvs_field.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE,
                                                fill='green3')


class Snake:

    def __init__(self):
        self.segments = [
            Segment(SEG_SIZE, SEG_SIZE),
            Segment(2*SEG_SIZE, SEG_SIZE),
            Segment(3*SEG_SIZE, SEG_SIZE)]

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
            if (self.direction == self.mapping['Up'] and
               self.mapping[event.keysym] != self.mapping['Down'] or
               self.direction == self.mapping['Down'] and
               self.mapping[event.keysym] != self.mapping['Up'] or
               self.direction == self.mapping['Left'] and
               self.mapping[event.keysym] != self.mapping['Right'] or
               self.direction == self.mapping['Right'] and
               self.mapping[event.keysym] != self.mapping['Left']):

                self.direction = self.mapping[event.keysym]

    def eat(self):
        back = cnvs_field.coords(self.segments[0].rect)
        self.segments.insert(0, Segment(back[0], back[1]))


def start_game():
    global FREE_SPACES, snake
    snake = Snake()
    change_free_spaces()
    cnvs_field.bind('<KeyPress>', snake.change_direction)
    spawn_core()
    main()


def clear_field():
    cnvs_field.delete(CORE)
    for segment in snake.segments:
        cnvs_field.delete(segment.rect)


def restart_game(event):
    global IN_GAME, VICTORY
    IN_GAME, VICTORY = True, False
    clear_field()
    set_state(txt_game_over, 'hidden')
    set_state(txt_restart, 'hidden')
    set_state(txt_victory, 'hidden')
    set_state(txt_difficulty, 'hidden')
    set_state(txt_pathetic, 'hidden')
    set_state(txt_warrior, 'hidden')
    set_state(txt_martyr, 'hidden')
    start_game()


def pause_game(event):
    global PAUSED
    if IN_GAME is True and PAUSED is False:
        PAUSED = True
        set_state(txt_pause, 'normal')
    else:
        PAUSED = False
        set_state(txt_pause, 'hidden')
        main()


def change_free_spaces():
    global FREE_SPACES, snake
    FREE_SPACES.clear()

    snake_segments = [tuple(cnvs_field.coords(segment.rect)[:2])
                      for segment in snake.segments]
    for x in range(WIDTH // SEG_SIZE):
        for y in range(HEIGHT // SEG_SIZE):
            if (x*SEG_SIZE, y*SEG_SIZE) not in snake_segments:
                FREE_SPACES.append((x*SEG_SIZE, y*SEG_SIZE))


def pathetic(event):
    global DIFFICULTY
    DIFFICULTY = 175


def warrior(event):
    global DIFFICULTY
    DIFFICULTY = 100


def martyr(event):
    global DIFFICULTY
    DIFFICULTY = 75


def set_state(item, state):
    menu.itemconfigure(item, state=state)


root = tk.Tk()
root.title('Evangelion: 4.0+Snake')

cnvs_field = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black')
cnvs_field.grid()
cnvs_field.focus_set()
menu = tk.Canvas(root, height=HEIGHT_MENU, width=WIDTH_MENU, bg='purple2')
menu.grid(row=0, column=1)
menu.focus_set()

txt_game_over = menu.create_text(
    WIDTH_MENU/2, HEIGHT_MENU*3/4,
    text='HUMANITY IS DOOMED.\n'
         'YOU CANNOT REDO.\n'
         'OR CAN YOU?..',
    justify=tk.CENTER,
    font='Arial 20',
    fill='DarkOrange2',
    state='hidden'
)

txt_pause = menu.create_text(
    WIDTH_MENU/2, HEIGHT_MENU*3/4,
    text='YOU CAN REST FOR NOW\n'
         'BUT YOU WILL NOT STOP\n'
         'THE INEVITABLE.',
    justify=tk.CENTER,
    font='Arial 20',
    fill='DarkOrange2',
    state='hidden'
)

txt_restart = menu.create_text(
    WIDTH_MENU/2, HEIGHT_MENU*3/4 + HEIGHT_MENU*1/6,
    text='REDO',
    justify=tk.CENTER,
    font='Arial 20',
    fill='white',
    state='hidden'
)

txt_victory = menu.create_text(
    WIDTH_MENU/2, HEIGHT_MENU*3/4,
    text='IMPOSSIBLE!\n'
         'I AM INVINCIBLE\n'
         'BUT STILL YOU DEFEATED ME?..',
    justify=tk.CENTER,
    font='Arial 20',
    fill='DarkOrange2',
    state='hidden'
)

txt_difficulty = menu.create_text(
    WIDTH_MENU/2, 20,
    text='CHOOSE THE DIFFICULTY:',
    font='Arial 20',
    fill='DarkOrange2',
    state='hidden'
)

txt_pathetic = menu.create_text(
    WIDTH_MENU/2, 60,
    text='pathetic',
    font='Arial 20',
    fill='white',
    state='hidden'
)

txt_warrior = menu.create_text(
    WIDTH_MENU/2, 90,
    text='warrior',
    font='Arial 20',
    fill='white',
    state='hidden'
)

txt_martyr = menu.create_text(
    WIDTH_MENU/2, 120,
    text='martyr',
    font='Arial 20',
    fill='white',
    state='hidden'
)

menu.tag_bind(txt_pathetic, "<Button-1>", pathetic)
menu.tag_bind(txt_warrior, "<Button-1>", warrior)
menu.tag_bind(txt_martyr, "<Button-1>", martyr)
menu.tag_bind(txt_restart, "<Button-1>", restart_game)
cnvs_field.bind("<Escape>", pause_game)

start_game()

root.mainloop()
