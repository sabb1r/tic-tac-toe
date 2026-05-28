from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import random

class Point():
    ROWS = {0: ((0, 0), (0, 1), (0, 2)), 1: ((1, 0), (1, 1), (1, 2)), 2: ((2, 0), (2, 1), (2, 2))}
    COLUMNS = {0: ((0, 0), (1, 0), (2, 0)), 1: ((0, 1), (1, 1), (2, 1)), 2: ((0, 2), (1, 2), (2, 2))}
    DIAGS = {0: ((0, 0), (1, 1), (2, 2)), 1: ((0, 2), (1, 1), (2, 0))}
    CORNERS = {(0, 0), (0, 2), (2, 0), (2, 2)}
    REMAINING_MOVES = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
    VECTORS = {
            (0, 0): {ROWS[0], COLUMNS[0], DIAGS[0]}, 
            (0, 1): {ROWS[0], COLUMNS[1]},
            (0, 2): {ROWS[0], COLUMNS[2], DIAGS[1]},
            (1, 0): {ROWS[1], COLUMNS[0]},
            (1, 1): {ROWS[1], COLUMNS[1], DIAGS[0], DIAGS[1]},
            (1, 2): {ROWS[1], COLUMNS[2]},
            (2, 0): {ROWS[2], COLUMNS[0], DIAGS[1]},
            (2, 1): {ROWS[2], COLUMNS[1]},
            (2, 2): {ROWS[2], COLUMNS[2], DIAGS[0]}
            }

class Player(Point):
    def __init__(self, name, position, image):
        self.name = name
        self.position = position
        self.image = image
        self.own_moves = []
        self.own_vector = set()
        self.opponent_moves = []
        self.opponent_vector = set()
        self.win_vector = set()
        self.winning_move = tuple()
    
    def add_move(self, move):
        self.own_moves.append(move)
        self.own_vector = self.own_vector.union(self.VECTORS[move])
        self.win_vector = self.own_vector.difference(self.opponent_vector)
        self.winning_move_calculation()
    
    def add_opponent_move(self, move):
        self.opponent_moves.append(move)
        self.opponent_vector = self.opponent_vector.union(self.VECTORS[move])
        self.win_vector = self.own_vector.difference(self.opponent_vector)
        self.winning_move_calculation()

    def winning_move_calculation(self):
        if len(self.own_moves) >= 2:
            for i in range(3):
                moves = self.own_moves
                probable_row_pos = list(set(self.ROWS[i]).difference(moves))
                probable_col_pos = list(set(self.COLUMNS[i]).difference(moves))
                if i < 2:
                    probable_diag_pos = list(set(self.DIAGS[i]).difference(moves))
                if len(probable_row_pos) == 1:
                    x, y = probable_row_pos[0]
                    if button_set[x][y].instate(['!disabled']):
                        self.winning_move = (x, y)
                        break
                elif len(probable_col_pos) == 1:
                    x, y = probable_col_pos[0]
                    if button_set[x][y].instate(['!disabled']):
                        self.winning_move = (x, y)
                        break
                elif i < 2 and len(probable_diag_pos) == 1:
                    x, y = probable_diag_pos[0]
                    if button_set[x][y].instate(['!disabled']):
                        self.winning_move = (x, y)
                        break
    
    def is_winner(self):
        if len(self.own_moves) < 3:
            return False
        for i in range(3):
            if not set(self.ROWS[i]).difference(self.own_moves):
                return True
            if not set(self.COLUMNS[i]).difference(self.own_moves):
                return True
            if i == 2:
                continue
            else:
                if not set(self.DIAGS[i]).difference(self.own_moves):
                    return True
        return False
    
    def __repr__(self):
        return 'Player Name: {}, Plays: {}'.format(self.name, self.position)
    
def create_window():
    root = Tk()
    root.title('Tic Tac Toe')
    content = ttk.Frame(root, width=600, height=400)
    content.grid(row=0, column=0, sticky=NSEW)

    content.columnconfigure(0, weight=2)
    content.columnconfigure(1, weight=2)
    content.columnconfigure(2, weight=2)
    content.rowconfigure(0, weight=2)
    content.rowconfigure(1, weight=2)
    content.rowconfigure(2, weight=2)
    content.rowconfigure(3, weight=2)

    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=2)

    return root

