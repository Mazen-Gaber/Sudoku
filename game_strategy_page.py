import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Label
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton, CTkScrollableFrame, CTkCheckBox, CTkEntry
import customtkinter as ctk
from PIL import ImageTk, Image
import os
import sys

import warnings
warnings.filterwarnings("ignore")

class GameStrategy:
    def __init__(self):
        self.root = CTk()
        self.root.title("Game Strategy")
        self.root.geometry('1200x500')
        self.root.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        
        self.speed = tk.IntVar(value=5)
        self.mode = tk.StringVar(value="normal")
        self.difficulty = tk.StringVar(value="easy")
        self.player = tk.StringVar(value="ai")
        
        image = Image.open("assets/game_strategy_background.jpg")
        resized_image = image.resize((1500, 700), Image.LANCZOS)
        background = ImageTk.PhotoImage(resized_image)
        background_label = CTkLabel(self.root, image= background, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.puzzle_frame = CTkFrame(self.root, width=500)
        self.puzzle_frame.pack(side = 'left', padx = [500,80])
        
        self.speed_label = CTkLabel(self.puzzle_frame, text="Speed", font=("Arial Black", 16))
        self.speed_label.pack()

        self.speed_slider2 = CTkSlider(self.puzzle_frame, from_=1, to=10, number_of_steps=10, orientation='horizontal', button_color=("#1B558D","#D53D44"), variable=self.speed)
        self.speed_slider2.pack()
        
        self.radio_frame = CTkFrame(self.puzzle_frame, width=90)
        self.radio_frame.pack(pady = [10,5], padx = 70)
        
        self.player_label = CTkLabel(self.radio_frame, text="PLAYER", font=("Arial Black", 16))
        self.player_label.pack(pady = 5)
        
        self.user_player = CTkRadioButton(self.radio_frame, value="user", text="User", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.player)
        self.user_player.pack(anchor='e' ,padx=80, pady=2)
        self.ai_player = CTkRadioButton(self.radio_frame, value="ai", text="AI", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.player)
        self.ai_player.pack(anchor='e',padx=80, pady=10)
        
        self.radio_frame2 = CTkFrame(self.puzzle_frame, width=90)
        self.radio_frame2.pack(pady = 5)
        
        self.player_label = CTkLabel(self.radio_frame2, text="DIFFICULTY", font=("Arial Black", 16))
        self.player_label.pack()
        
        self.easy_game = CTkRadioButton(self.radio_frame2, value="Easy", text="Easy", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.difficulty)
        self.easy_game.pack(anchor='e' ,padx=80, pady=2)
        self.medium_game = CTkRadioButton(self.radio_frame2, value="Medium", text="Medium", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.difficulty)
        self.medium_game.pack(anchor='e',padx=80, pady=5)
        self.hard_game = CTkRadioButton(self.radio_frame2, value="Hard", text="Hard", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.difficulty)
        self.hard_game.pack(anchor='e',padx=80, pady=5)
        
        self.radio_frame3 = CTkFrame(self.puzzle_frame, width=90)
        self.radio_frame3.pack(pady = [5,10])
        
        self.mode_label = CTkLabel(self.radio_frame3, text="MODE", font=("Arial Black", 16))
        self.mode_label.pack()
        
        self.normal_game = CTkRadioButton(self.radio_frame3, value="normal", text="Normal", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.mode)
        self.normal_game.pack(anchor='c', pady=2)
        self.interactive_game = CTkRadioButton(self.radio_frame3, value="interactive", text="Interactive", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"), variable=self.mode)
        self.interactive_game.pack(anchor='c', padx = 70, pady=5)
        
        button_frame = CTkFrame(self.puzzle_frame)
        button_frame.pack(pady=10)
        
        self.start_button2 = CTkButton(button_frame, command= self.go_to_game_page, text="Start", font=("Arial Black", 16), fg_color=("#3A7EBF","#D53D44"))
        self.start_button2.pack( pady=10, padx=10)
        
        
        
    def go_to_game_page(self):
        player = self.player.get()
        difficulty = self.difficulty.get()
        mode = self.mode.get()
        speed = int(self.speed.get())
        print(player, difficulty, mode, speed)
        
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
