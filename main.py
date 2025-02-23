import tkinter as tk
from charCard import CharacterCardEditor

if __name__ == "__main__":
    root = tk.Tk()
    root.title("角色卡编辑器")
    root.geometry("800x600")
    app = CharacterCardEditor(root)
    root.mainloop()