import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import json
from tkinter.font import Font

# Color Themes
THEMES = {
    "dark": {
        "background": "#2E3440",
        "text": "#ECEFF4",
        "primary": "#5E81AC",
        "secondary": "#81A1C1",
        "accent": "#88C0D0",
        "success": "#A3BE8C",
        "warning": "#EBCB8B",
        "error": "#BF616A",
        "card": "#3B4252",
        "highlight": "#8FBCBB"
    },
    "light": {
        "background": "#ECEFF4",
        "text": "#2E3440",
        "primary": "#81A1C1",
        "secondary": "#5E81AC",
        "accent": "#88C0D0",
        "success": "#A3BE8C",
        "warning": "#D08770",
        "error": "#BF616A",
        "card": "#E5E9F0",
        "highlight": "#5E81AC"
    }
}

theme_state = {"dark_mode": True}
selected_case = None

def get_test_cases():
    TEST_CASES_DIR = "test_cases"
    if not os.path.exists(TEST_CASES_DIR):
        os.makedirs(TEST_CASES_DIR)
    return [os.path.join(TEST_CASES_DIR, f) for f in os.listdir(TEST_CASES_DIR) if f.endswith(".json")]

def run_gui():
    global test_case_var, status_var, status_label, preview_text, root, theme_button

    colors = THEMES["dark"]

    def apply_theme():
        nonlocal colors
        mode = "dark" if theme_state["dark_mode"] else "light"
        colors = THEMES[mode]
        root.configure(bg=colors["background"])
        header.configure(bg=colors["primary"])
        status_frame.configure(bg=colors["primary"])
        status_label.configure(bg=colors["text"])
        selection_card.configure(bg=colors["card"])
        btn_frame.configure(bg=colors["card"])
        preview_card.configure(bg=colors["card"])
        theme_button.configure(bg=colors["secondary"], fg=colors["text"])
        test_case_menu.configure(background=colors["secondary"])
        preview_text.configure(
            bg=colors["background"], fg=colors["text"],
            insertbackground=colors["text"],
            selectbackground=colors["highlight"]
        )
        root.update()

    def toggle_theme():
        theme_state["dark_mode"] = not theme_state["dark_mode"]
        apply_theme()

    def load_case():
        global selected_case
        selected_case = test_case_var.get()
        if selected_case:
            try:
                with open(selected_case) as f:
                    data = json.load(f)
                    status_var.set(f"✔ Loaded: {os.path.basename(selected_case)}")
                    status_label.config(fg=colors["success"])
                    
                    preview_text.config(state=tk.NORMAL)
                    preview_text.delete(1.0, tk.END)
                    preview_text.insert(tk.END, json.dumps(data, indent=2))
                    preview_text.config(state=tk.DISABLED)
            except Exception as e:
                status_var.set(f"✖ Error loading file")
                status_label.config(fg=colors["error"])
        else:
            status_var.set("⚠️ Please select a test case")
            status_label.config(fg=colors["warning"])

    def run_in_pygame():
        if not selected_case:
            messagebox.showwarning("No Case Selected", "Please load a test case first.",
                                   icon="warning", parent=root)
            return
        status_var.set("🚀 Launching Pygame Simulation...")
        status_label.config(fg=colors["accent"])
        root.update()
        try:
            subprocess.Popen(["python", "main.py", selected_case])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch:\n{e}", parent=root)
            status_var.set("❌ Launch failed")
            status_label.config(fg=colors["error"])

    root = tk.Tk()
    root.title("🌟 Deadlock Simulator Pro")
    root.geometry("800x550")
    root.configure(bg=colors["background"])

    title_font = Font(family="Helvetica", size=14, weight="bold")
    button_font = Font(family="Helvetica", size=10, weight="bold")

    header = tk.Frame(root, bg=colors["primary"], height=60)
    header.pack(fill=tk.X)
    tk.Label(header, text="🧠 DEADLOCK SIMULATOR", font=title_font,
             bg=colors["primary"], fg=colors["text"]).pack(pady=15)

    theme_button = tk.Button(header, text="🌓 Toggle Theme", command=toggle_theme,
                             bg=colors["secondary"], fg=colors["text"],
                             font=("Helvetica", 9), relief=tk.FLAT)
    theme_button.place(x=640, y=20)

    content = tk.Frame(root, bg=colors["background"], padx=20, pady=20)
    content.pack(fill=tk.BOTH, expand=True)

    selection_card = tk.Frame(content, bg=colors["card"],
                              padx=15, pady=15, relief=tk.RAISED, bd=2)
    selection_card.pack(fill=tk.X, pady=(0, 20))

    tk.Label(selection_card, text="📁 SELECT TEST CASE",
             bg=colors["card"], fg=colors["highlight"],
             font=("Helvetica", 10, "bold")).pack(anchor="w")

    test_case_var = tk.StringVar()
    test_case_menu = ttk.Combobox(
        selection_card,
        textvariable=test_case_var,
        values=get_test_cases(),
        state="readonly",
        font=("Helvetica", 10)
    )
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox',
                    fieldbackground=colors["card"],
                    background=colors["secondary"],
                    foreground=colors["text"])
    test_case_menu.pack(fill=tk.X, pady=10)

    btn_frame = tk.Frame(selection_card, bg=colors["card"])
    btn_frame.pack(fill=tk.X)

    load_btn = tk.Button(btn_frame, text="📂 LOAD CASE", command=load_case,
                         width=15, bg=colors["secondary"], fg=colors["text"],
                         activebackground=colors["highlight"],
                         activeforeground=colors["text"],
                         font=button_font, relief=tk.RAISED, bd=3)
    load_btn.pack(side=tk.LEFT, padx=5)

    pygame_btn = tk.Button(btn_frame, text="🎮 RUN SIMULATION", command=run_in_pygame,
                           width=15, bg=colors["accent"], fg=colors["text"],
                           activebackground=colors["highlight"],
                           activeforeground=colors["text"],
                           font=button_font, relief=tk.RAISED, bd=3)
    pygame_btn.pack(side=tk.LEFT, padx=5)

    preview_card = tk.Frame(content, bg=colors["card"],
                            padx=15, pady=15, relief=tk.RAISED, bd=2)
    preview_card.pack(fill=tk.BOTH, expand=True)

    tk.Label(preview_card, text="📝 TEST CASE PREVIEW",
             bg=colors["card"], fg=colors["highlight"],
             font=("Helvetica", 10, "bold")).pack(anchor="w")

    preview_text = tk.Text(preview_card, bg=colors["background"], fg=colors["text"],
                           insertbackground=colors["text"],
                           selectbackground=colors["accent"],
                           wrap=tk.WORD, font=("Consolas", 10),
                           padx=10, pady=10, height=10)
    preview_text.pack(fill=tk.BOTH, expand=True)
    preview_text.insert(tk.END, "No test case loaded...")
    preview_text.config(state=tk.DISABLED)

    status_frame = tk.Frame(root, bg=colors["primary"], height=30)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)

    status_var = tk.StringVar(value="🟢 Ready to simulate")
    status_label = tk.Label(status_frame, textvariable=status_var,
                            bg=colors["primary"], fg=colors["text"],
                            font=("Helvetica", 9))
    status_label.pack(side=tk.LEFT, padx=10)

    apply_theme()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
