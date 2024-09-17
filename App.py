import tkinter as tk
from re import findall as find
from functools import partial
import Evaluar

class Calculadora:
    
    def __init__(self) -> None:
        
        #Definimos atributos recursivos
        self.font = "BOLD"
        self.sizeTitle = 50
        self.sizeSubtitle = 20
        self.sizeText = 12
        
        self.memory = None
        
        #Creamos nuestra interfaz
        self.main = tk.Tk()
        self.menu()
        
        self.main.mainloop()
    
    def evaluar(self,Exp,Tipo):
        #Creamos un try except para combrobar si el usuario tiene algun error en su expresion
        try:
            if Tipo == "EE":
                instancia_evaluar = Evaluar.EvaluarExpresion(Exp,"NO","NO","NO")
            elif Tipo == "EF":
                instancia_evaluar = Evaluar.EvaluarFraccionarios(Exp,"NO","NO","NO")
            
            result = instancia_evaluar.respuesta
        except SyntaxError:
            #Este tipo de error lo retorno Evaluar al comprobar si habia un error en la sintaxis
            result = "SyntaxError"
        except:
            #Este tipo de error es debido a que algo salio mal al intentar evaluar
            result = "Error"
        
        return result
    
    def convertir_valor(self,entry):
        return float(entry) if "." in entry else int(entry)
    
    def calc_basic(self):
        
        #Creamos la ventana
        calc = tk.Toplevel()
        calc.title("Calculadora Basica")
        
        #Definimos atributos para los botones
        button_properties = {"font":(self.font,self.sizeText),"width":3,"height":2}
        
        #Texto de la entrada
        entry = tk.Label(calc,text="0",font=(self.font,self.sizeText))
        entry.grid(row=0,column=0,columnspan=6)
        
        #Ejecuta funciones de los botones C, DEL, +/-
        def execute_functions(index):
            if index == "C":
                entry.config(text="0")
            elif index == "DEL":
                text = entry.cget("text")
                if len(text) > 1:
                    text = text[:-1]
                    entry.config(text=text)
                else:
                    entry.config(text="0")
            elif index == "+/-":
                expresion = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',entry.cget("text"))
                try:
                    valor = self.convertir_valor(expresion[-1])
                    if len(expresion) == 1:
                        expresion[0] = str(valor*-1)
                    else:
                        if valor < 0 and expresion[-2] != "*" and expresion[-2] != "/":
                            expresion[-1] = "+"+str(valor*-1)
                        else:
                            if expresion[-2] == "+":
                                expresion.pop(-2)
                                expresion[-1] = str(valor*-1)
                            else:
                                expresion[-1] = str(valor*-1)
                    entry.config(text="".join(map(str,expresion)))
                except:
                    pass
        
        def execute_memory(index):
            if index == "M+" or index == "M-":
                entrada = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',entry.cget("text"))
                if self.memory == None:
                    try: self.memory = self.convertir_valor(entrada[0] if len(entrada) == 1 else entrada[-1])
                    except: pass
                else:
                    try:
                        valor = self.convertir_valor(entrada[0] if len(entrada) == 1 else entrada[-1])
                        self.memory = self.memory + valor if index == "M+" else self.memory - valor
                    except: pass
            elif index == "MC":
                self.memory = None
            elif index == "MR":
                if self.memory != None:
                    entrada = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',entry.cget("text"))
                    if len(entrada) == 1:
                        entry.config(text=str(self.memory))
                    else:
                        entrada[-1] = self.memory
                        entry.config(text="".join(map(str,entrada)))
        
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
        memo = ["M+","M-","MR","MC"]
        functions = ["C","DEL","+/-"]
        nums = ["7","8","9","4","5","6","1","2","3","0","."]
        symbols = ["/","*","-","+"]
        
        #Boton del igual para evaluar la expresion
        solve = tk.Button(calc,text="=",command=partial(update_label, entry.cget("text"), Evaluar=True),**button_properties)
        solve.grid(row=5,column=3)
        
        #Creamos los botones
        for i in range(len(memo)):
            col = (i % 4) + 1
            memo_buttons = tk.Button(calc,text=memo[i],command=partial(execute_memory,memo[i]),**button_properties)
            memo_buttons.grid(row=1,column=col)
        for i in range(len(functions)):
            row = (i % 4) + 2
            function_buttons = tk.Button(calc,text=functions[i],command=partial(execute_functions,functions[i]),**button_properties)
            function_buttons.grid(row=row,column=0)
        for i in range(len(nums)):
            row = (i // 3) + 2
            col = i % 3 + 1
            buttons_nums = tk.Button(calc,text=nums[i],command=partial(update_label,nums[i]),**button_properties)
            buttons_nums.grid(row=row,column=col)
        for i in range(len(symbols)):
            row = (i % 4) + 2
            buttons_symbols = tk.Button(calc,text=symbols[i],command=partial(update_label,symbols[i]),**button_properties)
            buttons_symbols.grid(column=4,row=row)
    
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