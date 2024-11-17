import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#2b2b2b")
        
        # Display
        self.display_var = tk.StringVar()
        self.display = tk.Entry(root, 
                              textvariable=self.display_var,
                              font=('Arial', 24),
                              bg="#3b3b3b",
                              fg="white",
                              justify="right",
                              bd=0,
                              highlightthickness=1,
                              highlightbackground="#555")
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        #layout
        self.buttons = [
            [ 'e', 'mod', 'C', 'DEL', '÷'],
            ['log', 'sin', 'cos', 'tan', '×'],
            ['√', 'x²', '(', ')', '-'],
            ['7', '8', '9', 'π', '+'],
            ['4', '5', '6', '0'],
            ['1', '2', '3', '.', '=']
        ]
        
        for i, row in enumerate(self.buttons):
            for j, text in enumerate(row):
                if text == '=':
                    #eql button
                    btn = tk.Button(root,
                                  text=text,
                                  font=('Arial', 16, 'bold'),
                                  bg="#4CAF50",
                                  fg="white",
                                  activebackground="#45a049",
                                  activeforeground="white",
                                  bd=0,
                                  pady=5,
                                  command=lambda t=text: self.button_click(t))
                    btn.grid(row=i, column=j, rowspan=2, padx=1, pady=1, sticky="nsew")
                else:
                    #default button
                    btn = tk.Button(root,
                                  text=text,
                                  font=('Arial', 12),
                                  bg="#3b3b3b",
                                  fg="white",
                                  activebackground="#4b4b4b",
                                  activeforeground="white",
                                  bd=0,
                                  pady=5,
                                  command=lambda t=text: self.button_click(t))
                    btn.grid(row=i+1, column=j, padx=1, pady=1, sticky="nsew")
        
        for i in range(7):
            root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)
        
        self.current_expression = ""
        
    def handle_special_functions(self, expression):

        expression = expression.replace('π', str(math.pi))
        expression = expression.replace('e', str(math.e))
        
        parts = []
        current = ""
        operators = {'+', '-', '×', '÷', '(', ')', 'mod'}
        
        for char in expression:
            if char in operators and current:
                parts.append(current)
                parts.append(char)
                current = ""
            elif char in operators:
                parts.append(char)
            else:
                current += char
        if current:
            parts.append(current)

        for i in range(len(parts)):
            part = parts[i]
            try:
                # square
                if 'x²' in part:
                    num = part.replace('x²', '')
                    parts[i] = str(float(num) ** 2) if num else "**2"
                
                # trigonometric functions
                elif part.startswith(('sin', 'cos', 'tan')):
                    func = part[:3]
                    num = float(part[3:])
                    parts[i] = str(getattr(math, func)(math.radians(num)))
                
                # square root
                elif part.startswith('√'):
                    num = float(part[1:])
                    parts[i] = str(math.sqrt(num))
                
                # logarithm
                elif part.startswith('log'):
                    num = float(part[3:])
                    parts[i] = str(math.log10(num))
                
                # modulo
                elif part == 'mod':
                    parts[i] = '%'
                    
            except ValueError:
                pass

        return ''.join(parts)

    def evaluate_expression(self, expression):
        try:
            expression = expression.replace('×', '*').replace('÷', '/')
            
            # special functions and constants
            expression = self.handle_special_functions(expression)
            
            #main calculation
            result = eval(expression)
            
            #division by zero
            if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
                return "Cannot divide by zero"
            
            # Format the result
            if isinstance(result, float):
                result = f"{result:.10f}".rstrip('0').rstrip('.')
            return result
            
        except ZeroDivisionError:
            return "Cannot divide by zero"
        except Exception as e:
            return "Error"

    def button_click(self, value):
        if value == 'C':
            self.current_expression = ""
            self.display_var.set("")
        
        elif value == 'DEL':
            self.current_expression = self.current_expression[:-1]
            self.display_var.set(self.current_expression)
        
        elif value == '=':
            result = self.evaluate_expression(self.current_expression)
            self.display_var.set(result)
            self.current_expression = str(result) if result not in ["Error", "Cannot divide by zero"] else ""
        
        else:
            #special function inputs
            if value in ['sin', 'cos', 'tan', 'log']:
                self.current_expression += value
            elif value == '√':
                self.current_expression += '√'
            else:
                self.current_expression += value
            self.display_var.set(self.current_expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()