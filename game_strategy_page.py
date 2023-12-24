import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Label
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton, CTkScrollableFrame, CTkCheckBox, CTkEntry
import customtkinter as ctk
from PIL import ImageTk, Image
import os
import sys


class GameStrategy:
    def __init__(self):
        self.root = CTk()
        self.root.title("Game Strategy")
        self.root.geometry('1200x500')
        self.root.resizable(False, False)
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("dark-blue")
        self.speed = tk.IntVar(value=5)
        self.mode = tk.StringVar(value="normal")
        self.difficulty = tk.StringVar(value="easy")
        self.player = tk.StringVar(value="ai")
        
        image = Image.open("assets/game_strategy_background.jpg")
        resized_image = image.resize((1500, 700), Image.ANTIALIAS)
        background = ImageTk.PhotoImage(resized_image)
        background_label = CTkLabel(self.root, image= background, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.puzzle_frame = CTkFrame(self.root, width=500)
        self.puzzle_frame.pack(side = 'left', padx = [500,80])
        
        self.speed_label = CTkLabel(self.puzzle_frame, text="Speed", font=("joystix monospace", 12))
        self.speed_label.pack()

        self.speed_slider2 = CTkSlider(self.puzzle_frame, from_=1, to=10, number_of_steps=10, orientation='horizontal', button_color=("#1B558D","#504CD1"))
        self.speed_slider2.pack()
        
        self.radio_frame = CTkFrame(self.puzzle_frame, width=90)
        self.radio_frame.pack(pady = 5, padx = 70)
        
        self.player_label = CTkLabel(self.radio_frame, text="PLAYER", font=("joystix monospace", 12))
        self.player_label.pack()
        
        self.user_player = CTkRadioButton(self.radio_frame, value="user", text="USER", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.player, command=self.set_player("user"))
        self.user_player.pack(anchor='e' ,padx=80, pady=2)
        self.ai_player = CTkRadioButton(self.radio_frame, value="ai", text="AI", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.player, command=self.set_player("ai"))
        self.ai_player.pack(anchor='e',padx=80, pady=10)
        
        self.radio_frame2 = CTkFrame(self.puzzle_frame, width=90)
        self.radio_frame2.pack(pady = 5)
        
        self.player_label = CTkLabel(self.radio_frame2, text="DIFFICULTY", font=("joystix monospace", 12))
        self.player_label.pack()
        
        self.easy_game = CTkRadioButton(self.radio_frame2, value="Easy", text="Easy", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.difficulty, command=self.set_difficulty("easy"))
        self.easy_game.pack(anchor='e' ,padx=80, pady=2)
        self.medium_game = CTkRadioButton(self.radio_frame2, value="Medium", text="Medium", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.difficulty, command=self.set_difficulty("medium"))
        self.medium_game.pack(anchor='e',padx=80, pady=5)
        self.hard_game = CTkRadioButton(self.radio_frame2, value="Hard", text="Hard", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.difficulty, command=self.set_difficulty("hard"))
        self.hard_game.pack(anchor='e',padx=80, pady=5)
        
        self.radio_frame3 = CTkFrame(self.puzzle_frame, width=90)
        self.radio_frame3.pack(pady = 5)
        
        self.mode_label = CTkLabel(self.radio_frame3, text="Mode", font=("joystix monospace", 12))
        self.mode_label.pack()
        
        self.normal_game = CTkRadioButton(self.radio_frame3, value="normal", text="Normal", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.mode, command=self.set_mode("normal"))
        self.normal_game.pack(anchor='c', pady=2)
        self.interactive_game = CTkRadioButton(self.radio_frame3, value="interactive", text="Interactive", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.mode, command=self.set_mode("interactive"))
        self.interactive_game.pack(anchor='c', padx = 50, pady=5)
        
        button_frame = CTkFrame(self.puzzle_frame)
        button_frame.pack(pady=10)
        
        self.start_button2 = CTkButton(button_frame, command= self.go_to_game_page(), text="Start", font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.start_button2.pack( pady=10, padx=10)
        
        # self.change_puzzle_button = CTkButton(button_frame, text="Generate Puzzle", font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        # self.change_puzzle_button.pack(side='left', padx=10)
        
        
        # self.analysis_frame = CTkScrollableFrame(self.root, width = 350, height=250)
        # self.analysis_frame.pack(side='left', padx = 10)
        
        
    def set_player(self,player):
        self.player = player
    
    def set_difficulty(self,difficulty):
        self.difficulty = difficulty

    def set_mode(self,mode):
        self.mode = mode
    
    def set_speed(self):
        # self.speed = self.speed_slider2.get()
        print(self.speed)
        
    def go_to_game_page(self):
        player = self.player
        difficulty = self.difficulty
        mode = self.mode
        speed = self.speed_slider2.get()
        
        if sys.platform.startswith('linux'):
            os.system(f'python3 game_page.py {player} {difficulty} {mode} {speed}')
        
        else:
            os.system(f'python game_page.py {player} {difficulty} {mode} {speed}')
    
    
    
    def run(self):
        # Show the puzzle visualization
        self.root.mainloop()
        
        
        
        
        
app = GameStrategy()
print(app.__dir__)
app.run()
