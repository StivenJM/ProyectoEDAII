from .modelos.menu import *
from .modelos.grafo import *
from .modelos.dfs import AlgoritmoDFS
from .modelos.bfs import AlgoritmoBFS
import os
import platform
import shutil 
import subprocess
from typing import List
import json 
import csv

carpetaGrafos = 'datos_grafos' # Esta es la carpeta donde se guardan los grafos del programa
carpetaExportar = 'csv' # Esta es la carpeta donde se exportan los datos de los grafos

# Para utilizar editores graficos, se verifica si la maquina es windows
def esWindows() -> bool:
    return platform.system() == 'Windows'

# Funcion utilizada para abrir un archivo del programa con vscode o notepad
def abrirArchivoConEditor(nombreArchivo: str) -> bool:
    '''
    Esta funcion abre el archivo por defecto en VSCode, sin embargo si no está instalado, entonces abrirá el archivo por el bloc de notas de Windows. Es necesario pasarle el nombre del archivo con la extensión definida.

    Returns:
    - True: si el archivo se abrió exitosamente
    - False: si no se pudo abrir el archivo
    '''
    try:
        if existeArchivo(nombreArchivo):
            ruta = os.path.join(os.path.dirname(__file__), carpetaGrafos, nombreArchivo)
            # Verificar si VSCode está instalado
            if shutil.which("code"):
                # Abrir el archivo con VSCode
                subprocess.run(['code', ruta], shell=True, check=True)
            else:
                # Si VSCode no está instalado, abrir el archivo con Notepad
                subprocess.run(['notepad', ruta], shell=True, check=True)
            return True 
        else:
            return False 
    except Exception as e:
        return False 

def limpiarConsola():
    '''
    Este metodo puede limpiar la consola de sistema basados en Unix (Linux, macOS) o en Nt (Windows)
    '''
    try:

        sistemaOperativo = os.name

        if sistemaOperativo == 'posix':
            # Si el sistema operativo es UNIX (Linux, macOS)
            os.system('clear')
        elif sistemaOperativo == 'nt':
            # Si el sistema operativo es Windows
            os.system('cls')

    except Exception as e:
        pass 

def eliminarArchivo(nombreArchivo: str) -> bool:
    '''
    Elimina un archivo (archivo.extension) del almacenamiento del programa.
    '''
    ruta = os.path.join(os.path.dirname(__file__), carpetaGrafos, nombreArchivo)
    try:
        if existeArchivo(nombreArchivo):
            os.remove(ruta)
            return True 
        return False 
    except OSError as e:
        return False 

def eliminarGrafo(nombreGrafo: str) -> bool:
    f'''
    Elimina un archivo que guarda la informacion de un grafo en el almacenamiento del programa.
    '''
    archivo = nombreGrafo + '.json'
    return eliminarArchivo(archivo)

def obtenerArchivos() -> List[str]:
    '''
    Devuelve una lista de todos los archivos dentro del almacenamiento del programa.
    '''
    carpeta = os.path.join(os.path.dirname(__file__), carpetaGrafos)
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        archivos = os.listdir(carpeta)
        return archivos 
    return []

def existeArchivo(nombreArchivo: str) -> bool:
    '''
    Devuelve un booleano respondiendo a la pregunta si existe un archivo con el nombre nombreArchivo dentro del almacenamiento del programa.
    '''
    carpeta = os.path.join(os.path.dirname(__file__), carpetaGrafos)
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        archivos = os.listdir(carpeta)
        return nombreArchivo in archivos
    return False 

def existenGrafos() -> bool:
    '''
    Esta funcion indica si existe al menos un grafo almacenado en el programa
    '''
    archivos = obtenerArchivos()
    grafos = [grafo for grafo in archivos if grafo.endswith('.json')]
    return len(grafos) > 0

def obtenerGrafos() -> List[str]:
    '''
    Esta funcion devuelve una lista de los nombres de los grafos disponibles.
    '''
    archivos = obtenerArchivos()
    grafos = [grafo[:-5] for grafo in archivos if grafo.endswith('.json')]
    return grafos 

def guardarGrafo(grafo: 'Grafo', nombre: str):
    '''
    Esta funcion guarda el grafo que se pasa como parámetro en un archivo .json, no es necesario pasarle el nombre con la extensión ya que lo agrega automáticamente.
    '''
    grafoDiccionario = grafo.to_dict() # Se convierte al grafo en un diccionario
    nombreArchivo = nombre + '.json'
    ruta = os.path.join(os.path.dirname(__file__), carpetaGrafos, nombreArchivo)
    with open(ruta, 'w') as archivo:
        json.dump(grafoDiccionario, archivo, indent=4)

