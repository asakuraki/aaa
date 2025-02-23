import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import pyperclip
import about
import os

class CharacterCardEditor:
    def __init__(self, root):
        self.root = root
        self.data = {}
        self.appearance_entries = {}  # 外貌输入框字典
        self.attire_entries = {}      # 服装输入框字典
        
        self.setup_ui()
        
    def setup_ui(self):
        # 滚动区域
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 绑定鼠标滚轮事件
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 基础信息
        base_frame = ttk.LabelFrame(scrollable_frame, text="基础信息")
        base_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(base_frame, text="中文名：").grid(row=0, column=0, sticky="w")
        self.chinese_name_entry = ttk.Entry(base_frame)
        self.chinese_name_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(base_frame, text="日文名：").grid(row=0, column=2, sticky="w")
        self.japanese_name_entry = ttk.Entry(base_frame)
        self.japanese_name_entry.grid(row=0, column=3, sticky="ew")

        ttk.Label(base_frame, text="性别：").grid(row=1, column=0, sticky="w")
        self.gender_combobox = ttk.Combobox(base_frame, values=["female", "male", "other"])
        self.gender_combobox.grid(row=1, column=1, sticky="ew")

        ttk.Label(base_frame, text="年龄：").grid(row=1, column=2, sticky="w")
        self.age_spinbox = ttk.Spinbox(base_frame, from_=0, to=100)
        self.age_spinbox.grid(row=1, column=3, sticky="ew")

        ttk.Label(base_frame, text="身份：").grid(row=2, column=0, sticky="w")
        self.identity_entry = ttk.Entry(base_frame)
        self.identity_entry.grid(row=2, column=1, columnspan=3, sticky="ew")

        # 背景故事
        bg_frame = ttk.LabelFrame(scrollable_frame, text="背景故事（每行一条）")
        bg_frame.pack(padx=10, pady=5, fill="x")
        self.bg_text = tk.Text(bg_frame, height=4)
        self.bg_text.pack(fill="x")

        # 外貌特征
        appearance_frame = ttk.LabelFrame(scrollable_frame, text="外貌特征")
        appearance_frame.pack(padx=10, pady=5, fill="x")

        entries = [
            ("身高", "height"), ("发色", "hair_color"), ("发型", "hairstyle"),
            ("眼睛", "eyes"), ("鼻子", "nose"), ("嘴唇", "lips"),
            ("皮肤", "skin"), ("身材", "body")
        ]

        for i, (label, key) in enumerate(entries):
            ttk.Label(appearance_frame, text=label+": ").grid(row=i//4, column=(i%4)*2, sticky="w")
            entry = ttk.Entry(appearance_frame)
            entry.grid(row=i//4, column=(i%4)*2+1, sticky="ew")
            self.appearance_entries[key] = entry

        # 服装信息
        attire_frame = ttk.LabelFrame(scrollable_frame, text="服装设定")
        attire_frame.pack(padx=10, pady=5, fill="x")

        attire_items = [
            ("上衣", "tops"), ("下装", "bottoms"), ("鞋子", "shoes"),
            ("袜子", "socks"), ("内衣", "underwears"), ("配饰", "accessories")
        ]

        for i, (label, key) in enumerate(attire_items):
            ttk.Label(attire_frame, text=label+": ").grid(row=i//3, column=(i%3)*2, sticky="w")
            entry = ttk.Entry(attire_frame)
            entry.grid(row=i//3, column=(i%3)*2+1, sticky="ew")
            self.attire_entries[key] = entry

        # MBTI性格
        mbti_frame = ttk.LabelFrame(scrollable_frame, text="MBTI性格")
        mbti_frame.pack(padx=10, pady=5, fill="x")
        self.mbti_combobox = ttk.Combobox(mbti_frame, values=["INFP", "INTJ", "ENFJ", "ISTP", "其他类型"])
        self.mbti_combobox.pack()

        # 性格特质
        self.traits_frame = ttk.LabelFrame(scrollable_frame, text="性格特质（点击添加）")
        self.traits_frame.pack(padx=10, pady=5, fill="x")
        ttk.Button(self.traits_frame, text="+ 添加特质", command=self.add_trait).pack()

        # 人际关系
        self.relationship_frame = ttk.LabelFrame(scrollable_frame, text="人际关系（点击添加）")
        self.relationship_frame.pack(padx=10, pady=5, fill="x")
        ttk.Button(self.relationship_frame, text="+ 添加关系", command=self.add_relationship).pack()

        # 喜好系统
        likes_frame = ttk.LabelFrame(scrollable_frame, text="喜好（每行一条）")
        likes_frame.pack(padx=10, pady=5, fill="x")
        self.likes_text = tk.Text(likes_frame, height=3)
        self.likes_text.pack(fill="x")

        dislikes_frame = ttk.LabelFrame(scrollable_frame, text="厌恶（每行一条）")
        dislikes_frame.pack(padx=10, pady=5, fill="x")
        self.dislikes_text = tk.Text(dislikes_frame, height=3)
        self.dislikes_text.pack(fill="x")

        # 日常作息
        routine_frame = ttk.LabelFrame(scrollable_frame, text="日常作息")
        routine_frame.pack(padx=10, pady=5, fill="x")

        routine_labels = ["清晨", "上午", "下午", "傍晚", "夜间", "深夜"]
        self.routine_entries = []

        for i, label in enumerate(routine_labels):
            ttk.Label(routine_frame, text=label+": ").grid(row=0, column=i*2, sticky="w")
            entry = ttk.Entry(routine_frame)
            entry.grid(row=0, column=i*2+1, sticky="ew", padx=2)
            self.routine_entries.append(entry)

        (self.routine_am_entry, self.routine_morning_entry, self.routine_afternoon_entry, 
         self.routine_evening_entry, self.routine_night_entry, self.routine_late_entry) = self.routine_entries

    # def setup_menubar(self):
    #     """创建菜单栏"""
    #     menubar = tk.Menu(self.root)
    #     self.root.config(menu=menubar)

    #     # 文件菜单
    #     file_menu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="文件", menu=file_menu)
    #     file_menu.add_command(label="加载角色卡", command=self.load_character_card)
    #     file_menu.add_command(label="生成角色卡", command=self.create_character_card)

    #     # 帮助菜单
    #     help_menu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="帮助", menu=help_menu)
    #     help_menu.add_command(label="关于", command=about.show_about)

    def clear_dynamic_frames(self):
        """清空动态添加的组件"""
        for widget in self.traits_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        for widget in self.relationship_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()

    def load_character_card(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("JSON文件", "*.json")])
            if not filepath:
                return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                
            self.clear_dynamic_frames()
            self.root.update_idletasks()  # 确保界面刷新
            self.populate_data(self.data)
            messagebox.showinfo("成功", "角色卡加载完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载失败：{str(e)}")

    def populate_data(self, data):
        """填充数据到界面"""
        # 基础信息
        self.chinese_name_entry.delete(0, tk.END)
        self.chinese_name_entry.insert(0, data.get("Chinese_name", ""))
        self.japanese_name_entry.delete(0, tk.END)
        self.japanese_name_entry.insert(0, data.get("Japanese_name", ""))
        self.gender_combobox.set(data.get("gender", ""))
        self.age_spinbox.delete(0, tk.END)
        self.age_spinbox.insert(0, data.get("age", ""))
        self.identity_entry.delete(0, tk.END)
        self.identity_entry.insert(0, data.get("identity", ""))
        
        # 背景故事
        self.bg_text.delete("1.0", tk.END)
        self.bg_text.insert("1.0", "\n".join(data.get("background", [])))
        
        # 外貌信息
        if "appearance" in data:
            for key in self.appearance_entries:
                if key in data["appearance"]:
                    self.appearance_entries[key].delete(0, tk.END)
                    self.appearance_entries[key].insert(0, data["appearance"][key])
        
        # 服装信息
        if "attire" in data:
            attire_data = data["attire"].get("服装", {})
            for key in self.attire_entries:
                if key in attire_data:
                    self.attire_entries[key].delete(0, tk.END)
                    self.attire_entries[key].insert(0, attire_data[key])
        
        # MBTI
        self.mbti_combobox.set(data.get("MBTI_personality", ""))
        
        # 性格特质
        if "personal_traits" in data:
            for trait, details in data["personal_traits"].items():
                self.add_trait()
                dynamic_frames = [w for w in self.traits_frame.winfo_children() if isinstance(w, ttk.Frame)]
                last_trait = dynamic_frames[-1] if dynamic_frames else None
                
                if last_trait:
                    entry = [child for child in last_trait.winfo_children() if isinstance(child, ttk.Entry)][0]
                    texts = [child for child in last_trait.winfo_children() if isinstance(child, tk.Text)]
                    
                    entry.insert(0, trait)
                    texts[0].insert("1.0", details.get("description", ""))
                    texts[1].insert("1.0", "\n".join(details.get("dialogue_examples", [])))
                    texts[2].insert("1.0", "\n".join(details.get("behavior_examples", [])))

        # 人际关系
        if "relationship" in data:
            for name, desc_list in data["relationship"].items():
                self.add_relationship()
                dynamic_frames = [w for w in self.relationship_frame.winfo_children() if isinstance(w, ttk.Frame)]
                last_rel = dynamic_frames[-1] if dynamic_frames else None
                
                if last_rel:
                    entry = [child for child in last_rel.winfo_children() if isinstance(child, ttk.Entry)][0]
                    texts = [child for child in last_rel.winfo_children() if isinstance(child, tk.Text)]
                    entry.insert(0, name)
                    texts[0].insert("1.0", "\n".join(desc_list))
        
        # 喜好系统
        self.likes_text.delete("1.0", tk.END)
        self.likes_text.insert("1.0", "\n".join(data.get("likes", [])))
        self.dislikes_text.delete("1.0", tk.END)
        self.dislikes_text.insert("1.0", "\n".join(data.get("dislikes", [])))
        
        # 日常作息
        routine = data.get("daily_routine", {})
        self.routine_am_entry.delete(0, tk.END)
        self.routine_am_entry.insert(0, routine.get("early_morning", ""))
        self.routine_morning_entry.delete(0, tk.END)
        self.routine_morning_entry.insert(0, routine.get("morning", ""))
        self.routine_afternoon_entry.delete(0, tk.END)
        self.routine_afternoon_entry.insert(0, routine.get("afternoon", ""))
        self.routine_evening_entry.delete(0, tk.END)
        self.routine_evening_entry.insert(0, routine.get("evening", ""))
        self.routine_night_entry.delete(0, tk.END)
        self.routine_night_entry.insert(0, routine.get("night", ""))
        self.routine_late_entry.delete(0, tk.END)
        self.routine_late_entry.insert(0, routine.get("late_night", ""))

    def collect_data(self):
        """收集所有界面数据"""
        return {
            "Chinese_name": self.chinese_name_entry.get(),
            "Japanese_name": self.japanese_name_entry.get(),
            "gender": self.gender_combobox.get(),
            "age": self.age_spinbox.get(),
            "background": [line.strip() for line in self.bg_text.get("1.0", tk.END).split('\n') if line.strip()],
            "identity": self.identity_entry.get(),
            "appearance": {key: entry.get() for key, entry in self.appearance_entries.items()},
            "attire": {"服装": {key: entry.get() for key, entry in self.attire_entries.items()}},
            "MBTI_personality": self.mbti_combobox.get(),
            "personal_traits": self.collect_traits(),
            "relationship": self.collect_relationships(),
            "likes": [line.strip() for line in self.likes_text.get("1.0", tk.END).split('\n') if line.strip()],
            "dislikes": [line.strip() for line in self.dislikes_text.get("1.0", tk.END).split('\n') if line.strip()],
            "daily_routine": {
                "early_morning": self.routine_am_entry.get(),
                "morning": self.routine_morning_entry.get(),
                "afternoon": self.routine_afternoon_entry.get(),
                "evening": self.routine_evening_entry.get(),
                "night": self.routine_night_entry.get(),
                "late_night": self.routine_late_entry.get()
            }
        }

    def create_character_card(self):
        """生成角色卡"""
        try:
            data = self.collect_data()
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json")]
            )
            if not filepath:
                return
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", "角色卡保存成功！")
            pyperclip.copy(json.dumps(data, ensure_ascii=False, indent=2))
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")

    def collect_traits(self):
        """收集性格特质数据"""
        traits = {}
        for trait in self.traits_frame.winfo_children():
            if isinstance(trait, ttk.Frame):
                entries = [child for child in trait.winfo_children() if isinstance(child, ttk.Entry)]
                texts = [child for child in trait.winfo_children() if isinstance(child, tk.Text)]
                
                if entries and entries[0].get():
                    name = entries[0].get()
                    traits[name] = {
                        "description": texts[0].get("1.0", tk.END).strip(),
                        "dialogue_examples": [line.strip() for line in texts[1].get("1.0", tk.END).split('\n') if line.strip()],
                        "behavior_examples": [line.strip() for line in texts[2].get("1.0", tk.END).split('\n') if line.strip()]
                    }
        return traits

    def collect_relationships(self):
        """收集人际关系数据"""
        relationships = {}
        for rel in self.relationship_frame.winfo_children():
            if isinstance(rel, ttk.Frame):
                entries = [child for child in rel.winfo_children() if isinstance(child, ttk.Entry)]
                texts = [child for child in rel.winfo_children() if isinstance(child, tk.Text)]
                
                if entries and entries[0].get():
                    name = entries[0].get()
                    relationships[name] = {
                        "description": [line.strip() for line in texts[0].get("1.0", tk.END).split('\n') if line.strip()],
                        "features": [line.strip() for line in texts[1].get("1.0", tk.END).split('\n') if line.strip()]
                    }
        return relationships

    def add_trait(self):
        """添加性格特质组件"""
        trait_frame = ttk.Frame(self.traits_frame)
        trait_frame.pack(fill="x", pady=2)
        
        ttk.Label(trait_frame, text="特质名称：").pack(side="left")
        name_entry = ttk.Entry(trait_frame, width=15)
        name_entry.pack(side="left")
        
        ttk.Label(trait_frame, text="描述：").pack(side="left", padx=5)
        desc_entry = tk.Text(trait_frame, height=2, width=20)
        desc_entry.pack(side="left")
        
        ttk.Label(trait_frame, text="对话示例：").pack(side="left", padx=5)
        dialogue_entry = tk.Text(trait_frame, height=2, width=20)
        dialogue_entry.pack(side="left")
        
        ttk.Label(trait_frame, text="行为示例：").pack(side="left", padx=5)
        behavior_entry = tk.Text(trait_frame, height=2, width=20)
        behavior_entry.pack(side="left")

    def add_relationship(self):
        """添加人际关系组件"""
        rel_frame = ttk.Frame(self.relationship_frame)
        rel_frame.pack(fill="x", pady=2)
        
        ttk.Label(rel_frame, text="角色名称：").pack(side="left")
        name_entry = ttk.Entry(rel_frame, width=20)
        name_entry.pack(side="left")
        
        ttk.Label(rel_frame, text="关系描述：").pack(side="left", padx=5)
        desc_entry = tk.Text(rel_frame, height=3, width=40)
        desc_entry.pack(side="left")
        
        # 添加人物特征输入框
        ttk.Label(rel_frame, text="人物特征：").pack(side="left", padx=5)
        feature_entry = tk.Text(rel_frame, height=3, width=40)
        feature_entry.pack(side="left")
