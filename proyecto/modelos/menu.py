from typing import List 
from art import *
from .fuentes import *
from abc import ABC,abstractclassmethod

# Declaración de clase abstracta Menu
class Menu(ABC):
    '''
    Esta es una clase abstracta que obliga a las clases que la hereden a que tengan un metodo __str__ con el cual pueda mostrarse, tambien obliga a que tengan un metodo textoPorConsola(), actualmente las clases que heredan de esta son MenuConGrafo y MenuSinGrafo
    '''
    def __init__(self, opciones: List[str], titulo: str):
        self.opciones = opciones
        self.titulo = titulo 
        self.opcion = -1
    
    @abstractclassmethod
    def __str__(self):
        '''
        Este menu es abstracto ya que un menu puede mostrarse de otras aparte de la convencional que es:

        Titulo
        - Opciones

        Por ejemplo podría tener una variable con la que esté trabajando:

        Titulo
        Variable
        - Opciones

        un ejemplo de esto es:

        MENU DE FUNCIONES
        Funcion: x^2
        Opciones:
            - Eliminar
            - Modificar
            - Evaluar
        
        En el ejemplo anterior, la variable funcion sería un atributo que tengan o implemente la clase que herede de esta clase.
        '''
        pass

    @abstractclassmethod
    def textoPorConsola(self,fuente: str = FUENTE_NORMAL):
        '''
        #### DESCRIPCIÓN:
        Esta funcion está definida con el objetivo de agregar un estilo de fuente a la impresion por consola. 

        ---
        Las opciones de fuente disponibles especialmente establecidas para el menu son:\n
        FUENTE_NORMAL = 'normal'\n
        FUENTE_STANDARD = 'standard'\n
        FUENTE_CRICKET = 'cricket'\n
        FUENTE_CYBERLARGE = 'cyberlarge'\n
        FUENTE_DOOM = 'doom'\n

        ---
        Para obtener más fuentes disponibles utilizar la función  obtenerFuentesConsola del módulo 'fuentes' o de manera altenativa utilizar la librería art.

        ---
        #### Ejemplo con art, escribir en consola:

        pip install art\n
        python
        >>> from art import *
        >>> FONT_NAMES
        '''
        pass

    def pedirOpcion(self) -> None:
        '''
        Esta funcion pide ingresar un numero y a la vez retorna el numero ingresado. La utilidad de la función está en que anticipa errores como el ingreso de opciones que no existan en el menú.
        La opcion ingresada se guarda en el atributo "opcion" del objeto de esta clase.
        '''
        try:
            opcion = int(input("Seleccione una opción: "))
            if 0 <= opcion < len(self.opciones):
                self.opcion = opcion 
            else:
                print("Opción inválida. Inténtelo de nuevo. ", end="")
                self.pedirOpcion()
        except ValueError:
            print("Por favor, ingrese un número. ", end="")
            self.pedirOpcion()

# Declaración de clase MenuSinGrafo que elimina la abstraccion por parte de la clase abstracta Menu
class MenuSinGrafo(Menu):
    '''
    Esta clase es un menu que se utilizará especificamente en este proyecto para diferenciar entre los menús que no muestran un grafo con el que puedan trabajar, de los menús que sí lo hacen.

    En este caso, esta clase muestra un menu con la siguiente estructura:

    TITULO MENU
    - Opciones
    '''

    def __init__(self, opciones: List[str], titulo: str):
        super().__init__(opciones,titulo)

    def __str__(self):
        retorno = self.titulo + "\n\n"
        for i, opcion in enumerate(self.opciones):
            retorno += f'{i}. {opcion}\n'
        return retorno 

    def textoPorConsola(self,fuente: str = FUENTE_NORMAL):
        if fuente == FUENTE_NORMAL:
            return self.__str__()
        else:
            titulo = text2art(self.titulo,fuente)
            retorno = titulo + "\n\n"
            for i, opcion in enumerate(self.opciones):
                retorno += f'{i}. {opcion}\n'
            return retorno 
        
# Declaración de clase MenuConGrafo que elimina la abstraccion por parte de la clase Menu
class MenuConGrafo(Menu):
    '''
    Esta clase es un menu que se utilizará especificamente en este proyecto para diferenciar entre los menús que no muestran un grafo con el que puedan trabajar, de los menús que sí lo hacen.

    En este caso, esta clase muestra un menu con la siguiente estructura:

    TITULO MENU
    Nombre del Grafo: ()
    - Opciones
    '''

    def __init__(self, opciones: List[str], titulo: str, nombreGrafo: str = 'grafo1'):
        super().__init__(opciones,titulo)
        self.nombreGrafo = nombreGrafo

    def __str__(self):
        retorno = f'{self.titulo}\n\nNombre del grafo: {self.nombreGrafo}\n\n'
        for i, opcion in enumerate(self.opciones):
            retorno += f'{i}. {opcion}\n'
        return retorno 

    def textoPorConsola(self,fuente: str = FUENTE_NORMAL):
        if fuente == FUENTE_NORMAL:
            return self.__str__()
        else:
            titulo = text2art(self.titulo,fuente)
            retorno = f'{titulo}\n\nNombre del grafo: {self.nombreGrafo}\n\n'
            for i, opcion in enumerate(self.opciones):
                retorno += f'{i}. {opcion}\n'
            return retorno 