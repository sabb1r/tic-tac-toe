from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import random

class Player():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.moves = set()
    
    def add_move(self, move):
        self.moves.add(move)
    
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
        hard_btn = ttk.Radiobutton(content, text='Hard', variable=mode, value='hard')
        easy_btn.grid(row=2, column=1, sticky=E)
        hard_btn.grid(row=2, column=2, sticky=E)
    
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
    
def computer_play():
    if mode == 'easy':
        btn_pos_x, btn_pos_y = random.choice(list(remaining_moves))
        btn = button_set[btn_pos_x][btn_pos_y]
        btn.invoke()
    elif mode == 'medium':
        computer_win_position = winning_position(current_player)
        if computer_win_position:
            btn = button_set[computer_win_position[0]][computer_win_position[1]]
            btn.invoke()
        opponent_win_position = winning_position(next_player)
        
    else:
        pass

def winning_position(player):
    # Winning position check for the given player
    answer = tuple()
    for i in range(2):
        # same_row_pos = {x for x in player.moves if x[0] == i}
        # same_col_pos = {x for x in player.moves if x[1] == i}
        moves = player.moves
        probable_row_pos = ROWS[i].difference(moves)
        probable_col_pos = COLUMNS[i].difference(moves)
        if i < 2:
            probable_diag_pos = DIAGS[i].difference(moves)
        if len(probable_row_pos) == 1:
            if button_set[probable_row_pos[0]][probable_col_pos[1]].instate(['!disabled']):
                answer = probable_row_pos
                break
        elif len(probable_col_pos) == 1:
            if button_set[probable_col_pos[0]][probable_col_pos[1]].instate(['!disabled']):
                answer = probable_col_pos
                break
        elif i < 2:
            if button_set[probable_diag_pos[0]][probable_diag_pos[1]].instate(['!disabled']):
                answer = probable_diag_pos
                break
    return answer

def toggle_player():
    global current_player
    global next_player
    if current_player.position == 'First Player':
        next_player = player1
        current_player = player2
    else:
        next_player = player2
        current_player = player1

def move_selected(btn_pos_x, btn_pos_y):
    global current_player
    global next_player
    global remaining_moves

    if current_player.position == 'First Player':
        btn_img = cross_image
        # next_player = player2
    else:
        btn_img = round_image
        # next_player = player1

    btn = button_set[btn_pos_x][btn_pos_y]
    btn['image'] = btn_img
    btn.state(['disabled'])
    current_player.add_move((btn_pos_x, btn_pos_y))
    remaining_moves.remove((btn_pos_x, btn_pos_y))

    if is_winner(current_player):
        result_status['text'] = current_player.name
        for (btn_pos_x, btn_pos_y) in remaining_moves:
            button_set[btn_pos_x][btn_pos_y].state(['disabled'])
        return 
    
    if not remaining_moves:
        result_status['text'] = 'The Match is Drawn'
        return
    
    # current_player = next_player

    toggle_player()
    
    if current_player.name == 'Computer':
        root.after(500, computer_play)

def is_winner(player):
    moves = player.moves
    if len(moves) < 3:
        return False
    for i in range(3):
        if not ROWS[i].difference(moves):
            return True
        if not COLUMNS[i].difference(moves):
            return True
        if i == 2:
            continue
        else:
            if not DIAGS[i].difference(moves):
                return True
    return False
    
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

player1 = Player(first_player, 'First Player')
player2 = Player(second_player, 'Second Player')
remaining_moves = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
ROWS = [{(0, 0), (0, 1), (0, 2)}, {(1, 0), (1, 1), (1, 2)}, {(2, 0), (2, 1), (2, 2)}]
COLUMNS = [{(0, 0), (1, 0), (2, 0)}, {(0, 1), (1, 1), (2, 1)}, {(0, 2), (1, 2), (2, 2)}]
DIAGS = [{(0, 0), (1, 1), (2, 2)}, {(0, 2), (1, 1), (2, 0)}]

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
