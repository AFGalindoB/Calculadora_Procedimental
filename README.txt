# Calculadora Procedimental en Python

## Descripción

Esta es una calculadora procedimental desarrollada en Python que evalúa expresiones matemáticas siguiendo la jerarquía de operaciones (BODMAS/PEDMAS), 
incluyendo la gestión de operaciones con:

 - Paréntesis
 - Suma
 - Resta
 - Multiplicación
 - División
 - Potencias (en desarrollo)
 - Raices (proximamente)

El objetivo es proporcionar una evaluación clara de las expresiones matemáticas con la opción de ver el procedimiento completo y las prioridades en la expresión.

## Características

- **Evaluación de Expresiones Matemáticas:** Evalúa expresiones con las operaciones básicas y avanzadas.
- **Jerarquía de Operaciones (BODMAS/PEDMAS):** Sigue el orden estándar de operaciones.
- **Ver Prioridades:** Puedes ver cómo se resuelve la expresión con base en las prioridades de las operaciones.
- **Ver Procedimiento:** La opción de ver el procedimiento paso a paso de la evaluación.
- **Manejo de Decimales:** Compatible con operaciones que involucren números decimales.
- **Manejo de Potencias:** Se están desarrollando características para el manejo de potencias.
- **Compatibilidad con Fracciones:** Usa `EvaluarFraccionarios` para realizar operaciones con fracciones.

## Uso

Para usar la calculadora, debes llamar a la clase `EvaluarExpresion` con los siguientes parámetros:

- **Expresion:** La expresión matemática a evaluar.
- **VerPrioridad:** Especifica si quieres ver las prioridades en la expresión. Debe ser "Sí" o "No".
- **VerProcedimiento:** Especifica si quieres ver el procedimiento paso a paso. Debe ser "Sí" o "No".
- **VerRespuesta:** Si no deseas ver la respuesta final, puedes establecer este argumento en "No". Si no se especifica, por defecto se mostrará.

### Ejemplo de Uso

Para usar la calculadora tienes 2 opciones

- **Primera Opción:** Ejecutar el archivo Evaluar.py desde tu terminal. Al iniciar, se ejecutará la función main(), la cual te pedirá que elijas 
entre evaluar una operación matemática normal o una fracción.

 1) Al ejecutar el archivo, verás el siguiente menú:

	"""¿Qué desea realizar?:
		(1) Evaluar operación
		(2) Evaluar fracción
	   Ingrese el numero de la operacion que desea realizar: 
	"""

 2) Elige la opción correspondiente ingresando 1 para operaciones normales o 2 para fracciones.

 3) A continuación, te pedirá ingresar la expresión que deseas evaluar. Puedes escribirla sin espacios, por ejemplo: 3+5*(2-8).

 4) Luego, se te preguntará si deseas ver el procedimiento paso a paso. Debes responder con "Si" o "No".

 5) Dependiendo de tu selección, se evaluará la expresión usando la clase adecuada:
    - EvaluarExpresion: Para evaluar expresiones matemáticas normales.
    - EvaluarFraccionarios: Para evaluar expresiones con fracciones.

- **Segunda Opcion:** Si deseas tener mas control sobre como quieres ingresar tus datos puedes seguir la siguente estructura:

	# Importar la clase desde el archivo
	from Evaluar import EvaluarExpresion, EvaluarFraccionarios

	# Crear una instancia de la clase EvaluarExpresion o EvaluarFraccionarios "Para ambas clases el ingreso de los datos es el mismo"
	resultado = EvaluarExpresion(
	    Expresion="3 + 5 * (2 - 8)",
	    VerProcedimiento="Sí",
	    VerPrioridad="Sí",
	    VerRespuesta="Sí"
	)

- **Tercera Opcion:**  Si prefieres el uso de una interfaz grafica puedes ejecutar el archivo App.py desde tu terminal
    - Se desplegara una interfaz en la cual te preguntara que deseas hacer
    - Pulsa el boton Calculadora Basica en la cual se te desplegara otra ventana de una calculadora
	- Usa la calculadora como usarias otra calculadora ingresando tu expresion matematica
	- Si deseas ver el procedimiento en la calculadora pulsa el boton 'PRO'
	- Se desplegara otra ventana en la cual te mostrara el procedimiento de la ecuacion

