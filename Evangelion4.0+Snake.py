import tkinter as tk
from random import randint

'''
HEIGHT = 570
WIDTH = 570
SEG_SIZE = 30
'''
HEIGHT = 600
WIDTH = 600
SEG_SIZE = 100
IN_GAME = True
PAUSED = False
VICTORY = False
FREE_SPACES = []
# DIFFICULTY for root.after()
# ADD A COMMENT TO EVERY CLASS, CLASS METHOD AND FUNCTION
# ADD AN ABILITY TO KEEP RECORDS OF ALL GAMES VIA FILE SAVES


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

            root.after(250, main)

    else:
        if not VICTORY:
            set_state(txt_game_over, 'normal')
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
        print('VICTORY!!!')
        set_state(txt_victory, 'normal')


class Segment:

    def __init__(self, x, y):
        self.rect = cnvs_field.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE,
                                                fill='green3')


class Snake:

# Segment(SEG_SIZE, SEG_SIZE),
# Segment(2*SEG_SIZE, SEG_SIZE),
# Segment(3*SEG_SIZE, SEG_SIZE),

    def __init__(self):
        self.segments = [
            Segment(0, SEG_SIZE),
            Segment(SEG_SIZE, SEG_SIZE),
            Segment(2*SEG_SIZE, SEG_SIZE),
            Segment(3*SEG_SIZE, SEG_SIZE),
            Segment(4*SEG_SIZE, SEG_SIZE),
            Segment(4*SEG_SIZE, 2*SEG_SIZE),
            Segment(3*SEG_SIZE, 2*SEG_SIZE),
            Segment(2*SEG_SIZE, 2*SEG_SIZE),
            Segment(SEG_SIZE, 2*SEG_SIZE),
            Segment(0, 2*SEG_SIZE),
            Segment(0, 3*SEG_SIZE),
            Segment(SEG_SIZE, 3*SEG_SIZE),
            Segment(2*SEG_SIZE, 3*SEG_SIZE),
            Segment(3*SEG_SIZE, 3*SEG_SIZE),
            Segment(4*SEG_SIZE, 3*SEG_SIZE),
            Segment(4*SEG_SIZE, 4*SEG_SIZE),
            Segment(3*SEG_SIZE, 4*SEG_SIZE),
            Segment(2*SEG_SIZE, 4*SEG_SIZE),
            Segment(SEG_SIZE, 4*SEG_SIZE),
            Segment(0, 4*SEG_SIZE),
            Segment(0, 5*SEG_SIZE),
            Segment(SEG_SIZE, 5*SEG_SIZE),
            Segment(2*SEG_SIZE, 5*SEG_SIZE)]

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
    global IN_GAME
    IN_GAME = True
    clear_field()
    set_state(txt_game_over, 'hidden')
    set_state(txt_restart, 'hidden')
    set_state(txt_victory, 'hidden')
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

    snake_segments = [tuple(cnvs_field.coords(segment.rect)[:2]) for segment in snake.segments]
    for x in range(WIDTH // SEG_SIZE):
        for y in range(HEIGHT // SEG_SIZE):
            if (x*SEG_SIZE, y*SEG_SIZE) not in snake_segments:
                FREE_SPACES.append((x*SEG_SIZE, y*SEG_SIZE))


def set_state(item, state):
    cnvs_field.itemconfigure(item, state=state)


root = tk.Tk()
root.title('Evangelion: 4.0+Snake')

cnvs_field = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black')
cnvs_field.grid()
cnvs_field.focus_set()

txt_game_over = cnvs_field.create_text(
    WIDTH/2, HEIGHT/2 - SEG_SIZE,
    text='HUMANITY IS DOOMED.\n'
         'YOU CANNOT REDO.\n'
         'OR CAN YOU?..',
    justify=tk.CENTER,
    font='Arial 20',
    fill='DarkOrange1',
    state='hidden'
)

txt_pause = cnvs_field.create_text(
    WIDTH/2, HEIGHT/2 - SEG_SIZE,
    text='YOU CAN REST FOR NOW\n'
         'BUT YOU WILL NOT STOP\n'
         'THE INEVITABLE.',
    justify=tk.CENTER,
    font='Arial 20',
    fill='DarkOrange1',
    state='hidden'
)

txt_restart = cnvs_field.create_text(
    WIDTH/2, HEIGHT/2 + 2*SEG_SIZE,
    text='REDO',
    justify=tk.CENTER,
    font='Arial 20',
    fill='white',
    state='hidden'
)

txt_victory = cnvs_field.create_text(
    WIDTH/2, HEIGHT/2 - SEG_SIZE,
    text='IMPOSSIBLE!\n'
         'I AM INVINCIBLE\n'
         'BUT STILL YOU DEFEATED ME?..',
    justify=tk.CENTER,
    font='Arial 20',
    fill='DarkOrange1',
    state='hidden'
)

cnvs_field.tag_bind(txt_restart, "<Button-1>", restart_game)
cnvs_field.bind("<Escape>", pause_game)

start_game()

root.mainloop()
