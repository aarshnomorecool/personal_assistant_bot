# assistant_gui.py

import tkinter as tk
from tkinter import scrolledtext
from main import get_ai_response, load_memory, save_memory

# Load memory
memory = load_memory()

# 🧠 Handle Send Button
def send_message():
    user_input = user_entry.get().strip()
    if not user_input:
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"\n🧑 You: {user_input}\n", "user")
    user_entry.delete(0, tk.END)

    # Special memory commands
    if user_input.startswith("remember "):
        try:
            key, value = user_input.replace("remember ", "").split(" as ")
            memory[key.strip()] = value.strip()
            save_memory(memory)
            chat_area.insert(tk.END, f"✅ Assistant: Got it! Remembered {key.strip()}.\n", "bot")
        except:
            chat_area.insert(tk.END, "⚠️ Format: remember [thing] as [value]\n", "bot")

    elif user_input.startswith("recall "):
        key = user_input.replace("recall ", "").strip()
        value = memory.get(key, "❓ I don't remember that.")
        chat_area.insert(tk.END, f"🧠 Assistant: {value}\n", "bot")

    else:
        chat_area.insert(tk.END, "🤖 Assistant: Thinking...\n", "bot")
        chat_area.see(tk.END)
        chat_area.update()

        reply = get_ai_response(user_input, memory)
        chat_area.insert(tk.END, f"{reply}\n", "bot")

    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED)

# 🪟 GUI Setup
root = tk.Tk()
root.title("🧠 Qwerky AI Personal Assistant")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

# 🪟 Style configuration
style_dark = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "insertbackground": "#ffffff",
    "font": ("Consolas", 12)
}

# 💬 Chat Display Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, **style_dark)
chat_area.tag_config("user", foreground="#00ffff")
chat_area.tag_config("bot", foreground="#ffcc66")
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# 💡 User Input Field
user_entry = tk.Entry(root, **style_dark)
user_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
user_entry.bind("<Return>", lambda event: send_message())

# 🚀 Send Button
send_button = tk.Button(root, text="Send", command=send_message, bg="#333", fg="#fff", activebackground="#555", relief="raised")
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# 🧱 Responsive Grid Configuration
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# 🟢 Launch GUI
root.mainloop()
