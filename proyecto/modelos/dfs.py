from typing import Union, List
from .grafo import *


class AlgoritmoDFS:
    '''
    ---
    AlgoritmoDFS
    ---

    Clase que proporciona métodos para realizar Búsqueda en Profundidad (DFS) en grafos y generar árboles DFS.

    ---
    ### Métodos:

    - obtenerRecorridoEnOrden
    - encontrarRuta
    - generarArbolDFS
    '''

    @staticmethod
    def obtenerRecorridoEnOrden(grafo: Union['GrafoDirigido','GrafoNoDirigido'], nodoInicio: int) -> List[int]:
        '''
        ---
        Obtiene el recorrido en orden utilizando el algoritmo de Búsqueda en Profundidad (DFS).

        ---
        Args:
        ---
        - grafo (Grafo): El grafo sobre el cual se realizará la búsqueda.
        - nodoInicio (int): El identificador del nodo desde el cual comenzará la búsqueda.

        ---
        Returns:
        ---
        - List[int]: Lista de identificadores de nodos en el orden en que fueron visitados.

        ---
        Descripción:
        ---
        Este método implementa el algoritmo DFS para recorrer el grafo desde un nodo de inicio.
        Comienza la búsqueda desde el nodo especificado y visita todos los nodos en orden de profundidad. Retorna una lista con los identificadores de nodos en el orden en que
        fueron visitados.

        ---
        Ejemplo de uso:
        ---
        ```python
        grafo = GrafoDirigido() # Hay estas opciones de grafo
        grafo = GrafoNoDirigido()
        # Agregar nodos y aristas al grafo...
        recorrido = AlgoritmoDFS.obtenerRecorridoEnOrden(grafo, nodoInicio=1)
        print(recorrido)
        ```

        ---
        Nota:
        ---
        - Si el nodo de inicio no existe en el grafo, la lista devuelta estará vacía.
        '''
        def dfsRecursivo(nodo: int, recorrido: List[int], nodosVisitados: List[int]) -> None:
            try:
                recorrido.append(nodo)
                nodosVisitados.append(nodo)

                for vecino in grafo.obtenerNodoPorId(nodo).vecinos:
                    if not vecino.identificador in nodosVisitados:
                        dfsRecursivo(vecino.identificador, recorrido, nodosVisitados)
            except Exception as e:
                recorrido = []
            recorrido = []

        recorrido = []
        nodosVisitados = []
        # Se verifica si el nodo existe en el grafo para iniciar la funcion recursiva
        if grafo._nodosExisten([nodoInicio]):
            dfsRecursivo(nodoInicio, recorrido, nodosVisitados)
        return recorrido

    @staticmethod
    def encontrarRuta(grafo: Union['GrafoDirigido','GrafoNoDirigido'], nodoInicio: int, nodoFin: int) -> List[int]:
        '''
        ---
        Encuentra una ruta entre dos nodos utilizando el algoritmo de Búsqueda en Profundidad (DFS).

        ---
        Args:
        ---
        - grafo (Grafo): El grafo sobre el cual se realizará la búsqueda.
        - nodoInicio (int): El identificador del nodo desde el cual comenzará la búsqueda.
        - nodoFin (int): El identificador del nodo al cual se desea llegar.

        ---
        Returns:
        ---
        - List[int]: Lista de identificadores de nodos formando la ruta desde el nodo de inicio hasta el nodo de destino. Si no hay ruta, devuelve una lista vacía.

        ---
        Descripción:
        ---
        Este método implementa el algoritmo DFS para encontrar la ruta que se sigue entre dos nodos en un grafo. Comienza la búsqueda desde el nodo de inicio y continua hasta encontrar el nodo de destino. Retorna la lista de identificadores de nodos en la ruta tomada o una lista vacía si no hay ruta disponible.

        ---
        Ejemplo de uso:
        ---
        ```python
        grafo1 = GrafoDirigido() # Hay estas opciones de grafo
        grafo1 = GrafoNoDirigido()
        # Agregar nodos y aristas al grafo...
        ruta_en_profundidad = AlgoritmoDFS.encontrarRuta(grafo=grafo1, nodoInicio=1, nodoFin=5)
        print(ruta_en_profundidad)
        ```

        ---
        Notas:
        ---
        - Si alguno de los nodos no existe en el grafo, la función devuelve una lista vacía.
        - Si el nodo de inicio y el nodo de destino son el mismo, la ruta más corta será una lista que contiene únicamente ese nodo.
        '''
        def rutaDfsRecursiva(nodo: int, ruta: List[int], nodosVisitados: List[int]) -> None:
            try:
                ruta.append(nodo)
                nodosVisitados.append(nodo)

                # se obtienen los vecinos del nodo
                for vecino in grafo.obtenerNodoPorId(nodo).vecinos:
                    # Verificar si el vecino ya ha sido visitado, si no ha sido visitado entonces se le visita
                    if not vecino.identificador in nodosVisitados:
                        rutaDfsRecursiva(vecino.identificador, ruta, nodosVisitados)
                        if ruta[-1] == nodoFin:
                            # Si ya se encontró el nodo fin, entonces ya no es necesario buscar en los otros vecinos y solo regresa.
                            break 
                
                if ruta[-1] != nodoFin:
                    # Si el nodo visitado no es el nodoFin que se busca, entonces se elimina
                    ruta.pop(-1)

            except Exception as e:
                ruta = []
            ruta = []

        ruta = []
        nodosVisitados = []
        # Se verifica si el nodo existe en el grafo para iniciar la funcion recursiva
        if grafo._nodosExisten([nodoInicio]):
            rutaDfsRecursiva(nodoInicio, ruta, nodosVisitados)
        return ruta

    @staticmethod
    @overload
    def generarArbolDFS(grafo: 'GrafoDirigido', raiz: int) -> 'GrafoDirigido': ...
    @staticmethod
    @overload
    def generarArbolDFS(grafo: 'GrafoNoDirigido', raiz: int) -> 'GrafoNoDirigido': ...

    @staticmethod
    def generarArbolDFS(grafo: Union['GrafoDirigido','GrafoNoDirigido'], raiz: int) -> Union['GrafoDirigido', 'GrafoNoDirigido',None]:
        '''
        ---
        Genera un árbol DFS a partir de un grafo y una raíz.

        ---
        Args:
        ---
        - grafo (Grafo): El grafo sobre el cual se construirá el árbol DFS.
        - raiz (int): El identificador del nodo raíz.

        ---
        Returns:
        ---
        - Grafo | None: Un objeto de tipo Grafo (ya sea GrafoDirigido o GrafoNoDirigido) que representa el árbol DFS generado. Si la raíz no existe en el grafo, devuelve None.

        ---
        Descripción:
        ---
        Este método implementa el algoritmo DFS para generar un árbol DFS a partir de un grafo y una raíz especificada. Comienza la búsqueda desde la raíz y agrega nodos y aristas al árbol en función del recorrido DFS en el grafo original. Retorna el árbol DFS generado.

        ---
        Ejemplo de uso:
        ---
        ```
        grafo_original = GrafoDirigido()  # o GrafoNoDirigido()
        # Agregar nodos y aristas al grafo original...
        arbol_dfs = AlgoritmoDFS.generarArbolDFS(grafo_original, raiz=1)
        print(arbol_dfs)
        ```

        ---
        Notas:
        ---
        - Si la raíz no existe en el grafo, la función devuelve None.
        - El tipo de grafo retornado (GrafoDirigido o GrafoNoDirigido) dependerá del tipo del grafo original.
        - Los nodos en el árbol solo contienen el identificador y el contenido del nodo original.
        '''
        def dfsArbolRecursivo(arbol: Union['GrafoDirigido', 'GrafoNoDirigido'], nodo: int, nodosVisitados: List[int]) -> None:
            try:
                nodosVisitados.append(nodo)
                # Se copia el nodo en el arbol si todavía no existe en este pero se copia sin los vecinos, es decir únicamente el identificador y su contenido
                if arbol._buscarNodo(nodo) == -1: 
                    n = grafo.obtenerNodoPorId(nodo)
                    arbol.agregarNodo(Nodo(n.identificador,n.contenido))

                for vecino in grafo.obtenerNodoPorId(nodo).vecinos:
                    if not vecino.identificador in nodosVisitados:
                        # Si el arbol no tiene creado al vecino, entonces se crea este dentro del arbol.
                        if arbol._buscarNodo(vecino.identificador) == -1: 
                            v = grafo.obtenerNodoPorId(vecino.identificador)
                            arbol.agregarNodo(Nodo(v.identificador,v.contenido))
                        arbol.agregarArista(nodo, vecino.identificador)
                        # Se procede a buscar recursivamente en el vecino
                        dfsArbolRecursivo(arbol, vecino.identificador, nodosVisitados)
                            
                        
            except Exception as e:
                return None 
            return None 

        nodosVisitados = []
        if grafo.esDirigido():
            arbol = GrafoDirigido()
        else:
            arbol = GrafoNoDirigido()
        # Se verifica si la raiz existe en el grafo para iniciar la funcion recursiva
        if grafo._nodosExisten([raiz]):
            dfsArbolRecursivo(arbol, raiz, nodosVisitados)
            return arbol 
        else:
            return None