def initiate(root):

    def opponent_selection(player_info):
        opponent.set(player_info)
        if player_info == 'Player2':
            usr_btn.state(['disabled'])
            computer_btn.state(['!disabled'])
        else:
            usr_btn.state(['!disabled'])
            computer_btn.state(['disabled'])
            mode_selection()
    
    def mode_selection():
        # nonlocal mode
        mode_lbl = ttk.Label(content, text='Select Mode:')
        mode_lbl.grid(row=2, column=0, sticky=W)

        easy_btn = ttk.Radiobutton(content, text='Easy', variable=mode, value='easy')
        medium_btn = ttk.Radiobutton(content, text='Medium', variable=mode, value='medium')
        hard_btn = ttk.Radiobutton(content, text='Hard', variable=mode, value='hard')
        easy_btn.grid(row=2, column=1, sticky=E)
        medium_btn.grid(row=2, column=2, sticky=E)
        hard_btn.grid(row=2, column=3, sticky=E)
    
    def return_root():
        opponent_val = opponent.get()
        if opponent_val:
            if opponent_val == 'Computer':
                if mode.get():
                    if first_player.get():
                        root.destroy()
                    else:
                        ttk.Label(content, text='First Player is not selected').grid(row=4, column=0, columnspan=3, sticky=EW)
                else:
                    ttk.Label(content, text='Game Mode and/or First Player is not selected').grid(row=4, column=0, columnspan=3, sticky=EW)
            else:
                if first_player.get():
                    root.destroy()
                else:
                    ttk.Label(content, text='First Player is not selected').grid(row=4, column=0, columnspan=3, sticky=EW)
        else:
            ttk.Label(content, text='Opponent player is not selected').grid(row=4, column=0, columnspan=3, sticky=EW)

     
    opponent = StringVar()
    mode = StringVar()
    first_player = StringVar()

    content = root.winfo_children()[0]

    opponent_lbl = ttk.Label(content, text='Choose your opponent')
    opponent_lbl.grid(row=0, column=0, columnspan=3, sticky=NS)

    btn_frame = ttk.Frame(content)
    btn_frame.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    usr_btn = ttk.Button(btn_frame, image=usr_image, command=lambda: opponent_selection('Player2'))
    computer_btn = ttk.Button(btn_frame, image=computer_image, command=lambda: opponent_selection('Computer'))
    usr_btn.grid(row=0, column=0, sticky=NSEW)
    computer_btn.grid(row=0, column=1, sticky=NSEW)

    first_player_lbl = ttk.Label(content, text='Who will play first move?')
    first_player_lbl.grid(row=3, column=0, sticky=W)

    yes_btn = ttk.Radiobutton(content, text='You', variable=first_player, value='You')
    no_btn = ttk.Radiobutton(content, text='Opponent', variable=first_player, value='Opponent')
    yes_btn.grid(row=3, column=1, sticky=E)
    no_btn.grid(row=3, column=2, sticky=E)


    confirm_btn = ttk.Button(content, text='Confirm', command= return_root)
    confirm_btn.grid(row=5, column=2, sticky=E)

    btn_frame.columnconfigure(0, weight=2)
    btn_frame.columnconfigure(1, weight=2)
    btn_frame.rowconfigure(0, weight=2)

    root.mainloop()

    if first_player.get() == 'Opponent':
        first_player.set(opponent.get())

    return opponent.get(), mode.get(), first_player.get()

