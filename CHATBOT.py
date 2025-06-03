import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pygame.pkgdata')

import tkinter as tk
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import threading
import time
import uuid

pygame.mixer.init()

# Chatbot reply logic
def get_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi there! How can I help you?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm functioning properly!"
    elif "bye" in user_input:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I don't understand that."

# Text-to-speech using gTTS and pygame
def speak(text):
    unique_id = str(uuid.uuid4())
    filename = f"voice_{unique_id}.mp3"
    try:
        tts = gTTS(text=text)
        tts.save(filename)
        time.sleep(0.5)  # Wait for file to finish saving
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                pass  # File is still being used, safe to ignore

# Process user input (text)
def process_input():
    user_input = entry.get()
    chatbox.insert(tk.END, "You: " + user_input)
    entry.delete(0, tk.END)

    response = get_response(user_input)
    chatbox.insert(tk.END, "Bot: " + response)

    threading.Thread(target=speak, args=(response,)).start()

# Voice input using microphone
def use_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chatbox.insert(tk.END, "Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            chatbox.insert(tk.END, "You (voice): " + user_input)

            response = get_response(user_input)
            chatbox.insert(tk.END, "Bot: " + response)
            threading.Thread(target=speak, args=(response,)).start()

        except sr.UnknownValueError:
            chatbox.insert(tk.END, "Bot: Sorry, I couldn't understand that.")
        except sr.RequestError:
            chatbox.insert(tk.END, "Bot: Network error.")

# GUI setup
root = tk.Tk()
root.title("Simple Chatbot")

chatbox = tk.Listbox(root, width=50, height=15)
chatbox.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=(10, 0))

send_btn = tk.Button(root, text="Send", command=process_input)
send_btn.pack(side=tk.LEFT)

voice_btn = tk.Button(root, text="🎤", command=use_voice)
voice_btn.pack(side=tk.LEFT)

root.mainloop()
