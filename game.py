from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import random

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

    def player_select(player_info):
        opponent.set(player_info)
        if player_info == 'human':
            usr_btn.state(['disabled'])
            computer_btn.state(['!disabled'])
        else:
            usr_btn.state(['!disabled'])
            computer_btn.state(['disabled'])
    
    def close_initial_window():
        for child in content.winfo_children():
            child.destroy()
        start_game(root)
    
    content = root.winfo_children()[0]

    opponent_lbl = ttk.Label(content, text='Choose your opponent')
    opponent_lbl.grid(row=0, column=0, columnspan=3, sticky=NS)

    btn_frame = ttk.Frame(content)
    btn_frame.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    usr_btn = ttk.Button(btn_frame, image=usr_image, command=lambda: player_select('human'))
    computer_btn = ttk.Button(btn_frame, image=computer_image, command=lambda: player_select('computer'))
    usr_btn.grid(row=0, column=0, sticky=NSEW)
    computer_btn.grid(row=0, column=1, sticky=NSEW)

    mode_lbl = ttk.Label(content, text='Select Mode:')
    mode_lbl.grid(row=2, column=0, sticky=W)

    easy_btn = ttk.Radiobutton(content, text='Easy', variable=mode, value='easy')
    hard_btn = ttk.Radiobutton(content, text='Hard', variable=mode, value='hard')
    easy_btn.grid(row=2, column=1, sticky=E)
    hard_btn.grid(row=2, column=2, sticky=E)

    first_player_lbl = ttk.Label(content, text='Will you play first?')
    first_player_lbl.grid(row=3, column=0, sticky=W)

    yes_btn = ttk.Radiobutton(content, text='Yes', variable=first_player, value='Yes')
    no_btn = ttk.Radiobutton(content, text='No', variable=first_player, value='No')
    yes_btn.grid(row=3, column=1, sticky=E)
    no_btn.grid(row=3, column=2, sticky=E)

    confirm_btn = ttk.Button(content, text='Confirm', command= close_initial_window)
    confirm_btn.grid(row=4, column=2, sticky=E)

    btn_frame.columnconfigure(0, weight=2)
    btn_frame.columnconfigure(1, weight=2)
    btn_frame.rowconfigure(0, weight=2)
    
def start_game(root):
    def is_winner(position_set):
        if len(position_set) >= 3:
            for i in range(3):
                row = [x for x in position_set if x[0] == i]
                col = [x for x in position_set if x[1] == i]
                if len(row) == 3:
                    return (True, 'r', i)
                elif len(col) == 3:
                    return (True, 'c', i)
            if (1, 1) in position_set:
                if (0, 0) in position_set and (2, 2) in position_set:
                    return (True, 'd', 1)
                elif (0, 2) in position_set and (2, 0) in position_set:
                    return (True, 'd', 2)
            return (False, '', 0)
        else:
            return (False, '', 0)

    def move_selected(pos_x, pos_y):
        nonlocal counter
        nonlocal result_status
        nonlocal computer_played

        btn = button_set[pos_x][pos_y]
        if counter % 2:
            img = round_image
            player = 'Player 2'
            moves = player2_moves
        else:
            img = cross_image
            player = 'Player 1'
            moves = player1_moves
        
        btn['image'] = img
        btn.state(['disabled'])
        moves.add((pos_x, pos_y))
        winner, pattern, number = is_winner(moves)

        if winner:
            winner_celebration(player)
            
        remaining_moves.remove((pos_x, pos_y))

        counter += 1
        if counter == 9:
            result_status['text'] = 'Match is drawn'

        if player1 == 'computer' or player2 == 'computer':
            if not computer_played:
                computer_moves()
            else:
                computer_played = False

    def computer_moves():
        nonlocal computer_played
        computer_played = True
        if mode.get() == 'easy':
            selection = random.choice(remaining_moves)
            btn = button_set[selection[0]][selection[1]]
            btn.invoke()
        else:
            pass

    def winner_celebration(player):
        result_status['text'] = '{} is winner!!'.format(player)
        for x, y in remaining_moves:
                    button_set[x][y].state(['disabled'])

    content = root.winfo_children()[0]
    btn_frame = ttk.Frame(content, height=300, width=300)
    btn_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=NSEW)

    button_set = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
            ]
    
    for i in range(3):
        for j in range(3):
            btn = ttk.Button(btn_frame, image=background_image, command= lambda i=i, j=j: move_selected(i, j))
            button_set[i][j] = btn
            btn.grid(row=i, column=j, sticky=NSEW)

    info_frame = ttk.Frame(content, height=300, width=300)
    info_frame.grid(row=0, column=3, rowspan=3, sticky=NSEW)

    first_player_status = ttk.Label(info_frame, text='First Player')
    second_player_status = ttk.Button(info_frame, text='Second Player')
    result_status = ttk.Label(info_frame, text='WHO WINS?')

    first_player_status.grid(row=0, column=0)
    second_player_status.grid(row=1, column=0)
    result_status.grid(row=2, column=0)

    if first_player.get() == 'Yes':
        player1 = 'you'
        player2 = opponent.get()
    else:
        player1 = opponent.get()
        player2 = 'you'
    
    player1_moves = set()
    player2_moves = set()
    remaining_moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)] 
    counter = 0
    computer_played = False

    if player1 == 'computer':
        computer_moves()

# -- Main Program Starts Here -- #
root = create_window()

img_size = (80, 80)
usr_image = ImageTk.PhotoImage(Image.open('./resource/user.png').resize(img_size))
computer_image = ImageTk.PhotoImage(Image.open('./resource/computer.png').resize(img_size))
cross_image = ImageTk.PhotoImage(Image.open('./resource/cross.png').resize((80, 80)))
round_image = ImageTk.PhotoImage(Image.open('./resource/circle.png').resize(img_size))
background_image = ImageTk.PhotoImage(Image.open('./resource/background.png').resize(img_size))
opponent = StringVar()
mode = StringVar()
first_player = StringVar()

initiate(root)

root.mainloop()
