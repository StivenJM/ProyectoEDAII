from art import *
from typing import Dict, Union 

# Declaracion de variables de fuente constante
FUENTE_NORMAL = 'normal'
FUENTE_STANDARD = 'standard'
FUENTE_CRICKET = 'cricket'
FUENTE_CYBERLARGE = 'cyberlarge'
FUENTE_DOOM = 'doom'

def obtenerFuentesConsola(parametro: Union[str, None] = None) -> Dict[str,str]:
    '''
    DESCRIPCIÓN:
    Esta funcion por defecto retorna un diccionario que tiene nombreVariable: valorVariable

    PARÁMETROS DE LA FUNCION:
    * None: El parametro por defecto es None (usado para retornar un numero limitado de variables)
    * 'a': La funcion tambien puede tomar el valor de a (proviene de all) para retornar todas las fuentes posibles.
    '''
    if parametro == None:
        return {
            'FUENTE_NORMAL': 'normal',
            'FUENTE_STANDARD': 'standard',
            'FUENTE_CRICKET': 'cricket',
            'FUENTE_CYBERLARGE': 'cyberlarge',
            'FUENTE_DOOM': 'doom'
        }
    elif parametro == 'a':
        return dict(enumerate(FONT_NAMES))

