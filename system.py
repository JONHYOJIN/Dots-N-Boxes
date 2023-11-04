from tkinter import *
from tkinter import ttk
from itertools import combinations

from machine import MACHINE
from options import PLAYERS, BACKGROUND, RADIUS, LINE_WIDTH, LINE_COLOR, CIRCLE_WIDTH, CIRCLE_COLOR, \
                    USER_COLOR, MACHINE_COLOR, \
                    PROGRAM_SIZE, CANVAS_SIZE

class SYSTEM():
    def __init__(self):
        # Initialization
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = []
        self.whole_lines = []
        self.whole_points = []
        self.location = []
        self.squares = []

        self.interval = None
        self.offset = None

        # self.user = USER()
        self.machine = MACHINE()
        # self.referee = REFEREE()
        self.closed_square = 0
        self.board_size = 0

        self.turn = None

        # GUI
        self.root = Tk()

        # GUI Interface Settings
        self.root.configure(background=BACKGROUND)  # Background
        self.root.title("Dots & Boxes")
        self.root.geometry(PROGRAM_SIZE)
        self.root.resizable(True, True)


        """
            Reference: https://stackoverflow.com/questions/27912250/how-to-set-the-background-color-of-a-ttk-combobox
        """
        self.combostyle = ttk.Style()
        self.combostyle.theme_create('combostyle', parent='alt',
                                settings = {'TCombobox':
                                            {'configure':
                                            {'selectbackground': 'white',
                                            'fieldbackground': 'white',
                                            'background': "gray"
                                            }}}
                                )
        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        self.combostyle.theme_use('combostyle') 

        # Board
        self.label_options = Label(self.root, text="Board Size:", background=BACKGROUND)
        self.label_options.place(x=10, y=10)

        self.combobox_board = ttk.Combobox(self.root, textvariable=StringVar(), width=8, background=BACKGROUND)
        self.combobox_board['value'] = ['3 x 3', '5 x 5', '7 x 7']
        self.combobox_board.set('5 x 5')
        self.combobox_board.place(x=85, y=12)

        # Turn
        self.label_firstturn = Label(self.root, text="First Turn:", background=BACKGROUND)
        self.label_firstturn.place(x=180, y=10)

        self.combobox_firstturn = ttk.Combobox(self.root, textvariable=StringVar(), width=8, background=BACKGROUND)
        self.combobox_firstturn['value'] = PLAYERS
        self.combobox_firstturn.set("USER")
        self.combobox_firstturn.place(x=248, y=12)

        # Start Game
        self.button_startgame = Button(self.root, text="Start Game!", width=6, fg="grey20", highlightbackground=BACKGROUND, command=self.set_new_board)
        self.button_startgame.place(x=360, y=8)

        # Canvas
        self.board = Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE, background="white")
        self.board.place(x=200, y=50)

        # Turn
        turn_x, turn_y = 10, 60
        self.label_turn = Label(self.root, text="[ TURN ]", background=BACKGROUND)
        self.label_turn.place(x=turn_x, y=turn_y)
        self.label_currentturn = Label(self.root, text=self.turn, background=BACKGROUND)
        self.label_currentturn.place(x=turn_x, y=turn_y+25)

        # Score
        score_x, score_y = 10, 120
        self.label_score = Label(self.root, text="[ SCORE ]", background=BACKGROUND)
        self.label_score.place(x=score_x, y=score_y)

        self.label_userscore1 = Label(self.root, text="USER:", background=BACKGROUND)
        self.label_userscore1.place(x=score_x, y=score_y+30)
        self.label_userscore2 = Label(self.root, text=self.score[0], background=BACKGROUND)
        self.label_userscore2.place(x=score_x+45, y=score_y+30)

        self.label_machinescore1 = Label(self.root, text="MACHINE:", background=BACKGROUND)
        self.label_machinescore1.place(x=score_x, y=score_y+55)
        self.label_machinescore2 = Label(self.root, text=self.score[1], background=BACKGROUND)
        self.label_machinescore2.place(x=score_x+70, y=score_y+55)

        # User
        user_x, user_y = 10, 220
        self.label_user = Label(self.root, text="[ USER ]", background=BACKGROUND, fg=USER_COLOR)
        self.label_user.place(x=user_x, y=user_y)

        self.label_userstart = Label(self.root, text="From:", background=BACKGROUND)
        self.label_userstart.place(x=user_x, y=user_y+25)
        self.start_x = Entry(self.root, textvariable=IntVar(), width=3, highlightbackground=BACKGROUND)
        self.start_x.place(x=user_x+40, y=user_y+25)
        self.start_y = Entry(self.root, textvariable=IntVar(), width=3, highlightbackground=BACKGROUND)
        self.start_y.place(x=user_x+80, y=user_y+25)

        self.label_userend = Label(self.root, text="    To:", background=BACKGROUND)
        self.label_userend.place(x=user_x, y=user_y+55)
        self.end_x = Entry(self.root, textvariable=IntVar(), width=3, highlightbackground=BACKGROUND)
        self.end_x.place(x=user_x+40, y=user_y+55)
        self.end_y = Entry(self.root, textvariable=IntVar(), width=3, highlightbackground=BACKGROUND)
        self.end_y.place(x=user_x+80, y=user_y+55)

        self.label_usergo = Button(self.root, text="Go!", width=10, fg="grey20", highlightbackground=BACKGROUND, command=self.user_go)
        self.label_usergo.place(x=user_x, y=user_y+80)

        # Machine
        machine_x, machine_y = 10, 350
        self.label_machine = Label(self.root, text="[ MACHINE ]", background=BACKGROUND, fg=MACHINE_COLOR)
        self.label_machine.place(x=machine_x, y=machine_y)

        self.label_machinego = Button(self.root, text="Go!", width=10, fg="grey20", highlightbackground=BACKGROUND, command=self.machine_go)
        self.label_machinego.place(x=machine_x, y=machine_y+25)

        # Warning
        warning_x, warning_y = 10, 405
        self.label_warning = Label(self.root, text="", background=BACKGROUND)
        self.label_warning.place(x=warning_x, y=warning_y)

        # Result
        result_x, result_y = 10, 435
        self.label_result = Label(self.root, text="The game is ongoing!!", background=BACKGROUND)
        self.label_result.place(x=result_x, y=result_y)

        self.root.mainloop()
    
    # Canvas(Board)-related Functions
    def set_new_board(self):
        size = self.combobox_board.get()

        # Board Size
        self.board_size = int(size.split(" ")[0])

        # Initialization
        self.score = [0, 0]
        self.drawn_lines = []
        self.whole_points = []
        self.whole_lines = []
        self.board.delete(ALL)

        self.initialize_turn()

        self.interval = CANVAS_SIZE // (self.board_size+2)
        self.offset = (CANVAS_SIZE % (self.board_size+2)) // 2
        self.location = [x*self.interval+self.offset for x in range(1, (self.board_size+2))]
        idx_offset = 200 // self.board_size

        for idx_x, loc_x in enumerate(self.location):
            self.board.create_text((self.location[0]+idx_x*self.interval, self.location[0]-idx_offset), text=idx_x, width=5, fill="gray", font=("Arial", 16))
            self.board.create_text((self.location[0]-idx_offset, self.location[0]+idx_x*self.interval), text=idx_x, width=5, fill="gray", font=("Arial", 16))
            for idx_y, loc_y in enumerate(self.location):
                self.circle(loc_x, loc_y, CIRCLE_COLOR)
                self.whole_points.append((idx_x, idx_y))
        
        self.whole_lines = self.find_whole_lines()
        

    def circle(self, cx, cy, color):
        self.board.create_oval(cx-RADIUS, cy-RADIUS, cx+RADIUS, cy+RADIUS, fill=color, width=CIRCLE_WIDTH)
    
    def line(self, start, end, color):
        self.board.create_line(start[0], start[1], end[0], end[1], fill=color, width=LINE_WIDTH)
    
    def occupy_square(self, square):
        upper_left = square[0][0]
        lower_right = square[-1][-1]
        if self.turn == "USER":
            self.board.create_rectangle(self.offset+self.interval*(upper_left[0]+1), self.offset+self.interval*(upper_left[1]+1), \
                                        self.offset+self.interval*(lower_right[0]+1), self.offset+self.interval*(lower_right[1]+1), \
                                        fill=USER_COLOR)
        elif self.turn == "MACHINE":
            self.board.create_rectangle(self.offset+self.interval*(upper_left[0]+1), self.offset+self.interval*(upper_left[1]+1), \
                                        self.offset+self.interval*(lower_right[0]+1), self.offset+self.interval*(lower_right[1]+1), \
                                        fill=MACHINE_COLOR)
    
    def find_whole_lines(self):
        return [[a, b] for (a, b) in list(combinations(self.whole_points, 2)) if (a[0]-b[0])**2 + (a[1]-b[1])**2 == 1]
    
    def user_go(self):
        start_x = int(self.start_x.get())
        start_y = int(self.start_y.get())
        end_x = int(self.end_x.get())
        end_y = int(self.end_y.get())

        start_x, start_y, end_x, end_y = self.organize_points(start_x, start_y, end_x, end_y)

        if self.check_availability("USER", start_x, start_y, end_x, end_y):
            self.label_warning.config(text="")
            line = [(start_x, start_y), (end_x, end_y)]
            self.drawn_lines.append(line)

            draw = [(self.location[start_x], self.location[start_y]), (self.location[end_x], self.location[end_y])]
            self.line(draw[0], draw[1], color=LINE_COLOR)

            self.whole_lines.remove(line)

            if not self.check_square(line):
                self.change_turn() # 점수 획득이 없을 시

            self.label_userscore2.config(text=self.score[0])

            if not self.whole_lines or max(self.score)>=((self.board_size**2 // 2) + 1):
                f = lambda i: self.score[i]
                winner = PLAYERS[max(range(len(self.score)), key=f)]
                self.label_result.config(text=f"The Winner is {winner}!!")


        else:
            self.label_warning.config(text="Check the turn or the input!")
    
    def machine_go(self):
        self.machine.score = self.score
        self.machine.drawn_lines = self.drawn_lines
        self.machine.whole_lines = self.whole_lines
        self.machine.location = self.location

        line = self.machine.find_best_selection()

        start_x, start_y, end_x, end_y = self.organize_points(line[0][0], line[0][1], line[1][0], line[1][1])

        if self.check_availability("MACHINE", start_x, start_y, end_x, end_y ):
            self.label_warning.config(text="")
            line = [(start_x, start_y), (end_x, end_y)]
            self.drawn_lines.append(line)

            draw = [(self.location[start_x], self.location[start_y]), (self.location[end_x], self.location[end_y])]
            self.line(draw[0], draw[1], color=LINE_COLOR)

            self.whole_lines.remove(line)

            if not self.check_square(line):
                self.change_turn() # 점수 획득이 없을 시

            self.label_machinescore2.config(text=self.score[1])

            if not self.whole_lines or max(self.score)>=((self.board_size**2 // 2) + 1):
                f = lambda i: self.score[i]
                winner = PLAYERS[max(range(len(self.score)), key=f)]
                self.label_result.config(text=f"The Winner is {winner}!!")

        else:
            self.label_warning.config(text="Check the turn \nor the machine error!")
    
    def check_availability(self, turn, start_x, start_y, end_x, end_y):
        line = [(start_x, start_y), (end_x, end_y)]

        # Must be in the range
        condition1 = ((start_x in range(self.board_size+1)) and (start_y in range(self.board_size+1)) \
                    and (end_x in range(self.board_size+1)) and (end_y in range(self.board_size+1)))
        
        # Distance = 1 (Cannot be same points)
        condition2 = ((start_x - end_x)**2 + (start_y - end_y)**2 == 1)

        # Must be one of the whole lines
        condition3 = (line in self.whole_lines)

        # Must be new line
        condition4 = (line not in self.drawn_lines)

        # Must be own turn
        condition5 = (self.turn==turn)

        if  condition1 and condition2 and condition3 and condition4 and condition5:
            return True
        else:
            return False    
    
    def organize_points(self, start_x, start_y, end_x, end_y):
        if start_x < end_x:
            return start_x, start_y, end_x, end_y
        else:
            if start_x == end_x and start_y < end_y:
                return start_x, start_y, end_x, end_y
            else:
                return end_x, end_y, start_x, start_y
    
    # Score Checking Functions
    def check_square(self, line):
        get_score = False

        point1 = line[0]
        point2 = line[1]
        
        is_vertical = (point1[0]==point2[0])
        is_horizontal = (point1[1]==point2[1])

        if is_vertical:
            if (point1[0]==0): # Left Border
                right_square = [[point1, (point1[0],point1[1]+1)], \
                                [point1, (point1[0]+1,point1[1])], \
                                [(point1[0],point1[1]+1), (point1[0]+1,point1[1]+1)], \
                                [(point1[0]+1,point1[1]), (point1[0]+1,point1[1]+1)]]
                if all([line in self.drawn_lines for line in right_square]) and (right_square not in self.squares):
                    self.squares.append(right_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(right_square)
                    get_score = True
                

            elif (point1[0]==self.board_size): # Right Border
                left_square = [[(point1[0]-1,point1[1]), (point1[0]-1,point1[1]+1)], \
                               [(point1[0]-1,point1[1]), point1], \
                               [(point1[0]-1,point1[1]+1), (point1[0],point1[1]+1)], \
                               [point1, (point1[0],point1[1]+1)]]

                if all([line in self.drawn_lines for line in left_square]) and (left_square not in self.squares):
                    self.squares.append(left_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(left_square)
                    get_score = True
                
            else:
                right_square = [[point1, (point1[0],point1[1]+1)], \
                                [point1, (point1[0]+1,point1[1])], \
                                [(point1[0],point1[1]+1), (point1[0]+1,point1[1]+1)], \
                                [(point1[0]+1,point1[1]), (point1[0]+1,point1[1]+1)]]
                if all([line in self.drawn_lines for line in right_square]) and (right_square not in self.squares):
                    self.squares.append(right_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(right_square)
                    get_score = True

                left_square = [[(point1[0]-1,point1[1]), (point1[0]-1,point1[1]+1)], \
                               [(point1[0]-1,point1[1]), point1], \
                               [(point1[0]-1,point1[1]+1), (point1[0],point1[1]+1)], \
                               [point1, (point1[0],point1[1]+1)]]
                if all([line in self.drawn_lines for line in left_square]) and (left_square not in self.squares):
                    self.squares.append(left_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(left_square)
                    get_score = True
        
        elif is_horizontal:
            if (point1[1]==0): # Upper Border
                lower_square = [[point1, (point1[0],point1[1]+1)], \
                                [point1, (point1[0]+1,point1[1])], \
                                [(point1[0],point1[1]+1), (point1[0]+1,point1[1]+1)], \
                                [(point1[0]+1,point1[1]), (point1[0]+1,point1[1]+1)]]
                if all([line in self.drawn_lines for line in lower_square]) and (lower_square not in self.squares):
                    self.squares.append(lower_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(lower_square)
                    get_score = True

            elif (point1[1]==self.board_size): # Lower Border
                upper_square = [[(point1[0],point1[1]-1), point1], \
                                [(point1[0],point1[1]-1), (point1[0]+1,point1[1]-1)], \
                                [point1, (point1[0]+1,point1[1])], \
                                [(point1[0]+1,point1[1]-1), (point1[0]+1,point1[1])]]

                if all([line in self.drawn_lines for line in upper_square]) and (upper_square not in self.squares):
                    self.squares.append(upper_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(upper_square)
                    get_score = True
                
            else:
                lower_square = [[point1, (point1[0],point1[1]+1)], \
                                [point1, (point1[0]+1,point1[1])], \
                                [(point1[0],point1[1]+1), (point1[0]+1,point1[1]+1)], \
                                [(point1[0]+1,point1[1]), (point1[0]+1,point1[1]+1)]]
                if all([line in self.drawn_lines for line in lower_square]) and (lower_square not in self.squares):
                    self.squares.append(lower_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(lower_square)
                    get_score = True

                upper_square = [[(point1[0],point1[1]-1), point1], \
                                [(point1[0],point1[1]-1), (point1[0]+1,point1[1]-1)], \
                                [point1, (point1[0]+1,point1[1])], \
                                [(point1[0]+1,point1[1]-1), (point1[0]+1,point1[1])]]

                if all([line in self.drawn_lines for line in upper_square]) and (upper_square not in self.squares):
                    self.squares.append(upper_square)
                    self.score[PLAYERS.index(self.turn)]+=1
                    self.occupy_square(upper_square)
                    get_score = True
                
        return get_score

    # Turn-related Functions
    def check_turn(self):
        if self.turn:
            return self.turn
        else:
            return self.combobox_firstturn.get()
    
    def initialize_turn(self):
        turn = self.check_turn()
        if turn == "USER":
            self.turn = turn
            self.label_currentturn.config(text=turn, fg=USER_COLOR)

        elif turn == "MACHINE":
            self.turn = turn
            self.label_currentturn.config(text=turn, fg=MACHINE_COLOR)
        
    def change_turn(self):
        turn = self.check_turn()
        if turn == "USER":
            self.turn = "MACHINE"
            self.label_currentturn.config(text=self.turn, fg=MACHINE_COLOR)

        elif turn == "MACHINE":
            self.turn = "USER"
            self.label_currentturn.config(text=self.turn, fg=USER_COLOR)
    
