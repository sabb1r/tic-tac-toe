from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def initiate():

    def player_select(player_info):
        opponent.set(player_info)
        if player_info == 'human':
            usr_btn.state(['disabled'])
            computer_btn.state(['!disabled'])
        else:
            usr_btn.state(['!disabled'])
            computer_btn.state(['disabled'])

    root = Tk()
    root.title('Tic Tac Toe')
    content = ttk.Frame(root, width=500, height=400)
    content.grid(row=0, column=0, sticky=NSEW)

    opponent_lbl = ttk.Label(content, text='Choose your opponent')
    opponent_lbl.grid(row=0, column=0, columnspan=3, sticky=NS)

    btn_frame = ttk.Frame(content)
    btn_frame.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    img_size = (80, 80)
    usr_image = ImageTk.PhotoImage(Image.open('./resource/user.png').resize(img_size))
    computer_image = ImageTk.PhotoImage(Image.open('./resource/computer.png').resize(img_size))
    global opponent
    opponent = StringVar()
    usr_btn = ttk.Button(btn_frame, image=usr_image, command=lambda: player_select('human'))
    computer_btn = ttk.Button(btn_frame, image=computer_image, command=lambda: player_select('computer'))
    usr_btn.grid(row=0, column=0, sticky=NSEW)
    computer_btn.grid(row=0, column=1, sticky=NSEW)

    mode_lbl = ttk.Label(content, text='Select Mode:')
    mode_lbl.grid(row=2, column=0, sticky=W)
    global mode
    mode = StringVar()
    easy_btn = ttk.Radiobutton(content, text='Easy', variable=mode, value='easy')
    hard_btn = ttk.Radiobutton(content, text='Hard', variable=mode, value='hard')
    easy_btn.grid(row=2, column=1, sticky=E)
    hard_btn.grid(row=2, column=2, sticky=E)

    first_player_lbl = ttk.Label(content, text='Will you play first?')
    first_player_lbl.grid(row=3, column=0, sticky=W)
    global first_player
    first_player = StringVar()
    yes_btn = ttk.Radiobutton(content, text='Yes', variable=first_player, value='Yes')
    no_btn = ttk.Radiobutton(content, text='No', variable=first_player, value='No')
    yes_btn.grid(row=3, column=1, sticky=E)
    no_btn.grid(row=3, column=2, sticky=E)

    confirm_btn = ttk.Button(content, text='Confirm', command=root.destroy)
    confirm_btn.grid(row=4, column=2, sticky=E)

    btn_frame.columnconfigure(0, weight=2)
    btn_frame.columnconfigure(1, weight=2)
    btn_frame.rowconfigure(0, weight=2)
    content.columnconfigure(0, weight=2)
    content.columnconfigure(1, weight=2)
    content.columnconfigure(2, weight=2)
    content.rowconfigure(0, weight=2)
    content.rowconfigure(1, weight=2)
    content.rowconfigure(2, weight=2)
    content.rowconfigure(3, weight=2)

    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=2)

    root.mainloop()


def start_game(player1, player2):
    def is_winner(position_set):
        if len(position_set) < 3:
            return False
        
        for i in range(3):
            row = [x for x in position_set if x[0] == i]
            col = [x for x in position_set if x[1] == i]
            if len(row) == 3 or len(col) == 3:
                return True
        
        if (1, 1) in position_set:
            if (0, 0) in position_set and (2, 2) in position_set:
                return True
            elif (0, 2) in position_set and (2, 0) in position_set:
                return True
        return False

    def move_selected(root, btn, pos_x, pos_y):
        nonlocal counter
        nonlocal result
        if counter % 2:
            btn['image'] = round_image
            player2_moves.add((pos_x, pos_y))
            if is_winner(player2_moves):
               result['text'] = 'Player 2 is winner' 
        else:
            btn['image'] = cross_image
            player1_moves.add((pos_x, pos_y))
            if is_winner(player1_moves):
                result['text'] = 'Player 1 is winner'
        btn.state(['disabled'])
        counter += 1
        if counter == 9:
            result['text'] = 'Match is drawn'

    root = Tk()
    root.title('Tic Tac Toe')

    content = ttk.Frame(root)
    content.grid(row=0, column=0, sticky=NSEW)

    btn_frame = ttk.Frame(content, height=300, width=300)
    btn_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=NSEW)

    canvas = Canvas(btn_frame, height=275, width=275)
    canvas.grid(row=0, column=0, sticky=NSEW)
    
    cross_image = ImageTk.PhotoImage(Image.open('./resource/cross.png').resize((80, 80)))
    round_image = ImageTk.PhotoImage(Image.open('./resource/circle.png').resize((80, 80)))
    background_image = ImageTk.PhotoImage(Image.open('./resource/background.png').resize((80, 80)))


    button_set = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
            ]
    position_y = 5
    for i in range(3):
        position_x = 5
        for j in range(3):
            button_set[i][j] = ttk.Button(canvas, image=background_image, command= lambda i=i, j=j : move_selected(root, button_set[i][j], i, j))
            canvas.create_window(position_x, position_y, anchor='nw', window=button_set[i][j])
            position_x += 90
        position_y += 90

    info_frame = ttk.Frame(content, height=300, width=300)
    info_frame.grid(row=0, column=3, rowspan=3, sticky=NSEW)

    first_player = ttk.Label(info_frame, text='First Player')
    second_player = ttk.Button(info_frame, text='Second Player')
    result = ttk.Label(info_frame, text='WHO WINS?')

    first_player.grid(row=0, column=0)
    second_player.grid(row=1, column=0)
    result.grid(row=2, column=0)

    counter = 0
    root.mainloop()



initiate()
opponent = opponent.get()
mode = mode.get()
if first_player.get() == 'Yes':
    player1 = 'you'
    player2 = opponent
else:
    player1 = opponent
    player2 = 'you'
player1_moves = set()
player2_moves = set()
remaining_moves = set()

start_game(player1, player2)
