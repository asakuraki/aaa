import tkinter as tk
import about
from charCard import CharacterCardEditor
from worldInfoForspace import WorldEditor

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("角色与世界编辑器")
        self.root.geometry("1220x600")

        # 角色卡编辑器
        self.character_editor = CharacterCardEditor(self.root)
        # 世界书编辑器
        self.world_editor = WorldEditor(self.root)

        # 初始显示角色卡编辑器
        self.character_editor.pack(fill="both", expand=True)

        # 创建菜单栏
        self.setup_menubar()

    def setup_menubar(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="加载角色卡", command=self.character_editor.load_character_card)
        file_menu.add_command(label="保存角色卡", command=self.character_editor.create_character_card)
        file_menu.add_separator()
        file_menu.add_command(label="加载世界书", command=self.world_editor.load_world)
        file_menu.add_command(label="保存世界书", command=self.world_editor.save_world)

        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="角色卡编辑器", command=lambda: self.show_page("character"))
        view_menu.add_command(label="世界书", command=lambda: self.show_page("world"))

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=about.show_about)

    def show_page(self, page):
        """切换界面"""
        self.character_editor.pack_forget()
        self.world_editor.pack_forget()

        if page == "character":
            self.character_editor.pack(fill="both", expand=True)
        elif page == "world":
            self.world_editor.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
