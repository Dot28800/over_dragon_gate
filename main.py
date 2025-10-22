import glob
import os
import sys
import tkinter as tk
from tkinter import messagebox, PhotoImage, ttk
import pygame
from PIL import Image, ImageTk
from fence import Fence
from jumping import Jumping

class GameSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏选择界面")
        self.root.geometry("1300x850+0+0")
        self.selected_background = None
        self.selected_character = None
        self.title_font = ("Helvetica", 15)
        self.item_font = ("Helvetica", 12)
        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # 配置 Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 将可滚动区域绑定到 Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>",self._on_mousewheel)
        # 创建背景主题选择区域
        self.background_frame = tk.Frame(self.scrollable_frame)
        self.background_frame.pack(pady=10)
        self.fence_path="resources/prob_image/wb_fence.png"
        self.needle_path="resources/prob_image/needles.png"
        self.clock_path="resources/prob_image/clock.png"
        self.shield_path="resources/prob_image/shield.jpg"
        self.wing_path="resources/prob_image/wing.png"
        self.arrow_path="resources/prob_image/arrow.png"
        tk.Label(self.background_frame, text="请选择背景主题",font=self.title_font).grid(row=0, column=1, columnspan=3, pady=5)

        # 调整图像大小
        background_size = (150, 120)  # 设置背景图像的大小
        # 背景图片所在路径
        bg_dir = "resources/background_image"

        # 读取路径下所有 .jpg 文件（按文件名排序，确保顺序一致）
        self.background_images = [
            ImageTk.PhotoImage(
                Image.open(os.path.join(bg_dir, filename)).resize(background_size, Image.Resampling.LANCZOS)
            )
            for filename in sorted(os.listdir(bg_dir))  # sorted 确保每次加载顺序一致
            if filename.lower().endswith(".jpg")  # 只处理 jpg 格式图片
        ]
        jpg_files = [f for f in sorted(os.listdir(bg_dir)) if f.lower().endswith(".jpg")]
        self.background_names = [os.path.splitext(f)[0] for f in jpg_files]
        background_dir = "resources/background_image/"
        self.background_paths = [os.path.join(background_dir, f"{name}.jpg") for name in self.background_names]
        self.background_buttons = []
        for i, img in enumerate(self.background_images):
            button = tk.Button(self.background_frame, image=img, command=lambda i=i: self.select_background(i),
                               highlightbackground="blue", highlightcolor="blue", highlightthickness=0, bd=5)
            button.image = img  # 保持对图像的引用
            button.grid(row=1, column=i, padx=25, pady=5)
            self.background_buttons.append(button)
            name_label = tk.Label(self.background_frame, text=self.background_names[i],font=self.item_font)
            name_label.grid(row=2, column=i, padx=25, pady=0)
        self.character_frame = tk.Frame(self.scrollable_frame)
        self.character_frame.pack(pady=10)
        tk.Label(self.character_frame, text="请选择角色",font=self.title_font).grid(row=0, column=2, columnspan=2, padx=150,pady=5)
        # 调整图像大小
        character_size = (150, 150)  # 设置角色图像的大小
        # 角色图片所在路径
        char_dir = "resources/player_image/"

        # 筛选出所有图片文件（支持png等格式，按文件名排序）
        # 这里假设图片格式为png，如需支持其他格式可扩展元组
        char_files = [
            f for f in sorted(os.listdir(char_dir))
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")) and not f.startswith("护盾") and not f.startswith("飞行")
        ]

        # 生成图片对象列表
        self.character_images = [
            ImageTk.PhotoImage(
                Image.open(os.path.join(char_dir, f)).resize(character_size, Image.Resampling.LANCZOS)
            ) for f in char_files
        ]

        # 生成名称列表（去除扩展名）
        self.character_names = [os.path.splitext(f)[0] for f in char_files if not f.startswith("护盾") and not f.startswith("飞行")]
        # 生成完整路径列表
        self.character_paths = [os.path.join(char_dir, f) for f in char_files]
        self.character_sizes=[(96,120),(96,120),(96,120),(110,145),(112,153),(105,130)]
        self.character_map={self.character_names[i]:self.character_sizes[i] for i in range(len(self.character_names))}
        self.character_buttons = []
        for i, img in enumerate(self.character_images):
            button = tk.Button(self.character_frame, image=img, command=lambda i=i: self.select_character(i),
                               highlightbackground="white", highlightcolor="white", highlightthickness=0, bd=5)
            button.image = img  # 保持对图像的引用
            button.grid(row=1, column=i, padx=25, pady=5)
            self.character_buttons.append(button)
            name_label = tk.Label(self.character_frame, text=self.character_names[i],font=self.item_font)
            name_label.grid(row=2, column=i, padx=25, pady=0)
        # 创建规则介绍区域
        self.rule_frame = tk.Frame(self.scrollable_frame)
        self.rule_frame.pack(pady=10)
        rule_img_size=(120,120)
        self.prob_names=["栅栏:阻碍前进","倒针：碰到扣分","时钟：增加时间","护盾：无敌状态","翅膀：飞行充能","流矢：贯穿伤害"]
        self.prob_images=[
            ImageTk.PhotoImage(Image.open("resources/prob_image/wb_fence.png").resize(rule_img_size, Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(Image.open("resources/prob_image/needles.png").resize(rule_img_size, Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(Image.open("resources/prob_image/clock.png").resize(rule_img_size, Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(Image.open("resources/prob_image/shield.jpg").resize(rule_img_size, Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(Image.open("resources/prob_image/wing.png").resize(rule_img_size, Image.Resampling.LANCZOS)),
            ImageTk.PhotoImage(Image.open("resources/prob_image/arrow.png").resize(rule_img_size, Image.Resampling.LANCZOS))
        ]
        tk.Label(self.rule_frame, text="规则介绍",font=self.title_font).grid(row=0, column=2, columnspan=2, pady=5)
        for i, img in enumerate(self.prob_images):
            label = tk.Label(self.rule_frame, image=img, bd=5, relief="raised", cursor="hand2")
            label.image = img  # 保持对图像的引用
            label.grid(row=1, column=i, padx=25, pady=5)
            name_label = tk.Label(self.rule_frame, text=self.prob_names[i],font=self.item_font)
            name_label.grid(row=2, column=i, padx=25, pady=0)
        center_text = tk.Label(self.rule_frame, text="普通状态：k:跳跃 s:下蹲 a:后退 d:前进\n飞行状态:w:上浮 s:下沉 a:后退 d:前进\n在有限的时间内尽可能躲避障碍物，获得更高分吧", font=("Helvetica", 14))
        center_text.grid(row=3, column=1, columnspan=4, pady=10)
        start_button = tk.Button(self.rule_frame, text="开始游戏", command=self.start_game)
        start_button.grid(row=4, column=2, columnspan=2, padx=150,pady=10)


    def rule_introduction(self):
        messagebox.showinfo("规则介绍", "在规定时间内，尽可能躲避道具，获得更多分数吧！")

    def select_background(self, index):
        if self.selected_background is not None:
            self.background_buttons[self.selected_background].config(highlightthickness=0)
        self.selected_background = index
        self.selected_background_path= self.background_paths[index]
        self.background_buttons[index].config(highlightbackground="yellow", highlightcolor="blue",
                                              highlightthickness=25)

    def select_character(self, index):
        if self.selected_character is not None:
            self.character_buttons[self.selected_character].config(highlightthickness=0)
        self.selected_character = index
        self.character_name= self.character_names[index]
        self.selected_character_path= self.character_paths[index]

        self.character_buttons[index].config(highlightbackground="yellow", highlightcolor="blue",
                                             highlightthickness=25)

    def _on_mousewheel(self, event):
            """鼠标滚轮事件回调函数"""
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def start_game(self):
        if self.selected_background is None or self.selected_character is None:
            messagebox.showerror("错误", "请先选择背景和角色。")
        else:
            bg_rgb=(255,255,255)
            if "空桑" in self.selected_character_path:
                bg_rgb=(184,68,193)
            game=Jumping(bg_path=self.selected_background_path,player_path=self.selected_character_path,
                         fence_path=self.fence_path,needle_path=self.needle_path,clock_path=self.clock_path,shield_path=self.shield_path,
                         wing_path=self.wing_path,arrow_path=self.arrow_path,bg_rgb=bg_rgb,
                         player_size_x=self.character_map[self.character_name][0],player_size_y=self.character_map[self.character_name][1])
            game.prepare()
            game.run()




if __name__ == "__main__":
    root = tk.Tk()
    app = GameSelector(root)
    root.mainloop()

