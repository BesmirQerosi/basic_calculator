import tkinter as tk
from tkinter import messagebox
import math
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Calculator Pro")
        root.configure(bg='#f0f0f0')
        
        self.first_number = None
        self.operation = ""
        self.reset_screen = False
        
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        
        self.top_var = tk.BooleanVar()
        self.top_var.set(False)
        self.options_menu.add_checkbutton(label="Always on Top", onvalue=True, offvalue=False, 
                                          variable=self.top_var, command=self.toggle_topmost)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Exit", command=root.quit)

        self.history_label = tk.Label(
            root, text="", anchor="e", bg="#f0f0f0", fg="gray", font=('Arial', 10)
        )
        self.history_label.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=15, pady=(5,0))

        self.display_entry = tk.Entry(
            root,       
            width=20,                 
            borderwidth=1,            
            relief="solid",           
            font=('Arial', 30, 'bold'),       
            justify='right',
            state='readonly',
            readonlybackground="white", 
            fg="#333333"
        )
        self.display_entry.grid(row=1, column=0, columnspan=4, padx=15, pady=10, sticky="nsew", ipady=10)

        self.create_widgets()
        
        root.grid_rowconfigure(0, weight=0) 
        root.grid_rowconfigure(1, weight=0) 
        for i in range(2, 8): 
            root.grid_rowconfigure(i, weight=1)
        for i in range(4): 
            root.grid_columnconfigure(i, weight=1)

        self.bind_keys()

        try:
            icon_path = resource_path('calc.ico')
            root.iconbitmap(icon_path)
        except Exception:
            pass

    def toggle_topmost(self):
        is_top = self.top_var.get()
        self.root.attributes('-topmost', is_top)

    def _update_display(self, text):
        self.display_entry.config(state='normal')
        self.display_entry.delete(0, tk.END)
        self.display_entry.insert(0, text)
        self.display_entry.config(state='readonly')
    
    def _update_history(self, text):
        self.history_label.config(text=text)

    def _get_display_value(self):
        return self.display_entry.get()

    def add_digit(self, digit):
        current = self._get_display_value()
        
        if self.reset_screen:
            current = ""
            self.display_entry.config(state='normal')
            self.display_entry.delete(0, tk.END)
            self.reset_screen = False

        if str(digit) == '.' and '.' in current:
            return
        
        if current == "0" and str(digit) != ".":
            self.display_entry.config(state='normal')
            self.display_entry.delete(0, tk.END)
            self.display_entry.insert(0, str(digit))
            self.display_entry.config(state='readonly')
        else:
            self.display_entry.config(state='normal')
            self.display_entry.insert(tk.END, str(digit))
            self.display_entry.config(state='readonly')

    def clear_all(self):
        self._update_display("0")
        self._update_history("")
        self.first_number = None
        self.operation = ""
        self.reset_screen = False

    def backspace(self):
        if self.reset_screen: return
        current = self._get_display_value()
        if len(current) > 0:
            new_val = current[:-1]
            if new_val == "": new_val = "0"
            self._update_display(new_val)

    def calculate_percentage(self):
        try:
            val_str = self._get_display_value()
            if not val_str: return
            
            current_num = float(val_str)
            
            if self.first_number is not None and self.operation:
                if self.operation in ['+', '-']:
                    result = self.first_number * (current_num / 100)
                else:
                    result = current_num / 100
            else:
                result = current_num / 100

            self._update_display(str(result))
            self.reset_screen = True
            
        except ValueError:
            self.clear_all()

    def calculate_unary(self, op_symbol):
        try:
            val_str = self._get_display_value()
            if not val_str: return 
            number = float(val_str)
            
            if op_symbol == '\u221A':
                if number < 0:
                    messagebox.showerror("Error", "Square root of negative number!")
                    return
                result = math.sqrt(number)
            
            if result.is_integer(): result = int(result)
            self._update_display(str(result))
            self.reset_screen = True
            self.first_number = None 
            self.operation = ""
            self._update_history(f"√({val_str})")
            
        except ValueError:
            self.clear_all()

    def set_operator(self, symbol):
        try:
            val_str = self._get_display_value()
            if not val_str: return

            if self.first_number is not None and self.operation and not self.reset_screen:
                self.calculate(continue_chain=True)

            self.first_number = float(self._get_display_value())
            self.operation = symbol
            self.reset_screen = True
            
            display_num = int(self.first_number) if self.first_number.is_integer() else self.first_number
            self._update_history(f"{display_num} {symbol}")

        except ValueError:
            self.clear_all()

    def toggle_sign(self):
        try:
            current = self._get_display_value()
            if current and current != "0": 
                number = float(current)
                result = -1 * number
                if result.is_integer(): result = int(result)
                self._update_display(str(result))
        except ValueError:
            pass

    def calculate(self, continue_chain=False):
        if not self.operation or self.first_number is None:
            return

        try:
            second_number = float(self._get_display_value())
            result = 0

            if self.operation == '+':
                result = self.first_number + second_number
            elif self.operation == '-':
                result = self.first_number - second_number
            elif self.operation == '*':
                result = self.first_number * second_number
            elif self.operation == '/':
                if second_number == 0:
                    self._update_display("Error")
                    self.first_number = None
                    self.operation = ""
                    self.reset_screen = True
                    self._update_history("")
                    return
                result = self.first_number / second_number
            elif self.operation == 'x\u02B8':
                result = self.first_number ** second_number

            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self._update_display(str(result))
            
            if not continue_chain:
                self._update_history("")
                self.first_number = None
                self.operation = ""
            else:
                self.first_number = result

            self.reset_screen = True

        except Exception:
            self._update_display("Error")

    def create_widgets(self):
        widgets = self.root.grid_slaves()
        for w in widgets:
            if int(w.grid_info()['row']) >= 2: w.destroy()

        self.create_button('C', 2, 0, '#FF6347', 'white', self.clear_all)
        self.create_button('←', 2, 1, '#FF6347', 'white', self.backspace)
        self.create_button('%', 2, 2, '#ADD8E6', 'black', self.calculate_percentage)
        self.create_button('/', 2, 3, '#FFA500', 'white', lambda: self.set_operator('/'))

        self.create_button('7', 3, 0, 'white', 'black', lambda: self.add_digit('7'))
        self.create_button('8', 3, 1, 'white', 'black', lambda: self.add_digit('8'))
        self.create_button('9', 3, 2, 'white', 'black', lambda: self.add_digit('9'))
        self.create_button('*', 3, 3, '#FFA500', 'white', lambda: self.set_operator('*'))

        self.create_button('4', 4, 0, 'white', 'black', lambda: self.add_digit('4'))
        self.create_button('5', 4, 1, 'white', 'black', lambda: self.add_digit('5'))
        self.create_button('6', 4, 2, 'white', 'black', lambda: self.add_digit('6'))
        self.create_button('-', 4, 3, '#FFA500', 'white', lambda: self.set_operator('-'))

        self.create_button('1', 5, 0, 'white', 'black', lambda: self.add_digit('1'))
        self.create_button('2', 5, 1, 'white', 'black', lambda: self.add_digit('2'))
        self.create_button('3', 5, 2, 'white', 'black', lambda: self.add_digit('3'))
        self.create_button('+', 5, 3, '#FFA500', 'white', lambda: self.set_operator('+'))

        self.create_button('±', 6, 0, '#ADD8E6', 'black', self.toggle_sign)
        self.create_button('0', 6, 1, 'white', 'black', lambda: self.add_digit('0'))
        self.create_button('.', 6, 2, '#ADD8E6', 'black', lambda: self.add_digit('.'))
        self.create_button('x\u02B8', 6, 3, '#ADD8E6', 'black', lambda: self.set_operator('x\u02B8'))

        self.create_button('\u221A', 7, 0, '#ADD8E6', 'black', lambda: self.calculate_unary('\u221A'))
        
        btn_equals = tk.Button(self.root, text='=', font=('Arial', 12, 'bold'),
                                command=self.calculate, bg='#90EE90', fg='black', bd=1, relief="raised")
        btn_equals.grid(row=7, column=1, columnspan=3, padx=2, pady=2, sticky="nsew")
        
        btn_equals.bind("<Enter>", lambda e: btn_equals.config(bg="#76c976"))
        btn_equals.bind("<Leave>", lambda e: btn_equals.config(bg="#90EE90"))

    def create_button(self, text, r, c, bg_color, fg_color, command):
        btn = tk.Button(
            self.root, text=text, font=('Arial', 12, 'bold'),
            command=command, bg=bg_color, fg=fg_color, bd=1, relief="raised"
        )
        btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        def on_enter(e):
            if bg_color == 'white':
                btn.config(bg='#e6e6e6')
            elif bg_color == '#FFA500':
                btn.config(bg='#cc8400')
            elif bg_color == '#FF6347':
                btn.config(bg='#cc4f38')
            elif bg_color == '#ADD8E6':
                btn.config(bg='#8abccf')
            elif bg_color == '#90EE90':
                btn.config(bg='#76c976')

        def on_leave(e):
            btn.config(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def bind_keys(self):
        self.root.bind('<Return>', lambda event: self.calculate())
        self.root.bind('<KP_Enter>', lambda event: self.calculate())
        self.root.bind('<Escape>', lambda event: self.clear_all())
        self.root.bind('<BackSpace>', lambda event: self.backspace())
        
        for i in range(10): 
            self.root.bind(str(i), lambda event, num=i: self.add_digit(num))
        
        self.root.bind('+', lambda event: self.set_operator('+'))
        self.root.bind('-', lambda event: self.set_operator('-'))
        self.root.bind('*', lambda event: self.set_operator('*'))
        self.root.bind('/', lambda event: self.set_operator('/'))
        self.root.bind('.', lambda event: self.add_digit('.'))
        self.root.bind('%', lambda event: self.calculate_percentage())

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(320, 500)
    app = CalculatorApp(root)
    root.mainloop()