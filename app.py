import tkinter as tk
import pyttsx3
import string
import threading

THEME_DATA = {
    "A": ("A is for Ant 🐜", "#FFD700"),
    "B": ("B is for Ball ⚽", "#87CEFA"),
    "C": ("C is for Cat 🐱", "#FFB6C1"),
    "D": ("D is for Dog 🐶", "#EDC9AF"),
    "E": ("E is for Elephant 🐘", "#E6E6FA"),
    "F": ("F is for Fox 🦊", "#228B22"),
    "G": ("G is for Goat 🐐", "#32CD32"),
    "H": ("H is for Hen 🐔", "#FFFACD"),
    "I": ("I is for Ice 🧊", "#E0FFFF"),
    "J": ("J is for Jug 🫖", "#FF69B4"),
    "K": ("K is for Kite 🪁", "#87CEFA"),
    "L": ("L is for Lion 🦁", "#FF8C00"),
    "M": ("M is for Monkey 🐒", "#8B4513"),
    "N": ("N is for Nose 👃", "#D2B48C"),
    "O": ("O is for Orange 🍊", "#FFA500"),
    "P": ("P is for Pen 🖊️", "#800080"),
    "Q": ("Q is for Queen 👸", "#DA70D6"),
    "R": ("R is for Rain 🌧️", "#708090"),
    "S": ("S is for Sun ☀️", "#FFFF00"),
    "T": ("T is for Tiger 🐯", "#FF4500"),
    "U": ("U is for Umbrella ☂️", "#DA70D6"),
    "V": ("V is for Van 🚐", "#C0C0C0"),
    "W": ("W is for Watch ⌚", "#0077be"),
    "X": ("X is for Xylophone 🪘", "#C0C0C0"),
    "Y": ("Y is for Yam 🍠", "#DEB887"),
    "Z": ("Z is for Zebra 🦓", "#FFFFFF")
}

is_learning_mode = False
use_female_voice = False 

def speak(text):
    def run_speech():
        try:
            
            clean_text = text.encode('ascii', 'ignore').decode('ascii')
            
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            
            if use_female_voice and len(voices) > 1:
                temp_engine.setProperty('voice', voices[1].id)
            else:
                temp_engine.setProperty('voice', voices[0].id)
                
            temp_engine.setProperty('rate', 150)
            temp_engine.say(clean_text)
            temp_engine.runAndWait()
            temp_engine.stop() 
        except:
            pass

    threading.Thread(target=run_speech, daemon=True).start()

def toggle_voice():
    global use_female_voice
    use_female_voice = not use_female_voice
    label = "Female" if use_female_voice else "Male"
    voice_btn.config(text=f"🎙️ Voice: {label}", bg="#FF69B4" if use_female_voice else "#4682B4")
    speak(f"{label} voice selected")

def toggle_mode():
    global is_learning_mode
    is_learning_mode = not is_learning_mode
    mode_btn.config(text="🏫 Learning Mode" if is_learning_mode else "⌨️ Typing Mode")
    clear_word()

def add_letter(letter):
    word_entry.delete(0, tk.END) 
    if is_learning_mode:
        display_text, color = THEME_DATA.get(letter, (letter, "red"))
        word_entry.insert(tk.END, display_text)
        root.configure(bg=color)
        frame.configure(bg=color)
        speak(display_text)
    else:
        word_entry.insert(tk.END, letter)
        speak(letter)

def speak_full_text():
    
    current_text = word_entry.get()
    if current_text:
        speak(current_text)

def clear_word():
    word_entry.delete(0, tk.END)
    root.configure(bg="#F5F5F5")
    frame.configure(bg="#F5F5F5")

root = tk.Tk()
root.title("")
root.geometry("850x800")
root.configure(bg="#F5F5F5")

control_frame = tk.Frame(root, bg="#F5F5F5")
control_frame.pack(pady=10)

mode_btn = tk.Button(control_frame, text="⌨️ Typing Mode", font=("Arial", 12, "bold"), 
                     command=toggle_mode, width=20)
mode_btn.grid(row=0, column=0, padx=10)

voice_btn = tk.Button(control_frame, text="👨 Voice: Male", font=("Arial", 12, "bold"), 
                      command=toggle_voice, width=20, bg="#4682B4", fg="white")
voice_btn.grid(row=0, column=1, padx=10)

frame = tk.Frame(root, bg="#F5F5F5")
frame.pack(pady=10)

colors = ["#FFB6C1", "#87CEFA", "#98FB98", "#FFD700", "#E6E6FA", "#FFA07A", "#20B2AA", "#FF69B4"]
letters = string.ascii_uppercase

word_entry = tk.Entry(root, font=("Segoe UI Emoji", 24, "bold"), width=30, justify="center")
word_entry.pack(pady=20)

row, col = 0, 0
for letter in letters:
    btn = tk.Button(frame, text=letter, font=("Arial", 20, "bold"), width=4, height=2,
                   bg=colors[(row * 7 + col) % len(colors)],
                   command=lambda l=letter: add_letter(l))
    btn.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col == 7:
        col = 0
        row += 1

speak_btn = tk.Button(root, text="🔊 Repeat / click to speak", font=("Arial", 16, "bold"),
                      bg="#20B2AA", fg="white", command=speak_full_text, width=25)
speak_btn.pack(pady=10)

clear_btn = tk.Button(root, text="❌ Reset/clear", font=("Arial", 14), 
                      bg="#FF6347", fg="white", command=clear_word, width=20)
clear_btn.pack(pady=5)

root.mainloop()