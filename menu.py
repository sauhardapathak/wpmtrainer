import customtkinter as ctk
import subprocess
import sys
import os
from highscore import load_highscore

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TypingGameMenu:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("WPM Trainer")
        
        # Center window on screen
        window_width = 900
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Prevent resizing
        self.root.resizable(False, False)
        
        # Store high score
        self.high_score = load_highscore()
        
        self.show_main_menu()
        
    def show_main_menu(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create centered frame (vertical center is fine here - not much content)
        center_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ctk.CTkLabel(
            center_frame, 
            text="WPM TRAINER", 
            font=("Impact", 70),
            text_color=("#00ff96")
        )
        title.pack(pady=40)
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            center_frame,
            text="Test Your Typing Speed",
            font=("Arial", 20),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))
        
        # Start button
        start_btn = ctk.CTkButton(
            center_frame,
            text="Start Game",
            font=("Impact", 30),
            width=350,
            height=65,
            corner_radius=10,
            command=self.show_difficulty_menu
        )
        start_btn.pack(pady=12)
        
        # High score button
        highscore_btn = ctk.CTkButton(
            center_frame,
            text="High Score",
            font=("Impact", 30),
            width=350,
            height=65,
            corner_radius=10,
            command=self.show_high_score
        )
        highscore_btn.pack(pady=12)
        
        # Instructions button
        instructions_btn = ctk.CTkButton(
            center_frame,
            text="Instructions",
            font=("Impact", 30),
            width=350,
            height=65,
            corner_radius=10,
            command=self.show_instructions
        )
        instructions_btn.pack(pady=12)
        
        # Quit button
        quit_btn = ctk.CTkButton(
            center_frame,
            text="Quit",
            font=("Impact", 30),
            width=350,
            height=65,
            corner_radius=10,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.root.quit
        )
        quit_btn.pack(pady=12)
    
    def show_difficulty_menu(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Use scrollable frame for tall content
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.place(relx=0.5, rely=0, anchor="n", y=30)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Select Difficulty",
            font=("Impact", 55)
        )
        title.pack(pady=20)
        
        # Easy button
        easy_btn = ctk.CTkButton(
            main_frame,
            text="🟢 EASY",
            font=("Impact", 32),
            width=400,
            height=70,
            corner_radius=10,
            fg_color="#4caf50",
            hover_color="#388e3c",
            command=lambda: self.start_game("easy")
        )
        easy_btn.pack(pady=15)
        
        easy_desc = ctk.CTkLabel(
            main_frame,
            text="Slow words  •  4 letters  •  5 second spawn",
            font=("Arial", 16),
            text_color="gray"
        )
        easy_desc.pack(pady=(0, 20))
        
        # Medium button
        medium_btn = ctk.CTkButton(
            main_frame,
            text="🟡 MEDIUM",
            font=("Impact", 32),
            width=400,
            height=70,
            corner_radius=10,
            fg_color="#ff9800",
            hover_color="#f57c00",
            command=lambda: self.start_game("medium")
        )
        medium_btn.pack(pady=15)
        
        medium_desc = ctk.CTkLabel(
            main_frame,
            text="Normal speed  •  6 letters  •  4 second spawn",
            font=("Arial", 16),
            text_color="gray"
        )
        medium_desc.pack(pady=(0, 20))
        
        # Hard button
        hard_btn = ctk.CTkButton(
            main_frame,
            text="🔴 HARD",
            font=("Impact", 32),
            width=400,
            height=70,
            corner_radius=10,
            fg_color="#f44336",
            hover_color="#d32f2f",
            command=lambda: self.start_game("hard")
        )
        hard_btn.pack(pady=15)
        
        hard_desc = ctk.CTkLabel(
            main_frame,
            text="Fast words  •  8 letters  •  2.5 second spawn",
            font=("Arial", 16),
            text_color="gray"
        )
        hard_desc.pack(pady=(0, 30))
        
        # Back button
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Back",
            font=("Impact", 26),
            width=250,
            height=55,
            corner_radius=10,
            command=self.show_main_menu
        )
        back_btn.pack(pady=20)
    
    def start_game(self, difficulty):
        # Hide menu
        self.root.withdraw()
        
        # Launch game and wait
        subprocess.run([sys.executable, "wpmtrain.py", difficulty])
        
        # Reload high score from file (it may have changed)
        self.high_score = load_highscore()
        
        # Show menu again
        self.root.deiconify()
        self.show_main_menu()
    
    def show_high_score(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create centered frame
        center_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="🏆 High Score",
            font=("Impact", 55)
        )
        title.pack(pady=30)
        
        # Score box
        score_box = ctk.CTkFrame(center_frame, fg_color="#1e1e1e", corner_radius=15)
        score_box.pack(pady=20, padx=40, fill="x")
        
        score_label = ctk.CTkLabel(
            score_box,
            text=f"{self.high_score}",
            font=("Impact", 80),
            text_color="#00ff96"
        )
        score_label.pack(pady=40)
        
        score_text = ctk.CTkLabel(
            score_box,
            text="Words Typed",
            font=("Arial", 20),
            text_color="gray"
        )
        score_text.pack(pady=(0, 30))
        
        # Back button
        back_btn = ctk.CTkButton(
            center_frame,
            text="← Back",
            font=("Impact", 28),
            width=300,
            height=60,
            corner_radius=10,
            command=self.show_main_menu
        )
        back_btn.pack(pady=30)
    
    def show_instructions(self):
    # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Use frame anchored to top
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.place(relx=0.5, rely=0, anchor="n", y=15)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="📖 How to Play",
            font=("Impact", 50)
        )
        title.pack(pady=15)
        
        # Instructions box
        instructions_box = ctk.CTkFrame(main_frame, fg_color="#1e1e1e", corner_radius=15, width=700)
        instructions_box.pack(pady=15, padx=50)
        
        instructions = """
    1.  Words fall from the top of the screen

    2.  Type each word exactly as shown

    3.  Words disappear when typed correctly

    4.  You have 3 lives ♥ ♥ ♥

    5.  Missing a word costs 1 life

    6.  Game ends at 0 lives

    7.  Use BACKSPACE to fix mistakes

    8.  Press ESC to return to menu

            Try to get the highest score!
    """
        
        instructions_label = ctk.CTkLabel(
            instructions_box,
            text=instructions,
            font=("Courier", 17),
            justify="left"
        )
        instructions_label.pack(pady=25, padx=40)
        
        # Back button
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Back",
            font=("Impact", 26),
            width=280,
            height=55,
            corner_radius=10,
            command=self.show_main_menu
        )
        back_btn.pack(pady=15)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    menu = TypingGameMenu()
    menu.run()