def distance(point1, point2):
    return pow((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2, 0.5)

def computer_play():
    if mode == 'easy':
        push_random_btn()
    else:
        if current_player.winning_move:
            x, y = current_player.winning_move
            button_set[x][y].invoke()
        elif next_player.winning_move:
            x, y = next_player.winning_move
            button_set[x][y].invoke()
        else:
            if mode == 'medium':
                push_random_btn()
            else:
                if not current_player.own_moves and not current_player.opponent_moves:
                    push_random_btn(Point.CORNERS)
                elif not current_player.own_moves and current_player.opponent_moves:
                    if button_set[1][1].instate(['!disabled']):
                        button_set[1][1].invoke()
                    else:
                        push_random_btn(Point.CORNERS)
                else:
                    last_entry = current_player.own_moves[-1]

                    nearest_corner = []

                    remaining_corners = Point.CORNERS.difference(set(current_player.own_moves).union(set(next_player.own_moves)))
                    if len(remaining_corners) == 1:
                        optimum_point = remaining_corners.pop()
                    else:
                        for point in remaining_corners:
                            # for vector in current_player.win_vector:
                            #     if point in vector:
                            #         break
                            # else:
                            #     continue
                            d = distance(last_entry, point)
                            if round(d, 1) == 2.0:
                                nearest_corner.append(point)
                        if len(nearest_corner) > 1:
                            last_opponent_entry = current_player.opponent_moves[-1]
                            max_distance = -1
                            optimum_point = None 
                            for point in nearest_corner:
                                d = distance(last_opponent_entry, point)
                                if d > max_distance:
                                    max_distance = d
                                    optimum_point = point 
                        elif len(nearest_corner) == 1:
                            optimum_point = nearest_corner[0]
                        else:
                            optimum_point = random.choice(list(Point.REMAINING_MOVES))
                    
                    button_set[optimum_point[0]][optimum_point[1]].invoke()
                    
def push_random_btn(moves=''):
    if not moves:
        moves = Point.REMAINING_MOVES
    x, y = random.choice(list(moves))
    btn = button_set[x][y]
    btn.invoke()

def toggle_player():
    global current_player
    global next_player

    current_player, next_player = next_player, current_player

def move_selected(btn_pos_x, btn_pos_y):
    global current_player
    global next_player
    # global remaining_moves

    btn = button_set[btn_pos_x][btn_pos_y]
    btn['image'] = current_player.image
    btn.state(['disabled'])
    current_player.add_move((btn_pos_x, btn_pos_y))
    next_player.add_opponent_move((btn_pos_x, btn_pos_y))
    Point.REMAINING_MOVES.remove((btn_pos_x, btn_pos_y))

    if current_player.is_winner():
        result_status['text'] = current_player.name
        for (btn_pos_x, btn_pos_y) in Point.REMAINING_MOVES:
            button_set[btn_pos_x][btn_pos_y].state(['disabled'])
        return 
    
    if not Point.REMAINING_MOVES:
        result_status['text'] = 'The Match is Drawn'
        return

    toggle_player()
    
    if current_player.name == 'Computer':
        root.after(500, computer_play)

    
# -- Main Program Starts Here -- #
root = create_window()

img_size = (80, 80)
usr_image = ImageTk.PhotoImage(Image.open('./resource/user.png').resize(img_size))
computer_image = ImageTk.PhotoImage(Image.open('./resource/computer.png').resize(img_size))

opponent, mode, first_player = initiate(root)

if first_player != 'You':
    second_player = 'You'
else:
    second_player = opponent

root = create_window()
content = root.winfo_children()[0]

btn_frame = ttk.Frame(content, height=300, width=300)
btn_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=NSEW)

button_set = [[None, None, None],
            [None, None, None],
            [None, None, None]]

cross_image = ImageTk.PhotoImage(Image.open('./resource/cross.png').resize(img_size))
round_image = ImageTk.PhotoImage(Image.open('./resource/circle.png').resize(img_size))
background_image = ImageTk.PhotoImage(Image.open('./resource/background.png').resize(img_size))

player1 = Player(first_player, 'First Player', cross_image)
player2 = Player(second_player, 'Second Player', round_image)
    
for i in range(3):
    for j in range(3):
        btn = ttk.Button(btn_frame, image=background_image, command= lambda i=i, j=j: move_selected(i, j))
        button_set[i][j] = btn
        btn.grid(row=i, column=j, sticky=NSEW)

info_frame = ttk.Frame(content, height=300, width=300)
info_frame.grid(row=0, column=3, rowspan=3, sticky=NSEW)

first_player_status = ttk.Label(info_frame, text='First Player')
second_player_status = ttk.Label(info_frame, text='Second Player')
result_status = ttk.Label(info_frame, text='WHO WINS?')

first_player_status.grid(row=0, column=0)
second_player_status.grid(row=1, column=0)
result_status.grid(row=2, column=0)


current_player = player1
next_player = player2
if current_player.name == 'Computer':
    computer_play()

root.mainloop()
