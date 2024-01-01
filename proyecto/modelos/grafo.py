from abc import ABC, abstractclassmethod
from typing import List, overload, Union, Dict, Any 
from .nodo import Nodo 
from .arista import Arista 

class Grafo(ABC):
    def __init__(self):
        self.nodos: List['Nodo'] = []
        self.aristas: List['Arista'] = []

    def __str__(self) -> str:
        retorno = ""
        for n in self.nodos:
            # La forma en la que se van a ver los grafos por defecto es esta
            '''
            Nodo(identificador,contenido) -> [idNodoVecino1, idNodoVecino2, idNodoVecino3, idNodoVecino4, ...]
            Nodo(1, 'Hola mundo') -> [2, 4, 5, 1]
            Nodo(3, None) -> []
            Nodo(5, 'Python') -> [2, 1]
            '''
            retorno += f'{n} -> {[i.identificador for i in n.vecinos]}\n'
        return retorno
    
    def to_dict(self) -> Dict[str, Any]:
        '''
        Devuelve el objeto de Grafo como un diccionario.
        '''
        return {
            'dirigido': self.esDirigido(),
            'nodos': [nodo.to_dict() for nodo in self.nodos],
            'aristas': [arista.to_dict() for arista in self.aristas]
        }
    
    def _obtenerIdAristaDisponible(self) -> int:
        '''
        Esta funcion devuelve un entero que corresponde a un id que no existe dentro del grafo. Es util para crear nuevas aristas sin interferir con la implementacion del grafo.
        '''
        idsAristas = [arista.identificador for arista in self.aristas] + [0]

        idmin = min(idsAristas)
        idmax = max(idsAristas)

        # Busca si existe algun espacio disponible en el rango de ids
        for i in range(idmin,idmax):
            if not i in idsAristas:
                return i 
            
        return idmax+1
    
    def _obtenerIdNodoDisponible(self) -> int:
        '''
        Esta funcion devuelve un entero que corresponde a un id que no existe dentro del grafo. Es util para crear nuevos nodos sin interferir con la implementacion del grafo.
        '''
        idsNodos = [nodo.identificador for nodo in self.nodos] + [0]

        idmin = min(idsNodos)
        idmax = max(idsNodos)

        # Busca si existe algun espacio disponible en el rango de ids
        for i in range(idmin,idmax):
            if not i in idsNodos:
                return i 
            
        return idmax+1

    def _nodosExisten(self, idsNodo: List[int]) -> bool:
        '''
        ---
        Esta función ayuda a determinar si un conjunto de nodos existen en el grafo o no.

        Args:
            - idsNodo: Hace referencia a identificadores de nodos, es una lista de identificadores enteros de nodos de la clase Nodo. Ej: [id1, id2, id3, ...].
        
        Returns:
            - True: Si todos los elementos pertenecen al grafo
            - False: Si al menos 1 elemento no pertenece al grafo
        '''
        nodosExistentes = [n.identificador for n in self.nodos] # Lista de los ids de todos los nodos
        for i in idsNodo:
            if not i in nodosExistentes:
                return False 
        return True 
    
    def _buscarNodo(self, idNodo: int) -> int:
        '''
        Esta función busca un nodo en la lista de nodos del grafo llamada "nodos".

        Args:
            - idNodo: Hace referencia al identificador entero de un nodo de la clase Nodo.
        
        Returns:
            - int: Devuelve un entero mayor o igual a cero correspondiente a la posicion de la lista "nodos" perteneciente al grafo
            - -1: Devuelve este valor si no encontró el nodo
        '''
        for i,n in enumerate(self.nodos):
            if n.identificador == idNodo:
                return i 
        return -1

    @abstractclassmethod
    def _buscarArista(self, *args, **kwargs) -> int:
        pass 

    def _buscarAristasConNodo(self, idNodo: int) -> List[int]:
        '''
        Busca las aristas que se relacionan con el nodo pasado como parametro.

        Args:
            - idNodo: identificador del nodo.
        
        Returns:
            - List[int]: retorna una lista de enteros que corresponden a las posiciones de las aristas del grafo que se relacionan con nodo.
        '''
        return [i for i,arista in enumerate(self.aristas) if arista.a == idNodo or arista.b == idNodo]

    def obtenerNodoPorId(self, idNodo: int) -> Union['Nodo',int]:
        '''
        ---
        Esta funcion devuelve un objeto nodo del grafo.

        Args:
        - idNodo: es el identificador del nodo que se quiere obtener del grafo.

        Returns:
        - Nodo: Devuelve un objeto de tipo nodo con el id proporcionado.
        - -1: Si no encontró el nodo devuelve -1.
        '''
        posicionNodoEnGrafo = self._buscarNodo(idNodo)
        return self.nodos[posicionNodoEnGrafo] if posicionNodoEnGrafo>=0 else -1



    @abstractclassmethod
    def esDirigido(self) -> bool:
        pass 
    
    def agregarNodo(self, nodo: 'Nodo'):
        if self._nodosExisten([nodo.identificador]):
            nuevoId = self._obtenerIdNodoDisponible()
            nodo.identificador = nuevoId 
        self.nodos.append(nodo)
    
    @abstractclassmethod
    def agregarArista(self, *args, **kwargs):
        pass

    @abstractclassmethod
    def eliminarNodo(self, idNodo: int) -> int:
        '''
        Esta funcion elimina el nodo especificado en el grafo, junto con eso se eliminan tambien todas las aristas que estaban conectadas a ese nodo.

        Args:
            - idNodo: Es el identificador del nodo que se quiere eliminar.
        
        Returns:
            - 1: Si el nodo se eliminó exitosamente.
            - 0: Si no se encontró ni se eliminó el nodo.
        '''
        pass
    
    @abstractclassmethod
    def eliminarArista(self, *args, **kwargs):
        pass





