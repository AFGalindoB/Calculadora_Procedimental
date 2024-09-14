from re import findall as find
from math import gcd
from colorama import Style,Fore

#Hacemos una clase que evalue nuestra expresion
class EvaluarExpresion:
    #Iniciamos nuestra clase:
    def __init__(self, Expresion:str,  VerProcedimiento:str, VerPrioridad:str = "NO", VerRespuesta:str = "SI") -> None:
        
        #Comprobamos que nuestra expresion sea valida
        self.comprobar_expresion_valida(Expresion)
        
        #Despues de pasar nuestras comprobaciones evaluamos nuestra expresion
        self.respuesta = self.evaluar(Expresion,VerPrioridad,VerProcedimiento,VerRespuesta)
        
        #Establecemos atributos utiles para nuestra clase
        self.Expresion = Expresion
    #Comprobamos que nuestra expresion ingresada sea valida
    def comprobar_expresion_valida(self, Expresion:str) -> None:
        
        if (len(Expresion) == 0):
            print(f"{Fore.RED + Style.BRIGHT}\nSu resultado de la ecuacion '0' ={Fore.MAGENTA} 0\n{Style.RESET_ALL}")
            exit()
            
        #Definimos variables generales
        SIMBOLOS = ["+","-","*","/"]
        Error = False
        
        #Hacemos comprobaciones antes de evaluar nuestra expresion
        
        #Comprobamos que la expresion no termine en algun simbolo
        for i in range(len(SIMBOLOS)):
            Inicia = Expresion.startswith(SIMBOLOS[i])
            Termina = Expresion.endswith(SIMBOLOS[i])
            if (i != 1 and Inicia == True):
                print(f"{Style.BRIGHT+Fore.RED}\n(SYNTAX ERROR):{Style.RESET_ALL} su expresion tiene un", SIMBOLOS[i],"al inicio de su expresion\n")
                Error = True
            if(Termina == True):
                print(f"{Style.BRIGHT+Fore.RED}\n(SYNTAX ERROR):{Style.RESET_ALL} su expresion tiene un", SIMBOLOS[i],"al final de su expresion\n")
                Error = True
        
        #Si existen parentesis en la expresion comprobamos que sean de la misma cantidad
        if ("(" in Expresion or ")" in Expresion):
            
            #Contamos nuestros parentesis
            ParentesisDeApertura = Expresion.count("(")
            ParentesisDeCierre = Expresion.count(")")
            
            #Comprobamos que la cantidad de parentesis sean iguales
            if (ParentesisDeApertura == ParentesisDeCierre):
                pass
            else:
                #Segun la situacion le informamos al usuario su error
                if (ParentesisDeApertura > ParentesisDeCierre):
                    print(f"{Style.BRIGHT+Fore.RED}\n(SYNTAX ERROR):{Style.RESET_ALL} No ah cerrado todos sus parentesis\n")
                else:
                    Contador = ParentesisDeCierre - ParentesisDeApertura
                    print(f"{Style.BRIGHT+Fore.RED}\n(SYNTAX ERROR):{Style.RESET_ALL} Ah puesto {Contador} parentesis ')' extra\n")
                Error = True
        
        #Si existe algun error en la ecuacion finalizamos nuestro programa
        if (Error == True):
            exit()
    #Hacemos que una funcion convierta los numeros de un string a valores enteros o flotantes
    def convertir_valor(self,valor):
        return float(valor) if "." in valor else int(valor)
    #Definimos una clase donde guardaremos todas las funciones que no son muy extensas
    class FuncionesExtra:
        
        def convertir_notacion_a_decimal(Valor):
            if "e" in str(Valor):
                Valor = str(format(Valor,".13f"))
            
            return Valor
        
        def comprobar_decimal_igual_a_cero(Entry):
            if ("." in Entry):
                Temp = find(r'-?\d+|\.|\d+',Entry)
                if (Temp[2] == "0"):
                    #Si sucede el caso hacemos que nuestro resultado solo sea un numero entero
                    Result = Temp[0]
                else:
                    Result = Entry
            else:
                Result = Entry
            return Result
        
        #Creamos una funcion que nos transforme todo a una string en caso de que lo tengamos como una lista
        def convertir_lista_a_string(Entry: str | list):
            if(isinstance(Entry,list)):
                Txt = "".join(map(str,Entry))
            elif(isinstance(Entry,str)):
                Txt = Entry
            
            return Txt
    #Tokenizamos nuestra ecuacion para evaluarla
    def tokenizar(self, Expr: list | str, Ver: str = "NO", Parentesis:str = "NO") -> list:
        """
        Convierte nuestra expresion en un token (una lista) segun las condiciones para poder iterar
        sobre nuestra ecuacion y resolverla paso a paso
        """
        
        #En caso de que nuestra entrada sea una lista la convertimos a un string
        Expr = self.FuncionesExtra.convertir_lista_a_string(Expr)
        
        #Recreamos los tokens segun la prioridad
        if ("(" in Expr):
                
            #Definimos variables generales
            i = 0; i1 = 1
                
            #Tokenizamos nuestra ecuacion
            Token = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',Expr)
                
            #Iteramos sobre nuestros tokens para que los podamos evaluar utilmente
            while i1 < len(Token):
                    
                #Creamos variables que al iniciar/reiniciar el bucle esten en False para comprobar
                Indice1 = False
                Indice2 = False

                #Comprobamos que nuestro primer indice no sea un parentesis
                if ((Token[i] != "(")and(Token[i] != ")")):
                    Indice1 = True                
                    
                if ((Token[i1] != "(")and(Token[i1] != ")")):    
                    Indice2 = True
                    
                #Si ambos indices son true significa que son una expresion y no un parentesis
                if ((Indice1 == True) and (Indice2 == True)):
                        
                    #Juntamos 2 posiciones de un token en solo una posicion
                    Token[i] += Token[i1]
                    Token.pop(i1)
                    
                else:
                    #Aumentamos el valor en 1 para que se siga buscando mas valores de nuestra operacion
                    i += 1
                    i1 += 1
                
        elif (("*" in Expr) or ("/" in Expr)):
            Token = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/',Expr)
        else:
            Token = find(r'\d*\.\d+|\d+|\b\w+\b|\+|\-|\*|\/',Expr)
            
        if (Token[0] == "-"):
            Token[0] += Token[1]
            Token.pop(1)
            
        if (Token[0] == "+"):
            Token.pop(0)
        
        return Token
    #Creamos una funcion que simplifique nuestros parentesis
    def simplificar_parentesis(self,Expr:list,VerPrio:str,VerPro:str) -> list:
        """
        Simplifica nuestos parentesis hasta que no existan mas parentesis en la ecuacion
        (Retorna nuestra expresion sin parentesis)
        """
        
        #Le informamos al usuario que empezaremos por despejar parentesis
        if (VerPro == "SI"):
            print(f"Empezamos por despejar nuestros parentesis")
        
        #Contamos los pares de parentesis que hay en nuestra expresion
        ExprTxt = "".join(map(str,Expr))
        Contador = ExprTxt.count(")")
        
        #Despejamos todos nuestros pares de parentesis
        for i in range(Contador):
            #Buscamos el primer parentesis a despejar
            Pos = Expr.index(")")
            
            #Guardamos la expresion que hay dentro de nuestro parentesis en una variable
            Temp = Expr[Pos - 1]
            
            #Le informamos al usuario lo que despejaremos
            if (VerPro == "SI"):
                print(f"Despejamos: (", Temp,")\n",sep="")
            
            #Operamos hasta que en nuestros parentesis solo quede un numero
            while len(Temp) > 1:
                #Tokenizamos nuestra expresion temporal
                Temp = self.tokenizar(Temp)
                
                if (len(Temp) == 1):
                    #Si el tamaño de nuestra variable temporal es 1 significa que ya esta simplificada
                    break
                
                #Buscamos la prioridad de nuestra expreson
                PrioridadPOS = self.prioridad_a_operar(Temp,VerPrio)
                
                #Operamos
                Temp = self.operar(Temp,PrioridadPOS,VerPro)
                
                #Actualizamos nuestra expresion
                Txt = "".join(map(str,Temp))
                Expr[Pos - 1] = Txt
                Temp = self.tokenizar(Temp)
                
                #Si nuestra lista temp es mayor a 1 mostramos al usuario la expresion
                if (len(Temp) > 1):
                    if (VerPro == "SI"):
                        self.mostrar_ecuacion(Expr)
                
            #Despues de operar revisamos si hay que operar signos antes de quitar los parentesis
            Expr = self.operar_simbolos(Expr,VerPro)
            
            #Eliminamos los parentesis
            Pos = Expr.index(")")
            Expr.pop(Pos)
            Expr.pop(Pos - 2)
            Expr = self.tokenizar(Expr)
            
            #Mostramos al usuario nuestra expresion despues de simplificar
            if (VerPro == "SI"):
                self.mostrar_ecuacion(Expr)
            
        return Expr
    #Creamos una funcion que nos verifique si hay que operar signos al simplificar un parentesis
    def operar_simbolos(self,Expresion:list,Ver:str) -> list:
        """
        Si nuesta expresion necesecita operar signos para simplificar los parentesis 
        la funcion se encarga de comprobar esto y operar el numero dentro de los parentesis
        con el - fuera del parentesis
        """
        
        #Obtenemos nuestros tokens
        Token = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',"".join(map(str,Expresion)))
        
        #Obtenemos la posicion de nuestra prioridad
        Pos = Token.index(")") - 1
        
        #Hacemos una variable que nos registre la posicion del menos
        Verifica = Pos - 2
        
        #Hacemos nuestra comprobacion
        if (Token[Pos - 2] == "-" and ((Verifica == 0) or (Token[Pos - 3] == "(" or Token[Pos - 3] == "*" or Token[Pos - 3] == "/" or Token[Pos - 3] == "+" or Token[Pos - 3] == "-"))):
            
            if (Ver == "SI"):
                self.mostrar_ecuacion(Expresion)
            
            #Le informamos al usuario lo que haremos
            if (Ver == "SI"):
                print(f"{Fore.GREEN}Debido a que tenemos un menos fuera de nuestros parentesis operamos signos - *", Token[Pos],"y despejamos nuestros parentesis",Style.RESET_ALL,"\n")
            
            #Operamos signos
            if ("." in Token[Pos]):
                Token[Pos] = float(Token[Pos]) * -1
            else:
                Token[Pos] = int(Token[Pos]) * -1
            
            #Eliminamos el - fuera de nuestros parentesis
            Token.pop(Pos - 2)
        
        #Tokenizamos nuestra expresion para retornarla con las mismas condiciones con las que la recibimos
        Token = self.tokenizar(Token,Ver,"SI")
         
        return Token
    #Creamos una funcion para operar una prioridad BODMAS/PEDMAS
    def prioridad_a_operar(self,Token:list,Ver:str) -> int:
        """
        Evalua nuestra expresion y segun el nivel de prioridad (siguiendo la regla matematica de PEDMAS/BODMAS)
        nos retorna la posicion de la prioridad
        """

        #Definimos Variables generales
        NombreSim = ["Multiplicacion","Division","Resta","Suma"]
        Simbolos = ["*","/","-","+"]
        VarName = ["BuscarMul","BuscarDiv","BuscarRes","BuscarSum"]
        Variables = {}
        Prioridad = ""
        PrioridadPos = None
            
        #Creamos los print de cada una de las los simbolos segun existan
        for i in range(len(Simbolos)):
            if (Simbolos[i] in Token):
                Variables[VarName[i]] = Token.index(Simbolos[i])
                if (Ver == "SI"):
                    print(f"\tSu simbolo de {NombreSim[i]} se encuentra en la posicion {Variables[VarName[i]]}")
            else:
                Variables[VarName[i]] = "NA"
                if (Ver == "SI"):
                    print(f"\tNo se encontro el simbolo de {NombreSim[i]}")
        
        #Definimos las prioridades
        if ((isinstance(Variables["BuscarMul"],int) and isinstance(Variables["BuscarDiv"],int)) and (Variables["BuscarMul"]< Variables["BuscarDiv"]) or (Variables["BuscarDiv"] == "NA" and Variables["BuscarMul"] != "NA")):
            Prioridad = "*"
            PrioridadPos = Variables["BuscarMul"]
        elif ((isinstance(Variables["BuscarMul"],int) and isinstance(Variables["BuscarDiv"],int)) and Variables["BuscarDiv"]< Variables["BuscarMul"] or (Variables["BuscarDiv"] != "NA" and Variables["BuscarMul"] == "NA")):
            Prioridad = "/"
            PrioridadPos = Variables["BuscarDiv"]
        else:
            if ((isinstance(Variables["BuscarSum"],int) and isinstance(Variables["BuscarRes"],int)) and Variables["BuscarSum"] < Variables["BuscarRes"] or (Variables["BuscarRes"] == "NA" and Variables["BuscarSum"] != "NA")):
                Prioridad = "+"
                PrioridadPos = Variables["BuscarSum"]
            elif ((isinstance(Variables["BuscarSum"],int) and isinstance(Variables["BuscarRes"],int)) and Variables["BuscarRes"]< Variables["BuscarSum"] or (Variables["BuscarRes"] != "NA" and Variables["BuscarSum"] == "NA")):
                Prioridad = "-"
                PrioridadPos = Variables["BuscarRes"]
            else:
                Prioridad = "NA"
                PrioridadPos = None
        
        #Le informamos al usuario la prioridad
        if (Ver == "SI"):
            print(f"{Style.BRIGHT}\nPrioridad = '" + Prioridad +f"'{Style.NORMAL}")
        return PrioridadPos
    #Operamos nuestra expresion
    def operar(self,Token:list,Posicion:int,Ver:str) -> list:
        """
        Obtiene la lista de tokens y la posicion de la prioridad y con ellos opera nuestra expresion
        simplificandola poco a poco hasta que solo queda nuestra respuesta
        """
        
        #Comprobamos que la posicion despues de nuestra prioridad no sea un '-'
        if (Token[Posicion + 1] == "-"):
            Token[Posicion + 1] += Token[Posicion + 2]
            Token.pop(Posicion + 2)
        
        #Definimos variables generales
        ValorIzq = self.convertir_valor(Token[Posicion - 1])
        ValorDer = self.convertir_valor(Token[Posicion + 1])
        Sym = Token[Posicion]
        
        #Le informamos al usuario que operaremos
        if (Ver == "SI"):
            print(f"\n{Fore.BLUE}{Style.BRIGHT}","="*10," ( ","Operamos:",Token[Posicion - 1],Token[Posicion],Token[Posicion + 1]," ) ","="*10,f"\n{Style.RESET_ALL}",sep="")
        
        #Segun el tipo de simbolo operaremos nuestros valores
        if (Sym == "*"):
            Resultado = ValorIzq * ValorDer
        elif(Sym == "/"):
            if (ValorDer != 0):
                Resultado = ValorIzq / ValorDer
            else:
                print(Fore.RED,"="*10,"No se puede dividir entre 0","-"*10,"\n",Style.RESET_ALL,sep="")
                print("La ecuacion no puede ser realizada\n")
                exit()
        elif(Sym == "+"):
            Resultado = ValorIzq + ValorDer
        elif(Sym == "-"):
            Resultado = ValorIzq - ValorDer
        
        #Comprobamos que el decimal de nuestro numero no sea .0
        Resultado = self.FuncionesExtra.comprobar_decimal_igual_a_cero(str(Resultado))
        
        ValorDer = self.FuncionesExtra.convertir_notacion_a_decimal(ValorDer)
        ValorIzq = self.FuncionesExtra.convertir_notacion_a_decimal(ValorIzq)
        Resultado = str(self.FuncionesExtra.convertir_notacion_a_decimal(self.convertir_valor(Resultado)))
        
        #Le mostramos al usuario el resultado de lo que operamos
        if (Ver == "SI"):
            print(f"{Fore.BLUE} {ValorIzq} {Fore.RED} {Sym} {Fore.BLUE} {ValorDer} {Fore.RED} =", Style.BRIGHT ,Fore.GREEN, Resultado , Style.RESET_ALL,"\n")
        
        #Debido a que si operamos simbolos negativos el resultado va a ser positivo por ende se pierde un simbolo
        if ((Sym == "/" or Sym == "*") and (ValorIzq < 0 and ValorDer < 0)):
            Resultado = "+" + Resultado
        
        #Simplificamos lo que acabamos de operar y asignamos nuestro resultado a la ecuacion
        Token[Posicion - 1] = Resultado
        Token.pop(Posicion +1)
        Token.pop(Posicion)
        
        return Token
    #Mostramos al usuario lo que vamos a operar
    def mostrar_ecuacion(self,Token: list | str, Parentesis:str = "NO") -> None:
        
        #Llamamos una funcion que nos transforme todo a una string en caso de que lo tengamos como una lista
        Expr = self.FuncionesExtra.convertir_lista_a_string(Token)
        
        #Creamos un condicional que verifique si hay que informarle al usuario si esta operando la expresion o unos parentesis
        if (Parentesis == "NO"):
            print(f"{Fore.MAGENTA}Expresion: {Style.RESET_ALL}{Expr}\n")
        else:
            print(f"{Fore.MAGENTA}Parentesis a despejar: {Style.RESET_ALL}({Expr})\n")
    #Evaluamos nuestra ecuacion
    def evaluar(self, Expresion:str, VPrioridad:str, VProcedimiento:str,VerRespuesta:str) -> str:
        """Este metodo se encarga de evaluar toda la expresion y encontrar la respuesta organizando el flujo por el cual
        pasara la expresion para ser resuelta (Este metodo sera el que abarque todos los demas de la clase segun sea necesario)
        """
        
        #Definimos variables generales
        VPrioridad = VPrioridad.upper()
        VProcedimiento = VProcedimiento.upper()
        
        #Tokenizamos nuestra expresion
        if "^" in Expresion:
            Token = EvaluarPotencias(Expresion,VPrioridad,VProcedimiento,VerRespuesta="NO").respuesta
        else:
            Token = self.tokenizar(Expresion)
        
        #Si hay parentesis los simplificamos primero
        if (VProcedimiento == "SI"):
            self.mostrar_ecuacion(Token)
        
        if ("(" in Expresion):
            Token = self.simplificar_parentesis(Token,VPrioridad,VProcedimiento)
        
        PrioridadPOS = self.prioridad_a_operar(Token,VPrioridad)
        while len(Token) > 1:
            Token = self.operar(Token,PrioridadPOS,VProcedimiento)
            if(Token[0].startswith("+")):
                Token = self.tokenizar(Token)
            if len(Token) > 1:
                Token = self.tokenizar(Token)
                if (VProcedimiento == "SI"):
                    self.mostrar_ecuacion(Token)
                PrioridadPOS = self.prioridad_a_operar(Token,VPrioridad)
            else:
                break
        
        #Redondeamos nuestra respuesta
        if ("." in Token[0]):
            Temp = self.convertir_valor(Token[0])
            if "e" in str(Temp):
                ResultadoAprox = str(format(Temp,".13f"))
            else:
                ResultadoAprox = str(round(Temp,13))
            
            if "." in ResultadoAprox:
                if str(ResultadoAprox).endswith("0"):
                    ResultadoAprox = str(ResultadoAprox).rstrip("0")
                    Token[0] = str(Token[0]).rstrip("0")
                else:
                    ResultadoAprox = str(ResultadoAprox)
            
        else:
            ResultadoAprox = None
        
        #Creamos un condicional donde segun lo que halla en el string se muestre en la terminal el resultado
        if (VerRespuesta.upper() == "SI"):
            #Creamos un condicional que nos muestre el valor resultante de nuestra expresion
            if (Token[0] == ResultadoAprox or ResultadoAprox == None):
                print(f"{Fore.RED + Style.BRIGHT}\nSu resultado de la ecuacion '{Expresion}' ={Fore.MAGENTA} {Token[0]}\n{Style.RESET_ALL}")
            else:
                #Si el resultado fue redondeado le mostramos al usuario el resultado sin aproximar y el resultado aproximado
                print(f"{Fore.RED + Style.BRIGHT}\nSu resultado de la ecuacion '{Expresion}' = {Fore.MAGENTA}{Token[0]}{Fore.RED} ≈{Fore.MAGENTA} {ResultadoAprox} \n{Style.RESET_ALL}")
        
        #Retornamos nuestro resultado
        if (ResultadoAprox != None):
            return str(ResultadoAprox)
        else:
            return str(Token[0])
    
