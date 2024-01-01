from .grafo import *
from collections import deque
from typing import List, Union, Deque

class AlgoritmoBFS():
    '''
    ---
    AlgoritmoBFS
    ---

    Clase que proporciona métodos para realizar Búsqueda en Amplitud (BFS) en grafos y generar árboles BFS.

    ---
    ### Métodos:

    - obtenerRecorridoEnOrden
    - encontrarRutaMasCorta
    - generarArbolBFS
    '''

    @staticmethod
    def obtenerRecorridoEnOrden(grafo: Union['GrafoDirigido','GrafoNoDirigido'], nodoInicio: int) -> List[int]:
        '''
        ---
        Obtiene el recorrido en orden utilizando el algoritmo de Búsqueda en Amplitud (BFS).

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
        Este método implementa el algoritmo BFS para recorrer el grafo desde un nodo de inicio.
        Comienza la búsqueda desde el nodo especificado y visita todos los nodos alcanzables en
        orden de amplitud. Retorna una lista con los identificadores de nodos en el orden en que
        fueron visitados.

        ---
        Ejemplo de uso:
        ---
        ```python
        grafo = GrafoDirigido() # Hay estas opciones de grafo
        grafo = GrafoNoDirigido()
        # Agregar nodos y aristas al grafo...
        recorrido = AlgoritmoBFS.obtenerRecorridoEnOrden(grafo, nodoInicio=1)
        print(recorrido)
        ```

        ---
        Nota:
        ---
        - Si el nodo de inicio no existe en el grafo, la lista devuelta estará vacía.
        '''
        colaBusqueda= deque()
        colaBusqueda += [nodoInicio]
        nodosVisitados = []
        if grafo.obtenerNodoPorId(nodoInicio) != -1: # Si el nodo existe en el grafo
            while colaBusqueda:
                nodo = colaBusqueda.popleft()
                if not nodo in nodosVisitados:
                    nodosVisitados.append(nodo)
                    vecinos = grafo.obtenerNodoPorId(nodo).vecinos 
                    colaBusqueda += [v.identificador for v in vecinos]
        return nodosVisitados
    
    @staticmethod
    def encontrarRutaMasCorta(grafo: 'Grafo', nodoInicio: int, nodoFin: int) -> List[int] | None:
        '''
        ---
        Encuentra la ruta más corta entre dos nodos utilizando el algoritmo de Búsqueda en Amplitud (BFS).

        ---
        Args:
        ---
        - grafo (Grafo): El grafo sobre el cual se realizará la búsqueda.
        - nodoInicio (int): El identificador del nodo desde el cual comenzará la búsqueda.
        - nodoFin (int): El identificador del nodo al cual se desea llegar.

        ---
        Returns:
        ---
        - List[int] | None: Lista de identificadores de nodos formando la ruta más corta desde el nodo de inicio hasta el nodo de destino. Si no hay ruta, devuelve None.

        ---
        Descripción:
        ---
        Este método implementa el algoritmo BFS para encontrar la ruta más corta entre dos nodos en un grafo. Comienza la búsqueda desde el nodo de inicio y continua hasta encontrar el nodo de destino. Luego, reconstruye la ruta más corta utilizando un diccionario de padres. Retorna la lista de identificadores de nodos en la ruta más corta o None si no hay ruta disponible.

        ---
        Ejemplo de uso:
        ---
        ```python
        grafo1 = GrafoDirigido() # Hay estas opciones de grafo
        grafo1 = GrafoNoDirigido()
        # Agregar nodos y aristas al grafo...
        ruta_corta = AlgoritmoBFS.encontrarRutaMasCorta(grafo=grafo1, nodoInicio=1, nodoFin=5)
        print(ruta_corta)
        ```

        ---
        Notas:
        ---
        - Si alguno de los nodos no existe en el grafo, la función devuelve None.
        - Si el nodo de inicio y el nodo de destino son el mismo, la ruta más corta será una lista que contiene únicamente ese nodo.
        '''
        colaBusqueda: Deque[int] = deque()
        colaBusqueda += [nodoInicio]
        nodosVisitados = []
        # Guarda un registro de todos los nodos Visitados y sus antecesores, para luego formar la ruta mas corta
        padres = {nodoInicio: None} 
        if grafo.obtenerNodoPorId(nodoInicio) != -1: # Si el nodo existe en el grafo
            while colaBusqueda:
                nodo = colaBusqueda.popleft()
                if not nodo in nodosVisitados:
                    if nodo == nodoFin:
                        rutaMasCorta = []
                        aux = nodo
                        while aux != None:
                            rutaMasCorta.append(aux)
                            aux = padres[aux]
                        return rutaMasCorta[::-1]
                    else:
                        # Se agrega el nodo como visitado
                        nodosVisitados.append(nodo)

                        # Se obtiene la lista de los vecinos del nodo
                        vecinos = grafo.obtenerNodoPorId(nodo).vecinos 
                        idsVecinos = [v.identificador for v in vecinos]

                        # Se forma una lista de los nodos que ya han sido visitados o que están esperando en la cola
                        aux = colaBusqueda
                        aux += nodosVisitados

                        # Se filtran los ids de vecinos que realmente faltan encolar
                        vecinosFiltrados = [v for v in idsVecinos if not v in aux]

                        colaBusqueda += vecinosFiltrados
                        for v in vecinosFiltrados:
                            padres[v] = nodo
        return None
    
    @staticmethod
    @overload
    def generarArbolBFS(grafo: 'GrafoDirigido', raiz: int) -> 'GrafoDirigido': ...
    @staticmethod
    @overload
    def generarArbolBFS(grafo: 'GrafoNoDirigido', raiz: int) -> 'GrafoNoDirigido': ...

    @staticmethod
    def generarArbolBFS(grafo: Union['GrafoDirigido','GrafoNoDirigido'], raiz: int) -> Union['GrafoDirigido','GrafoNoDirigido',None]:
        '''
        ---
        Genera un árbol BFS a partir de un grafo y una raíz especificada.

        ---
        Args:
        ---
        - grafo (Grafo): El grafo sobre el cual se generará el árbol BFS.
        - raiz (int): El identificador del nodo raíz desde el cual comenzará la generación.

        ---
        Returns:
        ---
        - Grafo | None: Un objeto de tipo Grafo (ya sea GrafoDirigido o GrafoNoDirigido) que representa el árbol BFS generado. Si la raíz no existe en el grafo, devuelve None.

        ---
        Descripción:
        ---
        Este método implementa el algoritmo BFS para generar un árbol BFS a partir de un grafo y una raíz especificada. Comienza la búsqueda desde la raíz y agrega nodos y aristas al árbol en función del recorrido BFS en el grafo original. Retorna el árbol BFS generado.

        ---
        Ejemplo de uso:
        ---
        ```
        grafo_original = GrafoDirigido()  # o GrafoNoDirigido()
        # Agregar nodos y aristas al grafo original...
        arbol_bfs = AlgoritmoBFS.generarArbolBFS(grafo_original, raiz=1)
        ```

        ---
        Notas:
        ---
        - Si la raíz no existe en el grafo, la función devuelve None.
        - El tipo de grafo retornado (GrafoDirigido o GrafoNoDirigido) dependerá del tipo del grafo original.
        - Los nodos en el árbol solo contienen el identificador y el contenido del nodo original.
        '''
        colaBusqueda: Deque[int] = deque()
        colaBusqueda += [raiz]
        nodosVisitados = []
        if grafo.esDirigido():
            arbol = GrafoDirigido()
        else:
            arbol = GrafoNoDirigido()

        if grafo.obtenerNodoPorId(raiz) != -1: # Si la raiz realmente existe en el grafo    
            while colaBusqueda:
                nodo = colaBusqueda.popleft()
                if not nodo in nodosVisitados:
                    nodosVisitados.append(nodo)

                    # Se obtiene la lista de los vecinos del nodo
                    vecinos = grafo.obtenerNodoPorId(nodo).vecinos 
                    idsVecinos = [v.identificador for v in vecinos]

                    # Se forma una lista de los nodos que ya han sido visitados o que están esperando en la cola
                    aux = colaBusqueda
                    aux += nodosVisitados

                    # Se filtran los ids de vecinos que realmente faltan encolar
                    vecinosFiltrados = [v for v in idsVecinos if not v in aux]

                    colaBusqueda += vecinosFiltrados

                    # Se copia el nodo en el arbol si todavía no existe en este pero se copia sin los vecinos, es decir únicamente el identificador y su contenido
                    if arbol._buscarNodo(nodo) == -1: 
                        n = grafo.obtenerNodoPorId(nodo)
                        arbol.agregarNodo(Nodo(n.identificador,n.contenido))
                    # Se agregan los vecinos al nodo en el arbol
                    for v in vecinosFiltrados:
                        if arbol._buscarNodo(v) == -1: # Se crea el nodo vecino en el arbol si no existe
                            n = grafo.obtenerNodoPorId(v)
                            arbol.agregarNodo(Nodo(n.identificador,n.contenido))
                        arbol.agregarArista(nodo,v)
            return arbol
        return None 
    