class GrafoDirigido(Grafo):
    '''
    ---
    Grafo Dirigido
    ---
    Clase que representa un grafo dirigido. Hereda de la clase abstracta Grafo.

    ### Métodos:
        - obtenerPadresNodo: metodo estático
        - obtenerHijosNodo: metodo estático
        - obtenerIndegreeNodo: metodo estático
        - obtenerOutdegreeNodo: metodo estático
        - esDirigido
        - eliminarNodo
        - agregarArista
        - eliminarArista
    
    ### Métodos heredados de Grafo:
        - obtenerNodoPorId
        - agregarNodo
    '''
    def __init__(self):
        super().__init__()
    
    @overload
    def _buscarArista(self, nodoOrigen: int, nodoDestino: int) -> int: ...
    @overload
    def _buscarArista(self, idArista: int) -> int: ...

    def _buscarArista(self, *args, **kwargs) -> int:
        '''
        Busca la arista en el grafo.

        Args:
            - nodoOrigen: Es el identificador del nodoOrigen
            - nodoDestino: Es el identificador del nodoDestino

            - idArista: Es el identificador de la arista que se quiere buscar.
        
        Returns:
            - int: Devuelve un entero mayor o igual a cero correspondiente a la posicion de la lista "aristas" perteneciente al grafo
            - -1: Devuelve este valor si no encontró la arista
        '''
        if len(args) == 1:
            # args[0] = idArista
            for i,a in enumerate(self.aristas):
                if a.identificador == args[0]:
                    return i 
            return -1
        elif len(args) == 2:
            # args[0] = nodoOrigen      args[1] = nodoDestino
            if self._nodosExisten([args[0],args[1]]):
                # Se filtran todas las aristas que son (nodoOrigen, nodoDestino)
                aristasEncontradas = [i for i,arista in enumerate(self.aristas) if arista.a == args[0] and arista.b == args[1]]
                if len(aristasEncontradas) != 0:
                    return aristasEncontradas[0]
                else:
                    return -1
            else:
                return -1
        return -1    

    @staticmethod
    def obtenerPadresNodo(idNodo: int, grafo: 'GrafoDirigido') -> List[int]:
        '''
        ---
        Descripción:
        ---
        En grafos dirigidos existe el concepto de nodos padres y nodos hijos, este metodo devuelve una lista de nodos padres teniendo como parametros al nodo y al grafo dirigido.

        ---
        Args:
        ---
        - idNodo: Es el identificador del nodo del cual se quiere saber sus padres.
        - grafo: Es un grafo dirigido de la clase GrafoDirigido

        ---
        Returns
        ---
        - List[int]: Devuelve una lista de enteros, cada entero representa un identificador de un nodo padre del idNodo pasado como parámetro.
        - []: Devuelve una lista vacía si no encuentra ningún padre para el nodo en cuestión.
        '''
        retorno = []
        for arista in grafo.aristas:
            if idNodo == arista.b:
                retorno.append(arista.a)
        return retorno 
    

    @staticmethod
    def obtenerHijosNodo(idNodo: int, grafo: 'GrafoDirigido') -> List[int]:
        '''
        ---
        Descripción:
        ---
        En grafos dirigidos existe el concepto de nodos padres y nodos hijos, este metodo devuelve una lista de nodos hijos teniendo como parametros al nodo y al grafo dirigido.

        ---
        Args:
        ---
        - idNodo: Es el identificador del nodo del cual se quiere saber sus hijos.
        - grafo: Es un grafo dirigido de la clase GrafoDirigido

        ---
        Returns
        ---
        - List[int]: Devuelve una lista de enteros, cada entero representa un identificador de un nodo hijo del idNodo pasado como parámetro.
        - []: Devuelve una lista vacía si no encuentra ningún hijo para el nodo en cuestión.
        '''
        retorno = []
        for arista in grafo.aristas:
            if idNodo == arista.a:
                retorno.append(arista.b)
        return retorno 
    
    @staticmethod
    def obtenerIndegreeNodo(idNodo: int, grafo: 'GrafoDirigido') -> int:
        '''
        ---
        Descripción:
        ---
        En grafos dirigidos existe el concepto indegree y outdegree, este metodo devuelve un numero entero correspondiente al indegree del nodo pasado como parametro.

        ---
        Args:
        ---
        - idNodo: Es el identificador del nodo del cual se quiere saber su indegree.
        - grafo: Es un grafo dirigido de la clase GrafoDirigido

        ---
        Returns
        ---
        - int: Devuelve enteros mayores o iguales a 0.
        '''
        padres = GrafoDirigido.obtenerPadresNodo(idNodo, grafo)
        return len(padres)
    
    
    @staticmethod
    def obtenerOutdegreeNodo(idNodo: int, grafo: 'GrafoDirigido') -> int:
        '''
        ---
        Descripción:
        ---
        En grafos dirigidos existe el concepto indegree y outdegree, este metodo devuelve un numero entero correspondiente al outdegree del nodo pasado como parametro.

        ---
        Args:
        ---
        - idNodo: Es el identificador del nodo del cual se quiere saber su outdegree.
        - grafo: Es un grafo dirigido de la clase GrafoDirigido

        ---
        Returns
        ---
        - int: Devuelve enteros mayores o iguales a 0.
        '''
        padres = GrafoDirigido.obtenerHijosNodo(idNodo, grafo)
        return len(padres)
    
    def esDirigido(self):
        return True
    
    def eliminarNodo(self, idNodo: int) -> int:
        '''
        Esta funcion elimina el nodo especificado en el grafo, junto con eso se eliminan tambien todas las aristas que estaban conectadas a ese nodo.

        Args:
            - idNodo: Es el identificador del nodo que se quiere eliminar.
        
        Returns:
            - 1: Si el nodo se eliminó exitosamente.
            - 0: Si no se encontró ni se eliminó el nodo.
        '''
        p = self._buscarNodo(idNodo) # p = posicion nodo en grafo
        if p == -1: # No se encontro un nodo con el id proporcionado
            return 0
        else:
            # padres es una lista de identificadores de los padres de idNodo
            idsPadres = GrafoDirigido.obtenerPadresNodo(idNodo,self)
            
            # Eliminar el nodo de sus padres
            for idPadre in idsPadres:
                padre = self.nodos[self._buscarNodo(idPadre)] # nodo padre con el id = idPadre
                padre.eliminarVecino(idNodo)
            
            # Eliminar aristas del grafo relacionadas con nodo
            posicionesAristas = self._buscarAristasConNodo(idNodo)
            posicionesAristas.sort(reverse=True) # Se ordenan los indices para evitar problemas al eliminar luego
            for pa in posicionesAristas:
                self.aristas.pop(pa)

            # Eliminar el nodo del grafo
            self.nodos.pop(p)

            return 1 # Se eliminó exitosamente

    def agregarArista(self, nodoOrigen: int, nodoDestino: int, idArista: int  = 0) -> int:
        '''
        Para agregar la arista en el grafo previamente deben existir los nodos correspondientes.

        Args:
            - nodoOrigen: Es el identificador del nodo de origen.
            - nodoDestino: Es el identificador del nodo de destino.

            - idArista: Es el identificador que se le quiera poner a la arista, por defecto es 0 pero si ya existe se escogerá uno automáticamente.

        Returns:
            - 1: Si se agregó la arista en el grafo exitosamente.
            - 0: Si no se puedo agregar la arista.
        '''
        try:
            
            if self._nodosExisten([nodoOrigen, nodoDestino]):

                nuevaArista = Arista(idArista, nodoOrigen, nodoDestino)

                if self._buscarArista(idArista) != -1:
                    nuevaArista.identificador = self._obtenerIdAristaDisponible()

                self.aristas.append(nuevaArista)  # Se agrega una arista al grafo
                pNodoOrigen = self._buscarNodo(nodoOrigen)      # Posicion del nodo de origen en el grafo
                pNodoDestino = self._buscarNodo(nodoDestino)    # Posicion del nodo de destino en el grafo
                self.nodos[pNodoOrigen].agregarVecino(self.nodos[pNodoDestino]) # Se agrega un vecino al nodoOrigen
                return 1
            else:
                return 0
        except Exception as e:
            print(f'Ocurrió un error: {e}.')
            return 0
    
    @overload
    def eliminarArista(self, nodoOrigen: int, nodoDestino: int) -> int: ...
    @overload
    def eliminarArista(self, idArista: int) -> int: ...

    def eliminarArista(self, *args, **kwargs) -> int:
        '''
        Elimina una arista del grafo.

        Args:
            nodoOrigen: Es el identificador del nodo de origen 
            nodoDestino: Es el identificador del nodo de destino

            idArista: Es el identificador único de la arista.
        
        Returns:
            1: Si eliminó la arista del grafo
            0: Si no se pudo eliminar nada
        '''
        try:

            # Se busca la posicion de la arista, si se le envia un parametro busca utilizando el identificador de la arista, por otro lado, si se le envian los nodos entonces buscará cualquier arista con esos nodos.
            posicionArista = self._buscarArista(args[0]) if len(args) == 1 else self._buscarArista(args[0], args[1])
            if posicionArista >= 0: # posicionArista es mayor o igual a 0 si se encontró realmente una posicion

                # En este bloque se busca aliminar el vecino del nodo origen
                arista = self.aristas[posicionArista]
                self.nodos[self._buscarNodo(arista.a)].eliminarVecino(arista.b)

                self.aristas.pop(posicionArista) # Se elimina la arista del grafo
                return 1
            return 0
            
        except Exception as e:
            print(f'Ocurrió un error: {e}')
            return 0  
        




