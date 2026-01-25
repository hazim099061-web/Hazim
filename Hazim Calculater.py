import tkinter as tk
from tkinter import ttk
import math

FONT_BIG = ('Segoe UI', 24)
FONT_MED = ('Segoe UI', 14)
ACCENT = '#4CAF50'
OP_BG = '#2b2b3a'
NUM_BG = '#323248'
BTN_FG = '#ffffff'


def create_calculator():
    root = tk.Tk()
    root.title("آلة حاسبة Hazim — محسنة")
    root.configure(bg='#1e1e2f')
    root.resizable(False, False)

    # شاشة العرض (استخدم StringVar لسهولة التحديث)
    display_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=display_var, font=FONT_BIG, bd=0, bg='#0f1724', fg='white', justify='right', insertbackground='white')
    entry.grid(row=0, column=0, columnspan=4, padx=12, pady=(12,6), sticky='we')

    # سطر لعرض الإجابة السابقة
    last_var = tk.StringVar(value='')
    last_label = tk.Label(root, textvariable=last_var, anchor='e', bg='#1e1e2f', fg='#9aa0b4', font=FONT_MED)
    last_label.grid(row=1, column=0, columnspan=4, padx=12, sticky='we')

    # إعداد أزرار منظمة في مصفوفة لتخطيط جميل
    button_layout = [
        ['C', '←', '%', '/'],
        ['7', '8', '9', '*'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['±', '0', '.', '^'],
        ['(', ')', '√', '=']
    ]

    # تحضير أسماء دوال الرياضيات المسموح بها في eval
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}
    allowed_names.update({'abs': abs})

    def insert(text):
        cur = display_var.get()
        if cur == 'Error':
            display_var.set('')
            cur = ''
        display_var.set(cur + text)

    def clear():
        display_var.set('')

    def backspace():
        s = display_var.get()
        display_var.set(s[:-1])

    def plus_minus():
        s = display_var.get()
        if not s:
            return
        # Toggle sign for the whole expression (simple behavior)
        if s.startswith('-'):
            display_var.set(s[1:])
        else:
            display_var.set('-' + s)

    def preprocess(expr: str) -> str:
        expr = expr.replace('^', '**')
        expr = expr.replace('√', 'sqrt')
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        expr = expr.replace('%', '/100')
        return expr

    def calculate(event=None):
        expr = display_var.get()
        try:
            expr = preprocess(expr)
            result = eval(expr, {"__builtins__": None}, allowed_names)
            display_var.set(str(result))
            last_var.set('Ans: ' + str(result))
        except ZeroDivisionError:
            display_var.set('Error')
        except Exception:
            display_var.set('Error')

    # دوال ربط نص الأزرار بسلوكها
    def on_button(text):
        if text == 'C':
            clear()
        elif text == '←':
            backspace()
        elif text == '±':
            plus_minus()
        elif text == '=':
            calculate()
        elif text == '√':
            insert('sqrt(')
        else:
            insert(text)

    # إنشاء أزرار مع ستايل بسيط
    buttons_frame = tk.Frame(root, bg='#1e1e2f')
    buttons_frame.grid(row=2, column=0, columnspan=4, padx=12, pady=(6,12))

    for r, row in enumerate(button_layout):
        for c, key in enumerate(row):
            bg = OP_BG if key in ['/', '*', '-', '+', '=', '^', '%'] else NUM_BG
            fg = BTN_FG if key not in ['C'] else '#fff'
            width = 6
            btn = tk.Button(buttons_frame, text=key, width=width, height=2, font=FONT_MED,
                            bg=bg, fg=fg, bd=0, activebackground='#555', command=lambda k=key: on_button(k))
            if key == '=':
                btn.configure(bg=ACCENT, fg='white', font=('Segoe UI', 16, 'bold'))
            if key == 'C':
                btn.configure(bg='#b00020')
            btn.grid(row=r, column=c, padx=6, pady=6)

    # اختصارات لوحة المفاتيح
    def key_handler(event):
        char = event.char
        if char in '0123456789.+-*/()%':
            insert(char)
        elif event.keysym == 'Return':
            calculate()
        elif event.keysym == 'BackSpace':
            backspace()
        elif event.keysym == 'Escape':
            clear()

    root.bind('<Key>', key_handler)

    # اجعل النافذة مناسبة للمحتوى
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)

    entry.focus_set()

    return root


if __name__ == '__main__':
    app = create_calculator()
    app.mainloop()