### Archivos Extra

 - Probar_Calculadora.py

  El archivo Probar_Calculadora.py es un archivo el cual comprueba el funcionamiento de la calculadora usando 2 diccionarios donde el primero
  tiene expresiones matematicas con variaciones tanto en el orden de simbolos, un agregado de parentesis en distintas formas y una representacion
  distinta de los numeros aveces teniendo numeros enteros como decimales. El segundo diccionario almacena las respuestas esperadas de cada expresion matematica,
  mas adelante en el codigo se comprueba si la respuesta entregada por la calculadora es la misma respuesta esperada y en caso de que todas las expresiones
  sean operadas correctamente la terminal de python mostrara en pantalla un mensaje con esta estructura:

	===================================================
	Todas las expresiones fueron operadas correctamente
	===================================================

  En caso de que alguna respuesta entregada por la calculadora no sea la respuesta esperada la terminal mostrara un mensaje de error. Ejemplo:

	Operaciones con Exponentes (Regla del Cociente con bases iguales):

	Expresion: '-4^3/-4^-4' Espera: -6384 != Respuesta: -16384

  Si deseas modificar el codigo y quieres comprobar si tus cambios generados en el codigo funcionan, puedes usar este archivo como una ayuda para probar la calculadora
  y verificar que la misma funcione de manera optima. A su vez si deseas agregar funcionalidades o quieres agregar una nueva ecuacion de prueba con su
  respectiva respuesta esperada puedes modificar los diccionarios "Expresiones" y "Respuestas" teniendo en cuenta la siguente estructura
 
  Estructura:	

	Nombre del diccionario:      =       {"Op + Numero_entero": ["Tu expresion/Respuesta"] }

  Ejemplo:	 

	Expresiones                  =       {"Op8":["5*-(3+(4-5*6))/2"]}

   + Aviso:

    En la linea 58 del codigo hay un condicional "if i < 8" el cual controla que solo se evaluen las Expresiones matematicas usando la clase
    EvaluarFraccionarios hasta la llave "Op7". Esto debido a que la clase EvaluarFraccionarios no se le han implementado el control de potencias
    Si tu llave "Op" es mayor a 7 solo se evaluara con la clase EvaluarExpresiones.

    En caso de que desees operar otras expresiones con la clase EvaluarFraccionarios elimina las claves "Op8" y "Op9" y elimina los respectivos valores de ambas claves
    a su vez quita el condicional "if i < 8" y las tabulaciones de las lineas de codigo que hay para el condicional

 - Ecuaciones_de_Prueba.txt
   
   El archivo Ecuaciones_de_Prueba.txt contiene las ecuaciones integradas en el archivo Probar_Calculadora.py con su respectivas respuestas,
   divididas por secciones y tipos de ecuaciones, al final de cada seccion se encuentran 2 formatos de listas de python las cuales almacenan tanto 
   la expresion como su respuesta esperadas, ordenadas de tal manera que los indices de cada respuesta esperada coinciden con el indice de la expresion matematica

### Instalación

 1) Clona este repositorio

	git clone https://github.com/AFGalindoB/Calculadora_Procedimental.git

 2) Navega al directorio del proyecto:
	
	cd Calculadora_Procedimental

 3) Si deseas usar la interfaz grafica primero instala la fuente ChillPixels-Maximal.otf

 4) Ejecuta o importa el archivo Python para utilizar la calculadora:
	
	python Evaluar.py #Para ejecutar el archivo Evaluar desde la terminal
	python App.py #Para ejecutar el archivo App desde la terminal
	import Evaluar #Para importar Evaluar en tu archivo de python

## Recomendaciones de Entorno

El uso de la biblioteca colorama añade soporte para colores en la salida del terminal. Se recomienda utilizar entornos o IDEs como Visual Studio Code, 
PyCharm, o terminales que soporten colores, como PowerShell o CMD en Windows. Si experimentas problemas con la visualización de colores, asegúrate de estar 
ejecutando el archivo en un entorno que lo soporte correctamente.

# Licencia
Este proyecto está licenciado bajo la Licencia Creative Commons Reconocimiento-No Comercial 4.0 Internacional


