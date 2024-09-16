import tkinter as tk
from functools import partial
import Evaluar

class Calculadora:
    
    def __init__(self) -> None:
        
        #Definimos atributos recursivos
        self.font = "BOLD"
        self.sizeTitle = 50
        self.sizeSubtitle = 20
        self.sizeText = 12
        
        #Creamos nuestra interfaz
        self.main = tk.Tk()
        self.menu()
        
        self.main.mainloop()
    
    def evaluar(self,Exp,Tipo):
        try:
            if Tipo == "EE":
                instancia_evaluar = Evaluar.EvaluarExpresion(Exp,"NO","NO","NO")
            elif Tipo == "EF":
                instancia_evaluar = Evaluar.EvaluarFraccionarios(Exp,"NO","NO","NO")
            result = instancia_evaluar.respuesta
        except SyntaxError:
            result = "SyntaxError"
        except:
            result = "Error"
        
        return result
    
    def calc_basic(self):
        calc = tk.Toplevel()
        calc.title("Calculadora Basica")
        
        width = 3
        heigth = 2
        
        #Texto
        entry = tk.Label(calc,text="0",font=(self.font,self.sizeText))
        entry.grid(row=0,column=0,columnspan=5)
        
        #Creamos una funcion para acutalizar el label
        def update_label(index, Evaluar:str=False):
            if Evaluar:
                result = self.evaluar(Exp=entry.cget("text"),Tipo="EE")
                entry.config(text=result)
            else:
                actualtxt = entry.cget("text")
                if index != ".":
                    entry.config(text=index) if actualtxt == "0" or actualtxt == "Error" or actualtxt == "SyntaxError" else entry.config(text=actualtxt + index)
                else:
                    entry.config(text=actualtxt + index)
        
        #Definimos los botones
        nums = ["7","8","9","4","5","6","1","2","3","0","."]
        symbols = ["/","*","-","+"]
        
        solve = tk.Button(calc,text="=",font=(self.font,self.sizeText),width=width,height=heigth,command=partial(update_label, entry.cget("text"), Evaluar=True))
        solve.grid(row=4,column=2)
        for i in range(len(nums)):
            row = (i // 3) + 1
            col = i % 3
            buttons_nums = tk.Button(calc,text=nums[i],font=(self.font,self.sizeText),width=width,height=heigth,command=partial(update_label,nums[i]))
            buttons_nums.grid(row=row,column=col)
        for i in range(len(symbols)):
            row = (i % 4) + 1
            buttons_symbols = tk.Button(calc,text=symbols[i],font=(self.font,self.sizeText),width=width,height=heigth,command=partial(update_label,symbols[i]))
            buttons_symbols.grid(column=3,row=row)
    
    def menu(self):
        #Nombre de ventana
        self.main.title("Calculadoras")
        
        #Textos
        title = tk.Label(self.main,text="Bienvenid@",font=(self.font,self.sizeTitle))
        title.grid(row=0,column=0,columnspan=3)
        description = tk.Label(self.main,text="¿Que desea realizar?",font=(self.font,self.sizeSubtitle))
        description.grid(row=1,column=0,columnspan=3)
        
        #Botones
        calc1 = tk.Button(self.main,text="Calculadora Basica",font=(self.font,self.sizeText),height=7,command=self.calc_basic)
        calc1.grid(row=2,column=0,pady=20)

Calculadora()
#Hacer que muestre el resultado de la calc_basic