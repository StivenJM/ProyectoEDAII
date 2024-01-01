from typing import Union, overload, List, Dict, Any 

class Nodo:

    def __init__(self, identificador: int = 0, contenido: Any = None):
        '''
        ---
        Descripción:
        ---
        Inicializa una nueva instancia de Nodo. Se puede inicializar sin argumentos, con un argumento de identificador, con un argumento de contenido o con ambos argumentos.

        ---
        Args
        ---
            - identificador: Es un identificador único del nodo, si no se pone nada el identificador por defecto siempre es 0.
            - contenido: Es el contenido que lleva el nodo, puede tener el contenido que quiera. Por defecto no tiene nada.

        ---
        Ejemplos:
        ---

        >>> nodo1 = Nodo() 
        Nodo(0, None)
        >>> nodo1 = Nodo(2) 
        Nodo(2, None)
        >>> Nodo('Hola mundo') 
        Nodo(0, Hola mundo)
        >>> Nodo(3,'Programa en python!') 
        Nodo(3, Programa en python!)

        Un caso especial es cuando no se quiere darle un identificador al nodo pero se quiere tener un contenido numérico, en ese caso se utiliza directamente la keyword de contenido.

        >>> Nodo(contenido=4)
        Nodo(0, 4)
        '''
        self.contenido = contenido
        self.vecinos: List['Nodo'] = [] # Lista de nodos conectados o vecinos
        if type(identificador) == int:
            self.identificador =  identificador 
        else:
            if contenido == None:
                self.contenido = identificador # Porque identificador tiene otro tipo de dato
            self.identificador = 0

    
    def __str__(self) -> str:
        return f'Nodo({self.identificador}, {self.contenido})'
    
    def __repr__(self) -> str:
        return f'Nodo({self.identificador}, {self.contenido})'
    
    def __eq__(self, otroNodo: 'Nodo') -> bool:
        return type(self) == type(otroNodo) and self.identificador == otroNodo.identificador
    
    def __ne__(self, otroNodo: 'Nodo') -> bool:
        return type(self) != type(otroNodo) or self.identificador != otroNodo.identificador
    
    def __hash__(self) -> int:
        return hash((self.identificador, 'Nodo'))
    
    def to_dict(self) -> Dict[str, Any]:
        '''
        Devuelve el objeto de Nodo como un diccionario.
        '''
        return {
            'identificador': self.identificador,
            'contenido': self.contenido
        }
    
    def agregarVecino(self,n: 'Nodo'):
        self.vecinos.append(n)
    
    @overload
    def eliminarVecino(self, idNodo: int) -> int: ...
    @overload
    def eliminarVecino(self, nodo: 'Nodo') -> int: ...

    def eliminarVecino(self, arg: Union['Nodo', int]) -> int:
        '''
        Elimina la conexión que tiene el nodo con su vecino. Es importante recalcar que no elimina el nodo vecino, sino la conexión que tiene con este.

        Args:
            - n: Es el identificador del nodo vecino que se quiere eliminar. Tambien puede ser el objeto directo de tipo Nodo.
        
        Returns:
            - 1: Si eliminó el vecino con el identificador proporcionado
            - 0: Si no encontró ni pudo eliminar el vecino
        '''
        if type(arg) == type(self):
            # Si el argumento es un nodo
            if arg in self.vecinos:
                self.vecinos.remove(arg)
                return 1
            
        elif type(arg) == int:
            # Si el argumento es un identificador
            for nodo in self.vecinos:
                if arg == nodo.identificador:
                    self.vecinos.remove(nodo)
                    return 1
        return 0 # Si no se encontro ni se puedo eliminar el vecino

    
    def obtenerInformacion(self) -> str:
        return f'Identificador: {self.identificador} \nContenido: {self.contenido} \nVecinos: {self.vecinos}'

    
