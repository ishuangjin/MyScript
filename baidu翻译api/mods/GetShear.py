#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2023-02-15 09:44:22
@LastEditTime: 2023-02-15 09:49:30
@FilePath: \\Github\\MyScript\\baidu翻译api\\mods\\GetShear.py
@Copyright (c) 2023 by ${git_name}, All Rights Reserved.
@Description:
'''
# 基于pyperclip模块实现

# pyperclip模块安装：
# 使用pip安装：pip install pyperclip
# 使用conda安装：conda install -c conda-forge pyperclip

# 依赖库：
import pyperclip
import tkinter as tk
import tkinter.messagebox as msgbox
# import googletrans  # googletrans模块安装：pip install googletrans

# 创建一个窗口
win = tk.Tk()
win.title('读取剪切板内容进行翻译')
win.geometry('400x300')
# 创建一个文本框，显示剪切板中的内容
text_clipboard = tk.Text(win, width=30, height=5)
text_clipboard.pack()
# 创建一个文本框，显示翻译的内容
text_translate = tk.Text(win, width=30, height=5)
text_translate.pack()
# 创建一个按钮，按下获取剪切板内容
btn_read = tk.Button(win, text='读取剪切板', width=15, height=2, command=lambda: read_clipboard())
btn_read.pack()
# 创建一个按钮，按下进行翻译
btn_translate = tk.Button(win, text='翻译', width=15, height=2, command=lambda: translate())
btn_translate.pack()
# 创建一个按钮，按下将翻译结果存入剪切板
btn_save = tk.Button(win, text='保存翻译结果', width=15, height=2, command=lambda: save_translate())
btn_save.pack()
# 将翻译结果保存到变量中
translate_result = ''


# 获取剪切板中的内容
def read_clipboard():
    text_clipboard.delete(1.0, tk.END)  # 清空文本框
    text_clipboard.insert(tk.END, pyperclip.paste())  # 将剪切板中的内容插入文本框