def exportarGrafo(grafo: 'Grafo', nombreGrafo: str) -> bool:
    '''
    Esta funcion recibe un grafo y crea dos archivos csv dentro de la carpeta "csv" del proyecto, estos archivos estan agrupados en una carpeta con el nombre del grafo, los archivos tienen la extensión csv.
    Un archivo almacena los nodos, mientras que otro almacena las aristas.

    ---
    Returns:
    - True: Si se logró exportar el grafo exitosamente
    - False: Si no se puedo exportar el grafo
    '''
    try:
        rutaCarpeta = os.path.join(os.path.dirname(__file__), carpetaExportar, nombreGrafo)

        # Se crea la carpeta
        os.makedirs(rutaCarpeta)

        # Se extraen los nodos del grafo
        nodosEncabezado = [['Id','Label']] # Es el encabezado del archivo que guardará lo nodos
        nodos = [[nodo.identificador, nodo.contenido] for nodo in grafo.nodos]
        nodos = nodosEncabezado + nodos 

        # Se extraen las aristas del grafo
        tipo = 'Directed' if grafo.esDirigido() else 'Undirected'
        aristasEncabezado = [['Source','Target','Type','Id']]
        aristas = [[arista.a, arista.b, tipo, arista.identificador] for arista in grafo.aristas]
        aristas = aristasEncabezado + aristas
        
        # Se obtienen las rutas para guardar los archivos
        rutaArchivoNodos = os.path.join(rutaCarpeta, 'nodos.csv')
        rutaArchivoAristas = os.path.join(rutaCarpeta, 'aristas.csv')

        # Se guardan los archivos
        with open(rutaArchivoNodos, 'w', newline='') as file:
            writter = csv.writer(file, delimiter=',')
            writter.writerows(nodos)

        with open(rutaArchivoAristas, 'w', newline='') as file:
            writter = csv.writer(file, delimiter=',')
            writter.writerows(aristas)

        return True 

    except Exception as e:
        return False 

def obtenerGrafo(nombreGrafo: str) -> Union['GrafoDirigido', 'GrafoNoDirigido']:
    '''
    Esta funcion devuelve un grafo guardado en alguno de los archivos del almacenamiento del programa.
    '''
    nombreArchivo = nombreGrafo + '.json'
    ruta = os.path.join(os.path.dirname(__file__), carpetaGrafos, nombreArchivo)
    with open(ruta, 'r') as archivo:
        grafoDict = json.load(archivo)
    
    # Primero se crea el grafo sea dirigido o no dirigido
    if grafoDict['dirigido']:
        grafoRecuperado = GrafoDirigido()
    else:
        grafoRecuperado = GrafoNoDirigido()
    
    # Se reconstruyen los nodos
    for nodoData in grafoDict['nodos']:
        nodo = Nodo(nodoData['identificador'], nodoData['contenido'])
        grafoRecuperado.agregarNodo(nodo)
    
    # Se reconstruyen las aristas
    for aristaData in grafoDict['aristas']:
        grafoRecuperado.agregarArista(aristaData['a'], aristaData['b'], aristaData['identificador'])
    
    return grafoRecuperado

def seleccionarGrafo() -> str:
    '''
    Esta funcion muestra los grafos disponibles y retorna el nombre del grafo seleccionado. Es recomendable que ya existan grafos disponibles en la carpeta de almacenamiento de grafos del programa.
    '''
    limpiarConsola()
    grafos = obtenerGrafos()
    menuAuxiliar = MenuSinGrafo(grafos, 'Seleccionar un grafo') # Se crea un menu auxiliar
    print(menuAuxiliar.textoPorConsola(FUENTE_STANDARD))
    menuAuxiliar.pedirOpcion()
    return menuAuxiliar.opciones[menuAuxiliar.opcion]

    

