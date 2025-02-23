import tkinter as tk
import about
from charCard import CharacterCardEditor

def setup_menubar(root, app):
    """创建菜单栏"""
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # 文件菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="加载角色卡", command=app.load_character_card)
    file_menu.add_command(label="生成角色卡", command=app.create_character_card)

    # 帮助菜单
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="帮助", menu=help_menu)
    help_menu.add_command(label="关于", command=about.show_about)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("角色卡编辑器")
    root.geometry("1220x600")
    app = CharacterCardEditor(root)
    setup_menubar(root, app)
    root.mainloop()
