import tkinter as tk
from re import findall as find
from functools import partial
import Evaluar

class Calculadora:
    
    def __init__(self) -> None:
        
        #Definimos atributos recursivos
        self.font = "ChillPixels-Maximal"
        self.sizeTitle = 60
        self.sizeSubtitle = 30
        self.sizeText = 20
        self.style = {"bg":"black","fg":"white"}
        self.button_properties = {"font":(self.font,self.sizeText),"width":3,"height":2,"bg":"black","fg":"white"}
        
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
        calc.config(bg="black")
        
        #Texto de la entrada
        entry = tk.Label(calc,text="0",font=(self.font,self.sizeSubtitle),width=12,height=2)
        entry.grid(row=0,column=0,columnspan=6)
        
        #Ejecuta funciones de los botones C, DEL, +/-
        def execute_functions(index):
            #Borra lo que hay en la entrada
            if index == "C":
                entry.config(text="0")
                
            #Borra el ultimo digito o simbolo escrito
            elif index == "DEL":
                text = entry.cget("text") #Obtenemos el texto de la entrada
                
                if len(text) > 1:
                    #Si el tamaño del texto es mayor a 1 eliminamos el ultimo caracter
                    text = text[:-1]
                    entry.config(text=text)
                else:
                    entry.config(text="0") #Si es menor o igual a 1 se cambia el texto por un 0
            
            #Cambia el signo del ultimo valor escrito
            elif index == "+/-":
                expresion = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',entry.cget("text")) #Obtiene la expresion como una lista
                try:
                    valor = self.convertir_valor(expresion[-1])
                    #Si el tamaño de la expresion es de 1 solo se cambia el valor que esta alli
                    if len(expresion) == 1:
                        expresion[0] = str(valor*-1)
                    else:
                        #Si el valor es menor a 0 cambiamos el valor a positivo y agregamos un '+' antes del valor
                        if valor < 0 and expresion[-2] != "*" and expresion[-2] != "/":
                            expresion[-1] = "+"+str(valor*-1)
                        else:
                            #Si la penultima posicion es un '+' eliminamos ese '+' y hacemos el cambio de signo de valor
                            if expresion[-2] == "+":
                                expresion.pop(-2)
                                expresion[-1] = str(valor*-1)
                            else:
                                expresion[-1] = str(valor*-1)
                    
                    entry.config(text="".join(map(str,expresion))) #Actualizamos la entrada usando la lista expresion
                    
                except: pass #Si el except se ejecuta es debido a que la ultima posicion es un simbolo por ende no se hace nada

        #Ejecuta funciones de los botones M+, M-, MC, MR
        def execute_memory(index):
            if index == "M+" or index == "M-":
                entrada = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',entry.cget("text")) #Obtiene la expresion como una lista
                if self.memory == None:
                    try: self.memory = self.convertir_valor(entrada[0] if len(entrada) == 1 else entrada[-1])
                    except: pass #Si se ejecuta es porque la entrada es un simbolo
                else:
                    try:
                        valor = self.convertir_valor(entrada[0] if len(entrada) == 1 else entrada[-1])
                        self.memory = self.memory + valor if index == "M+" else self.memory - valor #Sumamos o restamos memory con valor
                    except: pass #Si se ejecuta es porque la entrada es un simbolo
            elif index == "MC":
                self.memory = None
            elif index == "MR":
                if self.memory != None:
                    entrada = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',entry.cget("text"))
                    if len(entrada) == 1:
                        entry.config(text=str(self.memory)) # cambiamos la entrada por lo que hay en memoria
                    else:
                        #Comprobamos que la ultima posicion no sea un simbolo
                        if entrada[-1] != "+" and entrada[-1] != "-" and entrada[-1] != "*" and entrada[-1] != "/":
                            #Si no hay simbolos se cambia la ultima posicion por memory
                            entrada[-1] = self.memory
                        else:
                            #Si hay un simbolo agregamos al final de la lista memory
                            entrada.append(self.memory)
                            
                        entry.config(text="".join(map(str,entrada))) #Actualizamos la entrada
     
        #Creamos una funcion para acutalizar la entrada
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
        
        #Creamos los botones
        def buttons():
            #Definimos los botones
            memo = ["M+","M-","MR","MC"]
            functions = ["PRO","C","DEL","+/-"]
            nums = ["7","8","9","4","5","6","1","2","3","0","."]
            symbols = ["/","*","-","+"]
            
            #Boton del igual para evaluar la expresion
            solve = tk.Button(calc,text="=",command=partial(update_label, entry.cget("text"), Evaluar=True),**self.button_properties)
            solve.grid(row=5,column=4)
            
            #Creamos los botones de memoria
            for i in range(len(memo)):
                col = i % 4
                memo_buttons = tk.Button(calc,text=memo[i],command=partial(execute_memory,memo[i]),**self.button_properties)
                memo_buttons.grid(row=1,column=col)
            #Creamos los botones de funciones 
            for i in range(len(functions)):
                row = (i % 5) + 2
                function_buttons = tk.Button(calc,text=functions[i],command=partial(execute_functions,functions[i]),**self.button_properties)
                function_buttons.grid(row=row,column=0)
            #Creamos los botones de numeros
            for i in range(len(nums)):
                row = (i // 3) + 2; col = i % 3 + 1
                
                #Creamos un condicional para cambiar el formato del boton '0'
                if nums[i] != "0":
                    buttons_nums = tk.Button(calc,text=nums[i],command=partial(update_label,nums[i]),**self.button_properties)
                else:
                    buttons_nums = tk.Button(calc,text=nums[i],command=partial(update_label,nums[i]),**self.button_properties)
                    buttons_nums.config(width=self.button_properties["width"]*2)
                
                #Debido a que se cambio el formato para el boton '0' se deben hacer ajustes en la grid
                if nums[i] != "." and nums[i] != "0":
                    buttons_nums.grid(row=row,column=col)
                elif nums[i] == ".":
                    buttons_nums.grid(row=row,column=col + 1)
                elif nums[i] == "0":
                    buttons_nums.grid(row=row,column=col,columnspan=2)
            #Creamos los botones de simbolos
            for i in range(len(symbols)):
                row = (i % 4) + 1
                buttons_symbols = tk.Button(calc,text=symbols[i],command=partial(update_label,symbols[i]),**self.button_properties)
                buttons_symbols.grid(column=4,row=row)
        
        buttons()
    
    def menu(self):
        #Nombre de ventana
        self.main.title("Calculadoras")
        self.main.config(bg="black")
        
        #Textos
        title = tk.Label(self.main,text="Bienvenid@",font=(self.font,self.sizeTitle),**self.style)
        title.grid(row=0,column=0,columnspan=3)
        description = tk.Label(self.main,text="¿Que desea realizar?",font=(self.font,self.sizeSubtitle),**self.style)
        description.grid(row=1,column=0,columnspan=3)
        
        #Botones
        calc1 = tk.Button(self.main,text="Calculadora Basica",font=(self.font,self.sizeText),height=7,command=self.calc_basic,**self.style)
        calc1.grid(row=2,column=0,pady=20)

Calculadora()