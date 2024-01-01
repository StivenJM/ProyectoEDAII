from typing import Dict, Any 

class Arista():
    def __init__(self, identificador: int, a: int, b: int):
        self.identificador = identificador
        self.a = a 
        self.b = b 
    
    def __str__(self):
        return f'({self.a},{self.b})'
    
    def __repr__(self):
        return f'Arista({self.identificador}, {self.a}, {self.b})'
    
    def __eq__(self, otraArista: 'Arista') -> bool:
        return type(self) == type(otraArista) and self.identificador == otraArista.identificador
    
    def __ne__(self, otraArista: 'Arista') -> bool:
        return type(self) != type(otraArista) or self.identificador != otraArista.identificador
    
    def __hash__(self) -> int:
        return hash((self.identificador, 'Arista'))
    
    def to_dict(self) -> Dict[str, Any]:
        '''
        Devuelve el objeto de Arista como un diccionario.
        '''
        return {
            'identificador': self.identificador,
            'a': self.a,
            'b': self.b
        }