class EvaluarFraccionarios(EvaluarExpresion):
    
    def __init__(self, Expresion: str, VerProcedimiento: str, VerPrioridad: str = "NO", VerRespuesta:str = "SI") -> None:
        
        #Comprobamos que si podamos evaluar la expresion
        self.comprobar_expresion_valida(Expresion)
        
        #Evaluamos la expresion
        self.respuesta = self.evaluar(Expresion,VerPrioridad,VerProcedimiento,VerRespuesta)
        
        #Definimos atributos que pueden servirnos
        self.Expresion = Expresion
    
    def comprobar_expresion_valida(self, Expresion: str) -> None:
        return super().comprobar_expresion_valida(Expresion)
    
    def simplificar_parentesis(self, Expr: list, VerPro: str, VerPrio:str) -> list:
        """
        Simplifica nuestos parentesis hasta que no existan mas parentesis en la ecuacion
        (Retorna nuestra expresion sin parentesis)
        """
        
        #Le mostramos al usuario lo que haremos
        if (VerPro == "SI"):
            print(Fore.CYAN,"-"*20,"| EMPEZAMOS POR DESPEJAR NUESTROS PARENTESIS |","-"*20,Fore.RESET,"\n",sep="")
        
        #Contamos nuestos parentesis
        ExprTxt = "".join(map(str,Expr))
        Contador = ExprTxt.count(")")
        
        #Despejamos todos nuestros parentesis
        for i in range(Contador):
            
            #Buscamos el primer parentesis a despejar y la expresion del parentesis la alamcenamos en una variable
            Pos = Expr.index(")")
            Temp = Expr[Pos - 1]
            
            #Le mostramos al usuario los parentesis que despejaremos
            if (VerPro == "SI"):
                print(f"Despejamos: (", Temp,")\n",sep="")
            
            #Simplificamos los parentesis
            while len(Temp) >= 1:
                
                Temp1 = self.FuncionesExtra.convertir_lista_a_string(Temp)
                #Tokenizamos nuestra expresion para operarla con mas facilidad
                Temp = self.tokenizar(Temp,VerPro,Parentesis="SI",Txt=Expr)
                Temp2 = self.FuncionesExtra.convertir_lista_a_string(Temp)
                
                #Temp1 y Temp2 actuan como un comparador donde si ambos strings no son iguales
                #Significa que tokenizar hizo cambios en nuestra expresion por ende actualizamos nuestra lista
                if (Temp1 != Temp2):
                    Txt = "".join(map(str,Temp))
                    Expr[Pos - 1] = Txt
                    if (VerPro == "SI"):
                        self.mostrar_ecuacion(Expr)
                
                #Evaluamos la expresion hasta que quede solo una fraccion
                if (len(Temp) == 1):
                    #Cuando se termina de simplificar expresion dividimos la fraccion
                    Temp = EvaluarExpresion.tokenizar(self,Temp)
                    Temp = EvaluarExpresion.operar(self,Temp,1,VerPro)
                    Txt = "".join(map(str,Temp))
                    Expr[Pos - 1] = Txt
                    break
                elif (len(Temp) > 1):
                    #Buscamos la prioridad y operamos nuestra expresion
                    PrioridadPOS = self.prioridad_a_operar(Temp,VerPrio)
                    Temp = self.operar(Temp,PrioridadPOS,VerPro)
                    
                    #Actualizamos nuestra expresion
                    Txt = "".join(map(str,Temp))
                    Expr[Pos - 1] = Txt
                    
                    #Mostramos al usuario la expresion despues de haber simplificado
                    if (VerPro == "SI"):
                        self.mostrar_ecuacion(Expr)
                    
                    #Actualizamos nuestros token
                    Temp = self.tokenizar(Temp,VerPro,Parentesis="SI")
            
            #Llamamos el metodo operar_simbolos y operamos signos en caso de ser necesario
            Expr = self.operar_simbolos(Expr,VerPro)
            
            #Buscamos el parentesis en la expresion que estabamos operando
            Pos = Expr.index(")")
            
            #Eliminamos los parentesis
            Expr.pop(Pos)
            Expr.pop(Pos - 2)
            
            #Mostramos al usuario su expresion despues de haber simplificado nuestros parentesis
            if (VerPro == "SI"):
                self.mostrar_ecuacion(Expr)
            
            #Volvemos a tokenizar la expresion 
            Expr = self.tokenizar(Expr,VerPro)
        
        #Retornamos nuestra expresion sin parentesis
        return Expr
    #Simplificamos nuestra fraccion por medio del Maximo Comun Divisor
    def simplificar_con_MCD(self, Numerador:int, Denominador:int, Ver:str):
        """Definimos un metodo que encuentre en Maximo Comun Divisor de nuestra fraccion para simplificarla"""
        
        if (Denominador == 0):
            #Si nuestro denominador es 0 no buscamos el MCD
            return str(Numerador) + "/" + str(Denominador)
        else:
            #Calculamos el Maximo Comun Divisor
            mcd = gcd(Numerador,Denominador)
            
            #Comprobamos que el MCD no sea 1
            if (mcd != 1):
                #Simplificamos nuestra expresion
                Numer = Numerador // mcd
                Denom = Denominador // mcd

                #Comprobamos la cantidad de digitos de nuestra fraccion y nuestro MCD
                Size = self.FuncionesExtra.comprobar_tamano(Numerador,Denominador)
                Size1 = len(str(mcd))
                Size2 = self.FuncionesExtra.comprobar_tamano(Numer,Denom)
                    
                #Centramos nuestra fraccion visualmente
                Numerador = self.FuncionesExtra.centrar_fraccion(Numerador,Size)
                Denominador = self.FuncionesExtra.centrar_fraccion(Denominador,Size)
                Numer = self.FuncionesExtra.centrar_fraccion(Numer,Size2)
                Denom = self.FuncionesExtra.centrar_fraccion(Denom,Size2)
                
                if(Ver == "SI"):
                    
                    #Mostramos al usuario el valor de nuestro MCD
                    print(f"{Fore.GREEN}Nuestro Maximo Comun Divisor es:{Fore.YELLOW}", mcd)
                    
                    #Mostramos al usuario lo que haremos
                    print(f"{Style.RESET_ALL}Simplificamos nuestra fraccion: ")
                    
                    #Se mostrara en pantalla lo siguente (Fraccion inicial) | (El MCD) = (Fraccion simplificada)
                    print(f"\n{Fore.BLUE}{Numerador}{Fore.YELLOW} | {mcd}  ", " "*Size1, f"{Fore.BLUE}{Numer}", sep="")
                    print("-"*Size, f"{Fore.YELLOW} | ", " "*Size1, f"{Fore.RED} = {Fore.BLUE}", "-"*Size2, sep="")
                    print(f"{Denominador}{Fore.YELLOW} | ", " "*Size1, f"   {Fore.BLUE}{Denom}{Style.RESET_ALL}\n" ,sep="")
                
                #Convertimos nuestras variables de tipo string en variables de tipo numericas
                Denom = self.convertir_valor(Denom)
                Numer = self.convertir_valor(Numer)
                
                #Comprobamos que nuestro denominador no sea negativo
                if (Denom < 0):
                    
                    #Si se da el caso hacemos el cambio de signos
                    Numer = -Numer
                    Denom = -Denom
                    
                    #Mostramos al usuario lo hecho
                    if(Ver == "SI"):
                        print(f"Como nuestro denominador es negativo lo cambiamos a positivo: {Numer}/{Denom}\n")
                
                #Retornamos nuestra fraccion simplificada
                return str(Numer) + "/" + str(Denom)
            else:
                #En caso de que el MCD sea uno significa que no se puede simplificar la expresion
                if(Ver == "SI"):
                    #Le informamos al usuario la situacion
                    print(f"La fraccion '{Numerador}/{Denominador}' no se puede simplificar\n")
                
                #Retornamos la expresion tal cual fue recibida
                return str(Numerador) + "/" + str(Denominador)
    
    def operar_simbolos(self, Expresion: list, Ver: str) -> list:
        return super().operar_simbolos(Expresion, Ver)
    
    def convertir_valor(self, valor):
        return super().convertir_valor(valor)
    
    def tokenizar(self, Expr: list | str, Ver:str, Parentesis: str = "NO", Txt: list | str = "NA") -> list:
        """Definimos un metodo que lea nuestra expresion como un string y la convierta en una lista de fracciones
        Esto para operar paso a paso nuestras expresiones (ejemplo de lista resultado: ["19/2", "*", "25/4", "+", "12/6", ...])
        """
        
        #llamamos una funcion que nos transforme todo a una string en caso de que lo tengamos como una lista
        Expr = self.FuncionesExtra.convertir_lista_a_string(Expr)
        Txt = self.FuncionesExtra.convertir_lista_a_string(Txt)
        
        #Definimos una variable para saber si se ah convertido algun un numero en una fraccion
        Convert = False
        
        #Definimos una variable que nos indique en que posicion de nuestra lista operaremos
        FracNum = 0
            
        #Tokenizamos nuestra expresion
        if ("(" in Expr):
            #Si nuestra expresion tiene parentesis usamos la tokenizacion de la clase padre
            return super().tokenizar(Expr)
        else:
            
            #Tokenizamos una lista con un patron que divida a numeros (Decimales o enteros) y simbolos matematicos
            Token = find(r'\d*\.\d+|\d+|\+|\-|\*|\/',Expr)

            #FracNum actuara como un indice el cual hara que se concatenen fracciones o en su defecto se transformen numeros en fracciones
            #FracNum trabajara con 3 indices 0, 1 y 2 donde las posiciones 0 y 2 deben ser numeros y la posicion 1 debe ser un "/"
            #Haciendo asi que FracNum convierta a 3 indices de una fraccion en uno solo
            #Esto para que el resultado de nuestra lista sea el siguente [Fraccion, Simbolo, Fraccion, Simbolo, ...]
            #Siguiendo esta regla hacemos que nuestra lista se divida por medio de fracciones
            while FracNum < len(Token):
                
                #Verificamos que en Fracnum los indices 0 y 2 no sean un "-"
                #Si se da el caso significa que estamos hablando de un numero negativo
                #Por ende concatenamos el "-" con nuesto numero
                if (Token[FracNum] == "-"):
                    Token[FracNum] += Token[FracNum + 1]
                    Token.pop(FracNum + 1)
                if (FracNum + 2 < len(Token) and Token[FracNum + 2] == "-"):
                    Token[FracNum + 2] += Token[FracNum + 3]
                    Token.pop(FracNum + 3)
                
                #Si en FracNum el indice numero 1 no es un "/" signfica que el indice numero 0 no esta expresado como una fraccion
                #Por ende lo convertimos a una
                if (FracNum + 1 < len(Token) and Token[FracNum + 1] != "/"):
                    self.FuncionesExtra.mostrar_conversion_de_numero_a_fraccion(Token,FracNum,Ver,Parentesis=Parentesis,Txt=Txt,Convert=Convert)
                    #Hacemos que el indice 0 de FracNum sea una fraccion con denominador igual a 1
                    Token[FracNum] += "/1"
                    
                    #Como FracNum ya cumplio su tarea de hacer que un indice de nuestra lista sea una fraccion
                    #Aumentamos el valor de FracNum en 2
                    #El primer aumento es para no seguir concatenando a la misma fraccion
                    #Y el segundo aumento para que evite un simbolo matematico ya sea un "+", "-", "*" o un "/"
                    FracNum += 2
                    Convert = True
                else:
                    #Agregamos nuestro divisor
                    if (FracNum + 1 < len(Token)):
                        Token[FracNum] += Token[FracNum + 1]
                    else:
                        #Si no hay un "/" en la ultima posicion significa que esta posicion no tiene un denominador
                        if ("/" not in Token[-1]):
                            
                            self.FuncionesExtra.mostrar_conversion_de_numero_a_fraccion(Token,-1,Ver,Parentesis=Parentesis,Txt=Txt,Convert=Convert)
                            
                            #Convertimos el ultimo indice en una fraccion
                            Token[-1] += "/1"
                            Convert = True
                        
                        #Si el condicional "if (FracNum + 1 < len(Token))" no se cumple significa FracNum ah sobrepasado las posiciones de la lista
                        #Por ende salimos de nuestro bucle
                        break

                    #Concatenamos a nuestra fraccion el indice numero 2 de FracNum (Nuestro denominador)
                    if (FracNum + 2 < len(Token)):
                        Token[FracNum] += Token[FracNum + 2]
                        Token.pop(FracNum + 2)
                    
                    Token.pop(FracNum + 1)
                    FracNum += 2
            
            if (Convert):
                if (Ver == "SI"):
                    print("\n")
        
        #Retornamos nuestra lista actualizada
        return Token
    #Definimos una clase donde guardaremos todas las funciones que no son muy extensas
    class FuncionesExtra:
        """Es una clase la cual guarda funciones con codigo no muy extenso"""
        
        def convertir_notacion_a_decimal(Valor):
            return EvaluarExpresion.FuncionesExtra.convertir_notacion_a_decimal(Valor)
        
        def comprobar_decimal_igual_a_cero(Entry):
            return EvaluarExpresion.FuncionesExtra.comprobar_decimal_igual_a_cero(Entry)
        #Definimos una funcion la cual comprobara el tamaño en cuanto a digitos de nuestro denominador y numerador
        def comprobar_tamano(Nume,Denom):
            if (len(str(Nume))>=len(str(Denom))):
                Size = len(str(Nume))
            else:
                Size = len(str(Denom))
            #Dependiendo de cual entrada sea mayor en cuanto a digitos retornara la cantidad de digitos que sea mayor
            return Size
        #Definimos una funcion la cual mostrara al usuario que numero fue convertido a una fraccion
        def mostrar_conversion_de_numero_a_fraccion(Lista:list,Posicion:int,Ver:str,Parentesis:str = "NO",Txt:str = "NA",Convert:bool = True):
            if (Ver.upper() == "SI"):
                if (not Convert):
                    print()
                Text = "".join(map(str,Lista))
                #Mostramos al usuario el indice que convertiremos a una fraccion
                if (Parentesis == "NO"):
                    print(f"{Fore.BLACK}En la expresion {Fore.YELLOW}{Text}{Fore.BLACK} convertimos a fraccion el numero:{Fore.YELLOW} {Lista[Posicion]}{Fore.RED} = {Fore.YELLOW}{Lista[Posicion]}/1{Style.RESET_ALL}")
                else:
                    print(f"{Fore.BLACK}En la expresion {Fore.YELLOW}{Txt}{Fore.BLACK} en los parentesis a despejar {Fore.YELLOW}({Text}){Fore.BLACK} convertimos a fraccion el numero: {Fore.YELLOW}{Lista[Posicion]}{Fore.RED} = {Fore.YELLOW}{Lista[Posicion]}/1{Style.RESET_ALL}")
        #Definimos una funcion que centrara visualmente nuestra fraccion
        def centrar_fraccion(Valor,Fraccion):
            return str(Valor).center(Fraccion)
        
        def convertir_lista_a_string(Entry):
            return EvaluarExpresion.FuncionesExtra.convertir_lista_a_string(Entry)
    
    def prioridad_a_operar(self, Token: list, Ver: str) -> int:
        return super().prioridad_a_operar(Token, Ver)
    #Creamos una funcion que nos muestre visualmente nuestra fraccion de una mejor manera
    def mostrar_fraccion(self,NumeDer,DenomDer,NumeIzq,DenomIzq,Sym,OpTxt="NA",Title="A",NumRes="NA",DenomRes="NA",NumOp="NA"):
        """Es un metodo el cual hara que se muestre de una forma mas comoda como vamos a operar nuestras fracciones"""
        
        #Definimos un string que usaremos recurrentemente
        Str = f' Operamos "{OpTxt}": | '
        Sym = str(Sym)
        
        #SizeFrac1 abarcara el tamaño de la fraccion que se encuentra a la izquierda
        SizeFrac1 = self.FuncionesExtra.comprobar_tamano(NumeIzq,DenomIzq)
        #SizeFrac2 abarcara el tamaño de la fraccion que se encuentra a la derecha
        SizeFrac2 = self.FuncionesExtra.comprobar_tamano(NumeDer,DenomDer)
        #SizeFrac2_5 abarcara el tamaño de la fraccion intermedia de haber hecho regla de la carita feliz
        SizeFrac2_5 = self.FuncionesExtra.comprobar_tamano(NumOp,DenomRes)
        #SizeFrac3 abarcara el tamaño del resultado de la fraccion operada
        SizeFrac3 = self.FuncionesExtra.comprobar_tamano(NumRes,DenomRes)
        
        #Si la entrada NumRes es igual a "NA" significa que solo queremos mostrar 2 fracciones a operar
        if (NumRes == "NA"):
            #Definimos 2 variables (Numeradores y Denominadores) donde se almacenara un string con la siguente estructura "(Fraccion1)   (Fraccion2)"
            Numeradores = self.FuncionesExtra.centrar_fraccion(NumeIzq,SizeFrac1) + "   " + self.FuncionesExtra.centrar_fraccion(NumeDer,SizeFrac2)
            Denominadores = self.FuncionesExtra.centrar_fraccion(DenomIzq,SizeFrac1) + "   " + self.FuncionesExtra.centrar_fraccion(DenomDer,SizeFrac2)
        else:
            #Si la entrada NumOP es igual a "NA" significa que queremos mostrar el resultado de haber operado 2 fracciones sin usar regla de la carita feliz
            if (NumOp == "NA"):
                #Definimos 2 variables (Numeradores y Denominadores) donde se almacenara un string con la siguente estructura "(Fraccion1)   (Fraccion2)   (FraccionResultado)"
                Numeradores = self.FuncionesExtra.centrar_fraccion(NumeIzq,SizeFrac1) + "   " + self.FuncionesExtra.centrar_fraccion(NumeDer,SizeFrac2) + "   " + self.FuncionesExtra.centrar_fraccion(NumRes,SizeFrac3)
                Denominadores = self.FuncionesExtra.centrar_fraccion(DenomIzq,SizeFrac1) + "   " + self.FuncionesExtra.centrar_fraccion(DenomDer,SizeFrac2) + "   " + self.FuncionesExtra.centrar_fraccion(DenomRes,SizeFrac3)
            else:
                #Definimos 2 variables (Numeradores y Denominadores) donde se almacenara un string con la siguente estructura "(Fraccion1)   (Fraccion2)   (FraccionIntermedia)   (FraccionResultado)"
                Numeradores = self.FuncionesExtra.centrar_fraccion(NumeIzq,SizeFrac1) + "   " + self.FuncionesExtra.centrar_fraccion(NumeDer,SizeFrac2) + "   " + self.FuncionesExtra.centrar_fraccion(NumOp,SizeFrac2_5) + "   " + self.FuncionesExtra.centrar_fraccion(NumRes,SizeFrac3)
                Denominadores = self.FuncionesExtra.centrar_fraccion(DenomIzq,SizeFrac1) + "   " + self.FuncionesExtra.centrar_fraccion(DenomDer,SizeFrac2) + "   " + self.FuncionesExtra.centrar_fraccion(DenomRes,SizeFrac2_5) + "   " + self.FuncionesExtra.centrar_fraccion(DenomRes,SizeFrac3)
        
        #Title "A" es una abreviacion a decir "Aplica" por lo cual significa que estamos hablando de un titulo
        if (Title == "A"):
            #Mostramos visualmente nuestros Numeradores junto a una sangria
            print(" "*(10 + len(Str) - 2),f"| {Numeradores} | ",sep="")
            #Mostramos nuestros divisores y nuestro simbolo junto con una sangria que haga destacar 
            print("="*10,Str, "-"*SizeFrac1,f" {Sym} ", "-"*SizeFrac2," | " + "="*10,sep="")
            #Mostramos los Denominadores junto con una sangria para alinear nuestra fraccion
            print(" "*(10 + len(Str) - 2),f"| {Denominadores} | ",sep="")
        else:
            if (NumRes == "NA"):
                print(f"{Fore.BLUE}{Numeradores}")
                print("-"*SizeFrac1, Fore.RED,f" {Sym} ", Fore.BLUE, "-"*SizeFrac2,sep="")
                print(f"{Denominadores}{Style.RESET_ALL}\n")
            else:
                #Si NumRes es distinto de "NA" significa que vamos a mostrar el resultado de operar una fraccion
                if (NumOp == "NA"):
                    print(f"{Fore.BLUE}{Numeradores}")
                    print("-"*SizeFrac1, Fore.RED,f" {Sym} ", Fore.BLUE, "-"*SizeFrac2 , Fore.RED," = ", Fore.BLUE,"-"*SizeFrac3 ,sep="")
                    print(f"{Denominadores}{Style.RESET_ALL}\n")
                else:
                    print(f"{Fore.BLUE}{Numeradores}",sep="")
                    print("-"*SizeFrac1, Fore.RED,f" {Sym} ", Fore.BLUE, "-"*SizeFrac2 , Fore.RED," = ", Fore.BLUE,"-"*SizeFrac2_5, Fore.RED," = ", Fore.BLUE,"-"*SizeFrac3 ,sep="")
                    print(f"{Denominadores}{Style.RESET_ALL}\n")
    
    def operar(self, Token: list, Posicion: int, Ver: str) -> list:
        """Opera las expresiones usando las reglas de los fraccionarios (Usando regla de la carita feliz, Ley de la oreja etc)"""
        
        #Creamos variables que almacenaran las fracciones a operar y nuestro simbolo
        Fracciones = Token[Posicion - 1] + Token[Posicion] + Token[Posicion + 1]
        FracIzq = find(r'-?\d*\.\d+|-?\d+|\/',Token[Posicion - 1])
        FracDer = find(r'-?\d*\.\d+|-?\d+|\/',Token[Posicion + 1])
        Sym = Token[Posicion]
        
        #Convertimos nuestras posiciones de tipo de string a valores enteros/decimales para poder operarlos
        NumeDer = self.convertir_valor(FracDer[0])
        DenomDer = self.convertir_valor(FracDer[2])
        NumeIzq = self.convertir_valor(FracIzq[0])
        DenomIzq = self.convertir_valor(FracIzq[2])
        
        #Mostramos al usuario lo que operaremos
        if(Ver == "SI"):
            print(f"{Fore.BLUE}{Style.BRIGHT}")
            self.mostrar_fraccion(NumeDer,DenomDer,NumeIzq,DenomIzq,Sym,OpTxt=Fracciones)
            print(f"{Style.RESET_ALL}")
        
        #Dependiendo de el tipo de operacion operamos de distinta manera
        if (Sym == "+" or Sym == "-"):
            #Si es una operacion con simbolo "+" o "-" usamos regla de la carita feliz
            if (DenomIzq != DenomDer):
                Nume1 = NumeIzq * DenomDer
                Nume2 = NumeDer * DenomIzq
                Denom = DenomIzq * DenomDer
            else:
                #Si nuestras fracciones tienen mismo denominador nos saltamos el paso de carita feliz y dejamos el denominador solo operamos numeradores
                Nume1 = NumeIzq
                Nume2 = NumeDer
                Denom = DenomDer
            
            #Segun sea nuestro simbolo suma o resta despues de haber hecho regla de la carita feliz operamos nuestros numeradores
            if (Sym == "+"):
                Nume = Nume1 + Nume2
            if (Sym == "-"):
                Nume = Nume1 - Nume2
            
            #Mostramos al usuario el paso a paso de nuestra operacion
            if(Ver == "SI"):
                NumOp = str(Nume1) + f" {Sym} " + str(Nume2)
                self.mostrar_fraccion(NumeDer,DenomDer,NumeIzq,DenomIzq,Sym,Title="NA",NumRes=Nume,DenomRes=Denom,NumOp=NumOp)
        elif(Sym == "*"):
            #Si nuestra operacion es una multiplicacion de fracciones operamos directo
            Nume = NumeIzq * NumeDer
            Denom = DenomIzq * DenomDer
        elif(Sym == "/"):
            #Si nuestra operacion es una division de fracciones usamos ley de la oreja
            Nume = NumeIzq * DenomDer
            Denom = NumeDer * DenomIzq
        
        #Si nuestra operacion fue una multiplicacion o division mostramos al usuario como operamos
        if (Sym != "+" and Sym != "-"):
            if(Ver == "SI"):
                self.mostrar_fraccion(NumeDer,DenomDer,NumeIzq,DenomIzq,Sym,Title="NA",NumRes=Nume,DenomRes=Denom)
        
        #Comprobamos que no hallan decimales en nuestra fraccion resultante
        if ("." in str(Nume) or "." in str(Denom)):
            #Comprobamos que el decimal de nuestro numerador y denominador no sea .0
            Denom = self.FuncionesExtra.comprobar_decimal_igual_a_cero(str(Denom))
            Nume = self.FuncionesExtra.comprobar_decimal_igual_a_cero(str(Nume))
            #Almacenamos nuestra fraccion resultante en una variable
            Frac = Nume + "/" + Denom
        else:
            #Sacamos el Maximo Comun Divisor
            Frac = self.simplificar_con_MCD(Nume,Denom,Ver)
        
        #Mostramos el resultado de lo operado
        if(Ver == "SI"):
            print(f"{Fore.BLUE}Resultado: {Fore.RED}{Frac}{Fore.RESET}\n")
        
        #Actualizamos nuestra expresion
        Token[Posicion - 1] = Frac
        Token.pop(Posicion + 1)
        Token.pop(Posicion)

        #Retornamos nuestra expresion actualizada
        return Token
    
    def mostrar_ecuacion(self, Token: list | str, Parentesis: str = "NO") -> None:
        return super().mostrar_ecuacion(Token,Parentesis=Parentesis)
    
    def evaluar(self, Expresion: str, VPrioridad: str, VProcedimiento: str, VerRespuesta: str) -> str:
        """Este metodo se encarga de evaluar toda la expresion y encontrar la respuesta organizando el flujo por el cual
        pasara la expresion para ser resuelta (Este metodo sera el que abarque todos los demas de la clase segun sea necesario)
        """
        #Definimos variables generales
        VPrioridad = VPrioridad.upper()
        VProcedimiento = VProcedimiento.upper()
        Ecuacion = Expresion
        
        #Mostramos al usuario lo la expresion que nos entrego
        if VProcedimiento.upper() == "SI":
            print(Fore.RED + Style.BRIGHT,"\n\n","="*25,f"|  EXPRESION:{Expresion}  |","="*25,Style.RESET_ALL,"\n\n\n",sep="")
        
        #Tokenizamos nuestra expresion
        Token = self.tokenizar(Expresion,VProcedimiento)
        
        #Si hay parentesis en nuestra ecuacion los simplificamos
        if ("(" in Ecuacion):
            Token = self.simplificar_parentesis(Token,VProcedimiento,VPrioridad)
        else:
            if (VProcedimiento == "SI"):
                self.mostrar_ecuacion(Token)
        
        #Simplificamos toda nuestra expresion
        while len(Token) > 1:
            PrioridadPOS = self.prioridad_a_operar(Token,VPrioridad)
            Token = self.operar(Token,PrioridadPOS,VProcedimiento)
            if (VProcedimiento == "SI"):
                self.mostrar_ecuacion(Token)
            Token = self.tokenizar(Token,VProcedimiento)
        
        #Hacemos que nuestra fraccion resultado pasea a ser un numero (Entero/Decimal)
        Respuesta = "SI"
        if (Respuesta.upper() == "SI"):
            Token = EvaluarExpresion.tokenizar(self,Token)
            Token = EvaluarExpresion.operar(self,Token,1,VProcedimiento)
            Token = EvaluarExpresion.tokenizar(self,Token)
        
        #Si nuestro resultado es un valor decimal entonces redondeamos a 13
        if ("." in Token[0]):
            Temp = self.convertir_valor(Token[0])
            ResultadoAprox = str(round(Temp,13))
        else:
            ResultadoAprox = None
        
        #Mostramos al usuario el resultado de nuestra expresion
        if (VerRespuesta.upper() == "SI"):
            if (ResultadoAprox == Token[0] or ResultadoAprox == None):
                print(f"{Fore.RED + Style.BRIGHT}\n(Usando fracciones) Su resultado de la ecuacion '{Ecuacion}' = {Fore.MAGENTA}{Token[0]}\n{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED + Style.BRIGHT}\n(Usando fracciones) Su resultado de la ecuacion '{Ecuacion}' = {Fore.MAGENTA}{Token[0]}{Fore.RED} ≈ {Fore.MAGENTA}{ResultadoAprox}\n{Style.RESET_ALL}")
        
        #Retornamos nuestro resultado
        if (ResultadoAprox != None):
            return str(ResultadoAprox)
        else:
            return str(Token[0])