def main():
    menuPrincipal = MenuSinGrafo(['Salir', 'Grafos', 'Algoritmos'], 'Proyecto EDA II')
    menuGrafos = MenuSinGrafo(['Atrás', 'Crear grafo', 'Seleccionar grafo existente'], 'GRAFOS')
    menuAlgoritmos = MenuConGrafo(['Atrás', 'BFS', 'DFS'], 'Algoritmos')
    menuCrearGrafo = MenuConGrafo(['Atrás y crear','Atrás y descartar','Añadir nodo','Añadir arista','Eliminar nodo', 'Eliminar arista','Abrir editor de texto* Solo disponible en Windows'], 'Crear Grafo')
    menuGrafoSeleccionado = MenuConGrafo(['Atrás','Mostrar grafo completo','Editar grafo','Eliminar grafo','Obtener nodos','Obtener bordes','Exportar grafo a csv'], 'Grafo Seleccionado')
    menuEditarGrafo = MenuConGrafo(['Atrás','Añadir nodo','Añadir arista','Eliminar nodo','Eliminar arista','Abrir editor de texto* Solo disponible en Windows'], 'Editar Grafo')
    menuAlgoritmoBFS = MenuConGrafo(['Atrás','Mostrar recorrido', 'Mostrar ruta más corta','Generar árbol BFS'], 'Algoritmo BFS')
    menuAlgoritmoDFS = MenuConGrafo(['Atrás','Mostrar recorrido', 'Mostrar ruta DFS','Generar árbol DFS'], 'Algoritmo DFS')
    
    while menuPrincipal.opcion != 0:
        try:
            limpiarConsola()
            print(menuPrincipal.textoPorConsola(FUENTE_CRICKET))
            menuPrincipal.pedirOpcion()
            if menuPrincipal.opcion == 1:

                while menuGrafos.opcion != 0:
                    limpiarConsola()
                    print(menuGrafos.textoPorConsola(FUENTE_CYBERLARGE))
                    menuGrafos.pedirOpcion()
                    if menuGrafos.opcion == 1:

                        nombreGrafo = input('Escriba el nombre del grafo que desea crear: ')
                        if existeArchivo(nombreGrafo+'.json'):
                            input('Ese nombre ya existe. Presiona una tecla para continuar...')
                        else:
                            dirigido = input('¿El grafo es dirigido? (S|N): ')
                            # Creacion del grafo
                            if dirigido.upper() == 'S':
                                grafo1 = GrafoDirigido()
                            else:
                                grafo1 = GrafoNoDirigido()
                            menuCrearGrafo.nombreGrafo = nombreGrafo

                            while menuCrearGrafo.opcion != 0 and menuCrearGrafo.opcion != 1:
                                limpiarConsola()
                                print(menuCrearGrafo.textoPorConsola(FUENTE_CYBERLARGE))
                                menuCrearGrafo.pedirOpcion()
                                if menuCrearGrafo.opcion == 0: # Guardar grafo y salir
                                    guardarGrafo(grafo1, nombreGrafo)
                                if menuCrearGrafo.opcion == 1: # Descartar grafo y salir
                                    eliminarGrafo(nombreGrafo)
                                if menuCrearGrafo.opcion == 2: # Añadir nodo
                                    idNodo = input('Escriba el numero identificador del nodo, presione enter para id automatico: ')
                                    contenido = input('Escriba el contenido del nodo: ')
                                    if idNodo.isdigit():
                                        grafo1.agregarNodo(Nodo(int(idNodo), contenido))
                                    else:
                                        grafo1.agregarNodo(Nodo(contenido))
                                if menuCrearGrafo.opcion == 3: # Añadir arista
                                    print('NOTA: en un grafo dirigido el primer nodo ingresado es el nodo origen mientras que el segundo es el nodo de destino.')
                                    nodo1 = input('Escriba el id del primer nodo: ')
                                    nodo2 = input('Escriba el id del segundo nodo: ')
                                    r = False 
                                    if nodo1.isdigit() and nodo2.isdigit():
                                        r = grafo1.agregarArista(int(nodo1),int(nodo2))
                                    if not r:
                                        print('No se pudo agregar la arista, revise los datos.\nPresione una tecla para continuar...', end="")
                                        input()
                                if menuCrearGrafo.opcion == 4: # Eliminar nodo
                                    nodo = input('Escriba el id del nodo a eliminar: ')
                                    r = False 
                                    if nodo.isdigit():
                                        r = grafo1.eliminarNodo(int(nodo))
                                    if not r:
                                        print('No se pudo eliminar el nodo, revise los datos.\nPresione una tecla para continuar...', end="")
                                        input()
                                if menuCrearGrafo.opcion == 5: # Eliminar arista
                                    print('NOTA: en un grafo dirigido el primer nodo ingresado es el nodo origen mientras que el segundo es el nodo de destino.')
                                    nodo1 = input('Escriba el id del primer nodo: ')
                                    nodo2 = input('Escriba el id del segundo nodo: ')
                                    r = False 
                                    if nodo1.isdigit() and nodo2.isdigit():
                                        r = grafo1.eliminarArista(int(nodo1),int(nodo2))
                                    if not r:
                                        print('No se pudo eliminar la arista, revise los datos.\nPresione una tecla para continuar...', end="")
                                        input()
                                if menuCrearGrafo.opcion == 6: # Abrir editor grafico
                                    if esWindows():
                                        guardarGrafo(grafo1, nombreGrafo)
                                        r = abrirArchivoConEditor(nombreGrafo + '.json')
                                        if not r:
                                            input('No se pudo abrir el archivo. Presione una tecla para continuar...')
                                        else:
                                            menuCrearGrafo.opcion = 0 # Para que salga del menu y no genere incongruencias con lo ingresado en el editor de texto
                                    else:
                                        input('No tiene acceso a esta opcion. Presione una tecla para continuar...')
                            
                            menuCrearGrafo.opcion = -1 # Se restablece la opcion de menuCrearGrafo


                    elif menuGrafos.opcion == 2:
                        
                        if not existenGrafos():
                            input('No tiene grafos disponibles. Presione enter para continuar...')
                        else:
                            nombreGrafo = seleccionarGrafo() # Se pide seleccionar un grafo de los archivos
                            grafo1 = obtenerGrafo(nombreGrafo) # Se carga el grafo de los archivos
                            menuGrafoSeleccionado.nombreGrafo = nombreGrafo
                            menuEditarGrafo.nombreGrafo = nombreGrafo

                            while menuGrafoSeleccionado.opcion != 0:
                                limpiarConsola()
                                print(menuGrafoSeleccionado.textoPorConsola(FUENTE_CYBERLARGE))
                                menuGrafoSeleccionado.pedirOpcion()
                                if menuGrafoSeleccionado.opcion == 0: # Atras guardando grafo
                                    guardarGrafo(grafo1, nombreGrafo)
                                if menuGrafoSeleccionado.opcion == 1: # Mostrar grafo completo
                                    limpiarConsola()
                                    print(grafo1)
                                    input('Presione una tecla para continuar...')
                                elif menuGrafoSeleccionado.opcion == 2: # Editar grafo
                                    
                                    while menuEditarGrafo.opcion != 0:
                                        limpiarConsola()
                                        print(menuEditarGrafo.textoPorConsola(FUENTE_CYBERLARGE))
                                        menuEditarGrafo.pedirOpcion()
                                        if menuEditarGrafo.opcion == 1: # Añadir nodo al grafo
                                            idNodo = input('Escriba el numero identificador del nodo, presione enter para id automatico: ')
                                            contenido = input('Escriba el contenido del nodo: ')
                                            if idNodo.isdigit():
                                                grafo1.agregarNodo(Nodo(int(idNodo), contenido))
                                            else:
                                                grafo1.agregarNodo(Nodo(contenido))
                                        elif menuEditarGrafo.opcion == 2: # Añadir arista
                                            print('NOTA: en un grafo dirigido el primer nodo ingresado es el nodo origen mientras que el segundo es el nodo de destino.')
                                            nodo1 = input('Escriba el id del primer nodo: ')
                                            nodo2 = input('Escriba el id del segundo nodo: ')
                                            r = False 
                                            if nodo1.isdigit() and nodo2.isdigit():
                                                r = grafo1.agregarArista(int(nodo1),int(nodo2))
                                            if not r:
                                                print('No se pudo agregar la arista, revise los datos.\nPresione una tecla para continuar...', end="")
                                                input()
                                        elif menuEditarGrafo.opcion == 3: # Eliminar nodo
                                            nodo = input('Escriba el id del nodo a eliminar: ')
                                            r = False 
                                            if nodo.isdigit():
                                                r = grafo1.eliminarNodo(int(nodo))
                                            if not r:
                                                print('No se pudo eliminar el nodo, revise los datos.\nPresione una tecla para continuar...', end="")
                                                input()
                                        elif menuEditarGrafo.opcion == 4: # Eliminar arista
                                            print('NOTA: en un grafo dirigido el primer nodo ingresado es el nodo origen mientras que el segundo es el nodo de destino.')
                                            nodo1 = input('Escriba el id del primer nodo: ')
                                            nodo2 = input('Escriba el id del segundo nodo: ')
                                            r = False 
                                            if nodo1.isdigit() and nodo2.isdigit():
                                                r = grafo1.eliminarArista(int(nodo1),int(nodo2))
                                            if not r:
                                                print('No se pudo eliminar la arista, revise los datos.\nPresione una tecla para continuar...', end="")
                                                input()
                                        elif menuEditarGrafo.opcion == 5: # Abrir editor gráfico
                                            if esWindows():
                                                guardarGrafo(grafo1, nombreGrafo)
                                                r = abrirArchivoConEditor(nombreGrafo + '.json')
                                                if not r:
                                                    input('No se pudo abrir el archivo. Presione una tecla para continuar...')
                                                else:
                                                    menuEditarGrafo.opcion = 0 # Para que salga del menu y no genere incongruencias con los datos
                                                    menuGrafoSeleccionado.opcion = 0 
                                            else:
                                                input('No tiene acceso a esta opcion. Presione una tecla para continuar...')

                                    menuEditarGrafo.opcion = -1 # Se restablece la opcion de menuEditarGrafo

                                elif menuGrafoSeleccionado.opcion == 3: # Eliminar grafo
                                    eliminarGrafo(nombreGrafo)
                                    menuGrafoSeleccionado.opcion = 0 # Para que salga del menu ya que el grafo ya no existe
                                    input('Presione una tecla para continuar...')
                                elif menuGrafoSeleccionado.opcion == 4: # Obtener nodos
                                    print(grafo1.nodos)
                                    input('Presione una tecla para continuar...')
                                elif menuGrafoSeleccionado.opcion == 5: # Obtener aristas
                                    print(grafo1.aristas)
                                    input('Presione una tecla para continuar...')
                                elif menuGrafoSeleccionado.opcion == 6: # Exportar grafo
                                    r = exportarGrafo(grafo1, nombreGrafo)
                                    if not r:
                                        print('No se pudo exportar el grafo. ', ends='')
                                    input('Presione una tecla para continuar...')

                            menuGrafoSeleccionado.opcion = -1 # Se restablece la opcion de menuGrafoSeleccionado

                menuGrafos.opcion = -1 # Se restablece la opcion de menuGrafos

            elif menuPrincipal.opcion == 2:

                if not existenGrafos():
                    input('No tiene grafos disponibles. Presione enter para continuar...')
                else:
                    nombreGrafo = seleccionarGrafo() # Se pide seleccionar un grafo de los archivos
                    grafo1 = obtenerGrafo(nombreGrafo) # Se carga el grafo de los archivos
                    menuAlgoritmos.nombreGrafo = nombreGrafo
                    menuAlgoritmoBFS.nombreGrafo = nombreGrafo
                    menuAlgoritmoDFS.nombreGrafo = nombreGrafo

                    while menuAlgoritmos.opcion != 0:
                        limpiarConsola()
                        print(menuAlgoritmos.textoPorConsola(FUENTE_CYBERLARGE))
                        menuAlgoritmos.pedirOpcion()
                        if menuAlgoritmos.opcion == 1:

                            while menuAlgoritmoBFS.opcion != 0:
                                limpiarConsola()
                                print(menuAlgoritmoBFS.textoPorConsola(FUENTE_CYBERLARGE))
                                menuAlgoritmoBFS.pedirOpcion()
                                if menuAlgoritmoBFS.opcion == 1: # mostrar recorrido BFS
                                    limpiarConsola()
                                    print(grafo1)
                                    idNodo = input('\n\nEscriba el numero identificador del nodo de inicio: ')
                                    if idNodo.isdigit():
                                        print(f'\nRecorrido BFS: {AlgoritmoBFS.obtenerRecorridoEnOrden(grafo1, int(idNodo))}')
                                    else:
                                        print('Identificador inválido. Revise los datos...', end="")
                                    input('Presione una tecla para continuar...')
                                elif menuAlgoritmoBFS.opcion == 2: # mostrar ruta mas corta - BFS
                                    limpiarConsola()
                                    print(grafo1)
                                    nodoInicio = input('\n\nEscriba el id del nodo de inicio: ')
                                    nodoDestino = input('Escriba el id del nodo de destino: ')
                                    r = False 
                                    if nodoInicio.isdigit() and nodoDestino.isdigit():
                                        print(f'\nRuta más corta: {AlgoritmoBFS.encontrarRutaMasCorta(grafo1, int(nodoInicio), int(nodoDestino))}')
                                        r = True 
                                    if not r:
                                        print('Identificador inválido. Revise los datos...', end="")
                                    input('Presione una tecla para continuar...')
                                elif menuAlgoritmoBFS.opcion == 3: # generar arbol BFS
                                    limpiarConsola()
                                    print(grafo1)
                                    raiz = input('\n\nEscriba el numero identificador del nodo raiz: ')
                                    if raiz.isdigit():
                                        arbol = AlgoritmoBFS.generarArbolBFS(grafo1, int(raiz))
                                        print(f'\nArbol BFS: \n{arbol}')

                                        # Opcion para guardar el arbol
                                        guardarArbol = input('¿Desea guardar el árbol generado? (S|N): ')
                                        if guardarArbol.upper() == 'S':
                                            nombreArbol = input('Escriba el nombre del arbol: ')
                                            if existeArchivo(nombreArbol +'.json'):
                                                input('Ese nombre ya existe. Presiona una tecla para continuar...')
                                            else:
                                                guardarGrafo(arbol, nombreArbol)

                                    else:
                                        print('Identificador inválido. Revise los datos...', end="")
                                    input('Presione una tecla para continuar...')
                                    
                            menuAlgoritmoBFS.opcion = -1 # Se restablece la opcion de menuAlgoritmoBFS

                        elif menuAlgoritmos.opcion == 2:

                            while menuAlgoritmoDFS.opcion != 0:
                                limpiarConsola()
                                print(menuAlgoritmoDFS.textoPorConsola(FUENTE_CYBERLARGE))
                                menuAlgoritmoDFS.pedirOpcion()
                                if menuAlgoritmoDFS.opcion == 1: # Mostrar recorrido DFS
                                    limpiarConsola()
                                    print(grafo1)
                                    idNodo = input('\n\nEscriba el numero identificador del nodo de inicio: ')
                                    if idNodo.isdigit():
                                        print(f'\nRecorrido DFS: {AlgoritmoDFS.obtenerRecorridoEnOrden(grafo1, int(idNodo))}')
                                    else:
                                        print('Identificador inválido. Revise los datos...', end="")
                                    input('Presione una tecla para continuar...')
                                if menuAlgoritmoDFS.opcion == 2: # Mostrar ruta DFS
                                    limpiarConsola()
                                    print(grafo1)
                                    nodoInicio = input('\n\nEscriba el id del nodo de inicio: ')
                                    nodoDestino = input('Escriba el id del nodo de destino: ')
                                    r = False 
                                    if nodoInicio.isdigit() and nodoDestino.isdigit():
                                        print(f'\nRuta más corta: {AlgoritmoDFS.encontrarRuta(grafo1, int(nodoInicio), int(nodoDestino))}')
                                        r = True 
                                    if not r:
                                        print('Identificador inválido. Revise los datos...', end="")
                                    input('Presione una tecla para continuar...')
                                if menuAlgoritmoDFS.opcion == 3: # Generar arbol DFS
                                    limpiarConsola()
                                    print(grafo1)
                                    raiz = input('\n\nEscriba el numero identificador del nodo raiz: ')
                                    if raiz.isdigit():
                                        arbol = AlgoritmoDFS.generarArbolDFS(grafo1, int(raiz))
                                        print(f'\nArbol BFS: \n{arbol}')

                                        # Opcion para guardar el arbol
                                        guardarArbol = input('¿Desea guardar el árbol generado? (S|N): ')
                                        if guardarArbol.upper() == 'S':
                                            nombreArbol = input('Escriba el nombre del arbol: ')
                                            if existeArchivo(nombreArbol +'.json'):
                                                input('Ese nombre ya existe. Presiona una tecla para continuar...')
                                            else:
                                                guardarGrafo(arbol, nombreArbol)

                                    else:
                                        print('Identificador inválido. Revise los datos...', end="")
                                    input('Presione una tecla para continuar...')

                            menuAlgoritmoDFS.opcion = -1 # Se restablece la opcion de menuAlgoritmoDFS

                    menuAlgoritmos.opcion = -1 # Se restablece la opcion de menuAlgoritmos

        except Exception as e:
            input('Ocurrio un error. Presione enter para continuar...')

if __name__ == '__main__':
    main()