class GrafoNoDirigido(Grafo):
    '''
    ---
    Grafo No Dirigido
    ---
    Clase que representa un grafo no dirigido. Hereda de la clase abstracta Grafo.

    ### Métodos:
        - esDirigido
        - eliminarNodo
        - agregarArista
        - eliminarArista
    
    ### Métodos heredados de Grafo:
        - obtenerNodoPorId
        - agregarNodo
    '''
    def __init__(self):
        super().__init__()

    @overload
    def _buscarArista(self, nodo1: int, nodo2: int) -> int: ...
    @overload
    def _buscarArista(self, idArista: int) -> int: ...

    def _buscarArista(self, *args, **kwargs) -> int:
        '''
        Busca la arista en el grafo.

        Args:
            - nodo1: Es el identificador del nodo1
            - nodo2: Es el identificador del nodo2

            - idArista: Es el identificador de la arista que se quiere buscar.
        
        Returns:
            - int: Devuelve un entero mayor o igual a cero correspondiente a la posicion de la lista "aristas" perteneciente al grafo
            - -1: Devuelve este valor si no encontró la arista
        '''
        if len(args) == 1:
            # args[0] = idArista
            for i,a in enumerate(self.aristas):
                if a.identificador == args[0]:
                    return i 
            return -1
        elif len(args) == 2:
            # args[0] = nodo1      args[1] = nodo2
            if self._nodosExisten([args[0],args[1]]):
                # Se filtran las posiciones de las aristas que son tanto (nodo1,nodo2) como (nodo2,nodo1)
                aristasEncontradas = [i for i,arista in enumerate(self.aristas) if (arista.a == args[0] and arista.b == args[1]) or (arista.a == args[1] and arista.b == args[0])]
                if len(aristasEncontradas) != 0:
                    return aristasEncontradas[0]
                
        return -1
    
    def esDirigido(self):
        return False
    
    def eliminarNodo(self, idNodo: int) -> bool:
        '''
        Esta funcion elimina el nodo especificado en el grafo, junto con eso se eliminan tambien todas las aristas que estaban conectadas a ese nodo.

        Args:
            - idNodo: Es el identificador del nodo que se quiere eliminar.
        
        Returns:
            - True: Si el nodo se eliminó exitosamente.
            - False: Si no se encontró ni se eliminó el nodo.
        '''
        p = self._buscarNodo(idNodo) # p = posicion nodo en grafo
        if p == -1: # No se encontro un nodo con el id proporcionado
            return False 
        else:
            vecinos = self.nodos[p].vecinos 
            
            # Eliminar el nodo de sus vecinos
            for v in vecinos:
                v.vecinos.remove(Nodo(idNodo))
            
            # Eliminar aristas del grafo relacionadas con nodo
            posicionesAristas = self._buscarAristasConNodo(idNodo)
            posicionesAristas.sort(reverse=True)
            for pa in posicionesAristas:
                self.aristas.pop(pa)

            # Eliminar el nodo del grafo
            self.nodos.pop(p)

            return True # Se eliminó exitosamente
    
    def agregarArista(self, nodo1: int, nodo2: int, idArista: int = 0) -> bool:
        '''
        Para agregar la arista en el grafo previamente deben existir los nodos correspondientes.

        Args:
            - nodo1: Es el identificador del nodo de origen.
            - nodo2: Es el identificador del nodo de destino.

            - idArista: Es el identificador que se le quiera poner a la arista, por defecto es None y se escogerá uno automáticamente.

        Returns:
            - True: Si se agregó la arista en el grafo exitosamente.
            - False: Si no se puedo agregar la arista.
        '''
        try:
            
            if self._nodosExisten([nodo1, nodo2]):

                nuevaArista = Arista(idArista, nodo1, nodo2)

                if self._buscarArista(idArista) != -1:
                    nuevaArista.identificador = self._obtenerIdAristaDisponible()

                self.aristas.append(nuevaArista) # Se agrega una arista al grafo

                # Como los nodos existen, se obtienen sus respectivas posiciones en el grafo
                p1 = self._buscarNodo(nodo1)
                p2 = self._buscarNodo(nodo2)

                # Se agregan los nodos como vecinos mutuamente
                self.nodos[p1].agregarVecino(self.nodos[p2])
                self.nodos[p2].agregarVecino(self.nodos[p1])
                return True # Se agregó la arista correctamente
            else:
                return False # No se puedo agregar la arista
        except Exception as e:
            print(f'Ocurrió un error: {e}.')
            return False
    
    @overload
    def eliminarArista(self, nodo1: int, nodo2: int) -> bool: ...
    @overload
    def eliminarArista(self, idArista: int) -> bool: ...

    def eliminarArista(self, *args, **kwargs) -> bool:
        '''
        Elimina una arista del grafo.

        Args:
            - nodo1: Es el identificador del nodo1
            - nodo2: Es el identificador del nodo2

            - idArista: Es el identificador único de la arista.
        
        Returns:
            - True: Si eliminó la arista del grafo
            - False: Si no se pudo eliminar nada
        '''
        try:

            posicionArista = self._buscarArista(args[0]) if len(args) == 1 else self._buscarArista(args[0], args[1])
            if posicionArista != -1:
                # En este bloque se busca aliminar el vecino del nodo1
                arista = self.aristas[posicionArista]
                self.nodos[self._buscarNodo(arista.a)].eliminarVecino(arista.b)

                # En este bloque se busca aliminar el vecino del nodo2
                arista = self.aristas[posicionArista]
                self.nodos[self._buscarNodo(arista.b)].eliminarVecino(arista.a)

                self.aristas.pop(posicionArista)
                return True 
            return False
            
        except Exception as e:
            print(f'Ocurrió un error: {e}')
            return False