class EvaluarPotencias(EvaluarExpresion):
    def __init__(self, Expresion:str, VerProcedimiento:str, VerPrioridad:str = "NO", VerRespuesta:str = "SI") -> None:
            self.comprobar_expresion_valida(Expresion)
            self.respuesta = self.evaluar(Expresion,VerPrioridad,VerProcedimiento,VerRespuesta)

    def convertir_valor(self, valor):
        return super().convertir_valor(valor)
    
    class FuncionesExtra:
        
        def convertir_notacion_a_decimal(Valor):
            return EvaluarExpresion.FuncionesExtra.convertir_notacion_a_decimal(Valor)
        
        def separar_base_de_exponente(Entry):
            return find(r'-?\d*\.\d+|-?\d+|\^',Entry)
        
        def convertir_lista_a_string(Entry: str | list):
            return EvaluarExpresion.FuncionesExtra.convertir_lista_a_string(Entry)

    def tokenizar(self, Expresion: list | str):
        
        Expresion = self.FuncionesExtra.convertir_lista_a_string(Expresion)
        
        Contador = Expresion.count("^")
        
        Token = find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\^',Expresion)
        
        for i in range(Contador):
            
            Pos = Token.index("^")
            
            Token[Pos] += Token[Pos + 1]; Token.pop(Pos + 1)
            Token[Pos - 1] += Token[Pos]; Token.pop(Pos)
        
        return Token    

    def mostrar_ecuacion(self, Token: list | str, Parentesis: str = "NO") -> None:
        return super().mostrar_ecuacion(Token, Parentesis)
    
    def comprobar_expresion_valida(self, Expresion: str) -> None:
        return super().comprobar_expresion_valida(Expresion)

    def prioridad_a_operar(self, Token: list, Ver: str) -> int:
        
        Pos = None
        
        if "/" in Token or "*" in Token:
            
            if "*" in Token:
                Posicion = Token.index("*")
            elif "/" in Token:
                Posicion = Token.index("/")
            
            PotenciaIzq = self.FuncionesExtra.separar_base_de_exponente(Token[Posicion - 1])
            PotenciaDer = self.FuncionesExtra.separar_base_de_exponente(Token[Posicion + 1])

            
            if (PotenciaIzq[0] == PotenciaDer[0]):
                Pos = Posicion
        if Pos == None:
            for i in range(len(Token)):
                if "^" in Token[i]:
                    Pos = i
                    break
        
        return Pos
    
    def operar(self, Expresion:list, Posicion:int, Ver:str):
        
        def potenciar(Expresion:list, Posicion:int, Ver:str):
            if Ver == "SI":
                print(f"\n{Fore.BLUE}{Style.BRIGHT}","="*10," ( ","Potenciamos:",Expresion[Posicion]," ) ","="*10,f"\n{Style.RESET_ALL}",sep="")
            
            if (Expresion[Posicion] == "*" or Expresion[Posicion] == "/"):
                Operar = self.FuncionesExtra.separar_base_de_exponente(Expresion[Posicion - 1])
            else:
                Operar = self.FuncionesExtra.separar_base_de_exponente(Expresion[Posicion])
            
            Respuesta = pow(self.convertir_valor(Operar[0]),self.convertir_valor(Operar[2]))
            
            if "." in str(Respuesta):
                if "e" in str(Respuesta):
                    Temp = str(format(Respuesta, '.13f'))
                else:
                    Temp = Respuesta
                    Temp = str(round(Temp,13))
                
                Respuesta = Temp
            else:
                Temp = self.FuncionesExtra.convertir_notacion_a_decimal(Respuesta)
                
                Respuesta = Temp
            
            Respuesta = str(Respuesta)
            Temp = str(Temp)
            
            if "." in Respuesta:
                if Respuesta.endswith("0"):
                    Respuesta = Respuesta.rstrip("0")
                    Temp = Temp.rstrip("0")
                
            if Ver == "SI":
                if Temp != Respuesta:
                    print(f"{Fore.BLUE}{Operar[0]}{Fore.RED}^{Fore.BLUE}{Operar[2]}{Fore.RED} = {Fore.BLUE}{Respuesta}{Fore.RED} ≈ {Fore.BLUE}{Temp}{Fore.RESET}\n")
                else:
                    print(f"{Fore.BLUE}{Operar[0]}{Fore.RED}^{Fore.BLUE}{Operar[2]}{Fore.RED} = {Fore.BLUE}{Respuesta}{Fore.RESET}\n")
                
            Expresion[Posicion] = Respuesta
            
            return Expresion
        
        def producto_o_cociente(Expresion:list, Posicion:int, Ver:str):
            PotenciaIzq = self.FuncionesExtra.separar_base_de_exponente(Expresion[Posicion - 1])
            PotenciaDer = self.FuncionesExtra.separar_base_de_exponente(Expresion[Posicion + 1])
            
            if Ver == "SI":
                print(f"{Fore.BLUE}En la expresion: {Expresion[Posicion - 1]}{Fore.RED} {Expresion[Posicion]} {Fore.BLUE}{Expresion[Posicion + 1]}",end=" ")
            
            if Expresion[Posicion] == "*":
                if Ver == "SI":
                    print(f"Sumamos los exponentes: {PotenciaIzq[2]} {Fore.RED}+{Fore.BLUE} {PotenciaDer[2]}{Fore.RESET}")
                Expresion[Posicion - 1] = PotenciaIzq[0] + "^" + str(self.convertir_valor(PotenciaIzq[2]) + self.convertir_valor(PotenciaDer[2]))
            elif Expresion[Posicion] == "/":
                if Ver == "SI":
                    print(f"Restamos los exponentes: {PotenciaIzq[2]} {Fore.RED}-{Fore.BLUE} {PotenciaDer[2]}{Fore.RESET}")
                Expresion[Posicion - 1] = PotenciaIzq[0] + "^" + str(self.convertir_valor(PotenciaIzq[2]) - self.convertir_valor(PotenciaDer[2]))

            Expresion.pop(Posicion + 1); Expresion.pop(Posicion)
            
            return Expresion
            
        if Expresion[Posicion] == "*" or Expresion[Posicion] == "/":
            return producto_o_cociente(Expresion,Posicion,Ver)
        else:
            return potenciar(Expresion,Posicion,Ver)
    
    def evaluar(self, Expresion:str, VerPrioridad:str, VerProcedimiento:str, VerRespuesta:str):
        
        VerProcedimiento = VerProcedimiento.upper(); VerPrioridad = VerPrioridad.upper(); VerRespuesta = VerRespuesta.upper()
        
        if VerProcedimiento == "SI":
            self.mostrar_ecuacion(Expresion)
        
        Token = self.tokenizar(Expresion)
        Continue = False
        PrioridadPos = self.prioridad_a_operar(Token,VerPrioridad)
        Token = self.operar(Token,PrioridadPos,VerProcedimiento)
        
        while True:
            for i in range(len(Token)):
                if "^" in Token[i]:
                    Continue = True
                else:
                    if not Continue:
                        Continue = False
            
            if Continue:
                if (VerProcedimiento == "SI"):
                    self.mostrar_ecuacion(Token)
                Token = self.tokenizar(Token)
                PrioridadPos = self.prioridad_a_operar(Token,VerPrioridad)
                Token = self.operar(Token,PrioridadPos,VerProcedimiento)
                Continue = False
            else:
                break
        
        Solution = "".join(map(str,Token))
        
        if VerRespuesta == "SI":
            print(f"{Fore.RED + Style.BRIGHT}\nSu resultado de la ecuacion '{Expresion}' ={Fore.MAGENTA} {Solution}\n{Style.RESET_ALL}")
        
        return Token

def main():
    print("¿Que desea realizar?:\n","\t(1) Evaluar operacion","\t(2) Evaluar fraccion\n",sep="\n")
    while True:
        try:
            seleccion = int(input("Ingrese el numero de la operacion que desea realizar: "))
            if seleccion == 2 or seleccion == 1:
                break
            else:
                print("\nError. Ingrese una de las opciones indicadas\n")
        except:
            print("\nError. Ingrese un numero entero\n")
    expresion = input("Ingrese la expresion que quiere operar: ")
    if " " in expresion:
        expresion = "".join(map(str,find(r'-?\d*\.\d+|-?\d+|\+|\-|\*|\/|\(|\)',expresion)))
    while True:
        Procedimiento = input("¿Desea ver el procedimiento? (Si/No): ").upper()
        if Procedimiento == "SI" or Procedimiento == "NO":
            break
        else:
            print("Error. Ingrese solo 'si' o 'no'")
    if seleccion == 1:
        Evaluar = EvaluarExpresion(expresion,Procedimiento)
    elif seleccion == 2:
        Evaluar = EvaluarFraccionarios(expresion,Procedimiento)

if __name__ == "__main__":
    main()