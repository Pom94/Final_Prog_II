import requests
import json


"""___MENU PRIVADO___"""
def menuPrivado():
    while sesion != None:
        print("BIENVENIDO! ELIJA UNA OPCION:")
        print(" ")
        print("\t1) Peliculas.")
        print("\t2) Directores")
        print("\t3) Generos.")
        print(" ")
        print("\t0) Salir.")

        opcion = int(input())
        match opcion:
            case 1:
                menuPeliculas()
                break
            case 2:
                menuDirectores()
                break
            case 3:
                menuGeneros()
                break
            case 0:
                print("Hasta luego.")
                break
            case _:
                print("Opcion incorrecta.")



"___MENU PELICULAS___"""
def menuPeliculas():
    while True:
        print("\n\n-PELICULAS-")
        print("Elija una opcion:")
        print(" ")
        print("\t1) Buscar pelicula por titulo.")
        print("\t2) Buscar peliculas por un director particular.")
        print("\t3) Buscar peliculas con portadas.")
        print("\t4) Agregar una pelicula.")
        print("\t5) Borrar una pelicula.")
        print("\t6) Modificar una pelicula.")
        print("\t7) Puntuaciones.")
        print("\t8) Comentar una pelicula.")
        print(" ")
        print("\t0) Salir.")

        opcion = int(input())
        match opcion:
            case 1:
                print("-BUSCAR PELICULA-")
                peliculaBuscar = input("\tIngrese nombre de la pelicula a buscar: ")
                buscarPelicula(peliculaBuscar)
            case 2:
                print("-BUSCAR PELICULAS POR DIRECTOR-")
                director = input("\tIngrese el nombre del director: ")
                peliculaDirector(director)
            case 3:
                peliculaPortada()
            case 4:
                print("-AGREGAR PELICULA-")
                titulo = input("\tTitulo: ")
                anio = input("\tAnio: ")
                director = input("\tDirector: ")
                genero = input("\tGenero: ")
                sinopsis = input("\tSinopsis: ")
                imagen = input("\tImagen: ")
                agregarPelicula(titulo, anio, director, genero, sinopsis, imagen)
            case 5:
                print("-ELIMINAR PELICULA-")
                pelicula = input("\tTitulo: ")
                borrarPelicula(pelicula)
            case 6:
                print("-MODIFICAR PELICULA-")
                pelicula = input("\tIngrese nombre de la pelicula a modificar: ")
                titulo = input("\tTitulo: ")
                anio = input("\tAnio: ")
                director = input("\tDirector: ")
                genero = input("\tGenero: ")
                sinopsis = input("\tSinopsis: ")
                imagen = input("\tImagen: ")
                modificarPelicula(pelicula, titulo, anio, director, genero, sinopsis, imagen)
            case 7:
                menuPuntuar()
                break
            case 8:
                menuComentarios()
                break
            case 0:
                menuPrivado()
                break
            case _:
                print("Opcion incorrecta.")
            



"___BUSCADOR DE PELICULAS___"""
def buscarPelicula(peliculaBuscar):
    url = (f"http://localhost:5000/pelicula/{peliculaBuscar}/buscar")
    x = requests.get(url, cookies=sesion)

    if x.status_code == 200:        
        pelicula = x.json()
        
        print("\n\nPelicula: ")
        print("\t*" , pelicula['titulo'])
        print("\tAño:", pelicula['anio'])
        print("\tDirector:", pelicula['director'])
        print("\tGenero:", pelicula['genero'])
        print("\tSinopsis:", pelicula['sinopsis'])

        if len(pelicula['imagen']) > 0:
            print("\tPortada:", pelicula['imagen'])
        else:
            print("\tPortada: (No tiene portada registrada)")

        puntuaciones = pelicula['puntuacion']
        if puntuaciones:
            puntuacionesTotal = len(puntuaciones)
            suma = sum(puntuacion['puntuacion'] for puntuacion in puntuaciones)
            promedio = suma / puntuacionesTotal
            print("\tPuntuacion:", promedio)
        else:
            print("\tPuntuacion: (No ha sido puntuada)", )

        if len(pelicula['comentarios']) > 0:
            print("\tComentarios:")
            for comentario in pelicula['comentarios']:
                print("/t", comentario)
                print("")
        else:
            print("\tComentarios: (No tiene comentarios registrados.)")
            print("")

        print("\tVisitas:", pelicula['contador'])
    else:
        return ("Error.")



"""___DEVOLVER PELICULAS POR DIRECTOR___"""

def peliculaDirector(director):
    
    url= (f"http://localhost:5000/peliculas por director/{director}")
    x = requests.get(url, cookies=sesion)

    if x.status_code == 200:        
        peliculas = x.json()
        #print(peliculas)

        print("\n\n\tPeliculas dirigidas por ", director, ": ")
        for pelicula in peliculas:
            print("*" , pelicula['titulo'])
            print("\tAño:", pelicula['anio'])
            print("\tDirector:", pelicula['director'])
            print("\tGenero:", pelicula['genero'])
            print("\tSinopsis:", pelicula['sinopsis'])

            if len(pelicula['imagen']) > 0:
                print("\tPortada:", pelicula['imagen'])
            else:
                print("\tPortada: (No tiene portada registrada)")

            puntuaciones = pelicula['puntuacion']
            if puntuaciones:
                puntuacionesTotal = len(puntuaciones)
                suma = sum(puntuacion['puntuacion'] for puntuacion in puntuaciones)
                promedio = suma / puntuacionesTotal
                print("\tPuntuacion:", promedio)
            else:
                print("\tPuntuacion: (No ha sido puntuada)", )

            if len(pelicula['comentarios']) > 0:
                print("\tComentarios:")
                for comentario in pelicula['comentarios']:
                    print("/t'", comentario, "'")
                    print("")
            else:
                print("\tComentarios: (No tiene comentarios registrados.)")
                print("")

            print("\tVisitas:", pelicula['contador'])
    else:
        return ("Error.")



"""___DEVOLVER LISTA DE PELICULAS CON IMAGEN DE PORTADA___"""
def peliculaPortada():
    url= ("http://localhost:5000/peliculas con portada")
    x = requests.get(url, cookies=sesion)

    if x.status_code == 200:
        peliculas = x.json()

        print("\n\n\n\tPeliculas con portada: ")
        for pelicula in peliculas:
            print("*" , pelicula['titulo'])
            print("\tAño:", pelicula['anio'])
            print("\tDirector:", pelicula['director'])
            print("\tGenero:", pelicula['genero'])
            print("\tSinopsis:", pelicula['sinopsis'])
            print("\tPortada:", pelicula['imagen'])

            puntuaciones = pelicula['puntuacion']
            if puntuaciones:
                puntuacionesTotal = len(puntuaciones)
                suma = sum(puntuacion['puntuacion'] for puntuacion in puntuaciones)
                promedio = suma / puntuacionesTotal
                print("\tPuntuacion:", promedio)
            else:
                print("\tPuntuacion: (No ha sido puntuada)", )

            if len(pelicula['comentarios']) > 0:
                print("\tComentarios:")
                for comentario in pelicula['comentarios']:
                    print("/t", comentario)
                    print("")
            else:
                print("\tComentarios: (No tiene comentarios registrados.)")
                print("")

            print("\tVisitas:", pelicula['contador'])
    else:
        return ("Error.")



    
"""___AGREGAR PELICULAS___"""
def agregarPelicula(titulo, anio, director, genero, sinopsis, imagen, ):

    pelicula = {"titulo": titulo, "anio": anio, "director": director, "genero": genero, "sinopsis": sinopsis, "imagen": imagen, "comentario": [], "puntuacion": [], "puntuaciones totales": 0, "contador": 0}
    x = requests.post("http://localhost:5000/agregar pelicula", json=pelicula, cookies=sesion)

    if x.status_code == 200:
        print ("Pelicula agregada.")
    else:
        print("Error.")
    


"""___ELIMINAR PELICULA___"""
def borrarPelicula(pelicula):
    peliculaBorrar = {'titulo': pelicula}

    url = (f"http://localhost:5000/{pelicula}/borrar")
    x = requests.delete(url, json=peliculaBorrar, cookies=sesion)

    if x.status_code == 200:
        return ("Pelicula eliminada.")
    else:
        return("Error.")




"""___EDITAR PELICULA___""" 
def modificarPelicula(pelicula, titulo, anio, director, genero, sinopsis, imagen):

    peliculaNueva = {"titulo": titulo, "anio": anio, "director": director, "genero": genero, "sinopsis": sinopsis, "imagen": imagen}

    url = (f"http://localhost:5000/{pelicula}/editar")
    x = requests.put(url, json=peliculaNueva, cookies=sesion)

    if x.status_code == 201:
        return ("Pelicula modificada.")
    else:
        return("Error.")
    




"""___MENU DIRECTORES___"""
def menuDirectores():
    while True:
        print("\n\n\n-DIRECTORES-")
        print("Elija una opcion:")
        print(" ")
        print("\t1) Buscar un director.")
        print("\t2) Lista de directores registrados.")
        print("\t3) Agregar un director.")
        print("\t4) Borrar un director.")
        print("\t5) Modificar un director.")
        print(" ")
        print("\t0) Salir.")

        opcion = int(input())
        match opcion:
            case 1:
                print("\n\n-BUSCAR DIRECTOR-")
                director = input("\tIngrese el nombre del director: ")
                buscardirector(director)
            case 2:
                listaDirectores()
            case 3:
                print("-AGREGAR DIRECTOR-")
                director = input("\tIngrese el nombre del director: ")
                altaDirector(director)
            case 4:
                print("-BORRAR DIRECTOR-")
                director = input("\tIngrese el nombre del director: ")
                borrarDirector(director)
            case 5:
                print("-MODIFICAR DIRECTOR-")
                directorAnterior= input("\tIngrese el nombre del director a modificar: ")
                directorModificado= input("\tIngrese el nuevo nombre: ")
                modificarDirector(directorAnterior, directorModificado)
            case 0:
                menuPrivado()
                break
            case _:
                print("Opcion incorrecta.")


"""___BUSCAR DIRECTOR___"""
def buscardirector(director):
    url = (f"http://localhost:5000/director/{director}/buscar")
    x = requests.get(url, cookies=sesion)

    if x.status_code == 200:        
        director = x.json()
        print("\n\n\n\tDirector: ")
        print("\t", director)

    else:
        return ("Error.")
    


"""___LISTA DE DIRECTORES___"""
def listaDirectores():
    url = ("http://localhost:5000/directores")
    x = requests.get(url, cookies=sesion)

    if x.status_code == 200:        
        directores = x.json()
        print("\n\n\n\tDirectores: ")
        print("\t", directores)

    else:
        return ("Error.")
    

"""___ALTA DIRECTOR___"""
def altaDirector(director):

    directorNuevo = {"director": director}
    url = ("http://localhost:5000/director/alta")
    x = requests.post(url, json=directorNuevo, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\nDirector agregado.")
    else:
        return("Error.")
    

"""___ELIMINAR PELICULA___"""
def borrarDirector(director):

    directorEliminar = {"director": director}
    url = ("http://localhost:5000/director/baja")
    x = requests.delete(url, json=directorEliminar, cookies=sesion)

    if x.status_code == 200:
        return ("Director eliminado.")
    else:
        return("Error.")
    

"""___EDITAR DIRECTOR___""" 
def modificarDirector(directorAnterior, directorModificado):

    directorModificar = {"director anterior": directorAnterior, "director modificado": directorModificado}
    url = ("http://localhost:5000/director/modificar")
    x = requests.put(url, json=directorModificar, cookies=sesion)

    if x.status_code == 201:
        return ("Director modificado.")
    else:
        return("Error.")
    



"""___MENU PUNTUAR___"""
def menuPuntuar():
    while True:
        print("-PUNTUACION-")
        print("Elija una opcion:")
        print(" ")
        print("\t1) Agregar una puntuacion.")
        print("\t2) Borrar una puntuacion.")
        print("\t3) Modificar una puntuacion.")
        print(" ")
        print("\t0) Salir.")

        opcion = int(input())
        match opcion:
            case 1:
                print("\n\n\n-PUNTUAR-")
                pelicula = input("\tIngrese el nombre de la pelicula: ")
                puntuacion = int(input("\tIngrese la puntuacion: "))
                puntuarPelicula(pelicula, puntuacion)
            case 2:
                print("\n\n\n-ELIMINAR PUNTUACION-")
                pelicula = input("\tIngrese el nombre de la pelicula: ")
                puntuacionEliminar = int(input("\tIngrese la puntuacion: "))
                borrarPuntuacion(pelicula, puntuacionEliminar)
            case 3:
                print("\n\n\n-MODIFICAR PUNTUACION-")
                pelicula = input("\tIngrese el nombre de la pelicula: ")
                puntuacionNueva = int(input("\tIngrese la puntuacion: "))
                editarPuntuacion(pelicula, puntuacionNueva)
            case 0:
                menuPrivado()
                break
            case _:
                print("Opcion incorrecta.")



"""___PUNTUAR____"""
def puntuarPelicula(pelicula, puntuacion):

    puntuacion = {"puntuacion": puntuacion}
    url = (f"http://localhost:5000/pelicula/{pelicula}/puntuar")
    x = requests.post(url, json=puntuacion, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\tPuntuacion hecha.")
    else:
        error = x.json()
        print(error)
        return("Error.")
    




"""___ELIMINAR PUNTUACION___"""
def borrarPuntuacion(pelicula, puntuacion):

    url = (f"http://localhost:5000/pelicula/{pelicula}/eliminar puntuacion")
    puntuacionEliminar = {"puntuacion": puntuacion}    
    x = requests.delete(url, json=puntuacionEliminar, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\nPuntuacion eliminada.")
    else:
        error = x.json()
        print(error)
        return("Error.")
    



"""___EDITAR PUNTUACION___""" 
def editarPuntuacion(pelicula, puntuacion):

    url = (f"http://localhost:5000/pelicula/{pelicula}/editar puntuacion")
    puntuacionModificar = {"puntuacion": puntuacion}
    x = requests.put(url, json=puntuacionModificar, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\nPuntuacion modificada.")
    else:
        error = x.json()
        print("ERROR")
        print(error)
        return("Error.")
    


"""___MENU COMENTARIOS___"""
def menuComentarios():
    while True:
        print("-COMENTARIOS-")
        print("Elija una opcion:")
        print(" ")
        print("\t1) Agregar un comentario.")
        print("\t2) Borrar un comentario.")
        print("\t3) Modificar un comentario.")
        print(" ")
        print("\t0) Salir.")

        opcion = int(input())
        match opcion:
            case 1:
                print("\n\n\n-COMENTAR-")
                pelicula = input("\tIngrese el nombre de la pelicula: ")
                comentario = input("\tIngrese el comentario: ")
                comentarPelicula(pelicula, comentario)
            case 2:
                print("\n\n\n-ELIMINAR COMENTARIO-")
                pelicula = input("\tIngrese el nombre de la pelicula: ")
                borrarComentario(pelicula)
            case 3:
                print("\n\n\n-MODIFICAR COMENTARIO-")
                pelicula = input("\tIngrese el nombre de la pelicula: ")
                comentarioModificar = input("\tIngrese el comentario: ")
                editarComentario(pelicula, comentarioModificar)
            case 0:
                menuPrivado()
                break
            case _:
                print("Opcion incorrecta.")



"""___COMENTAR____"""
def comentarPelicula(pelicula, comentario):

    comentar = {"comentario": comentario}
    url = (f"http://localhost:5000/pelicula/{pelicula}/comentario")
    x = requests.post(url, json=comentar, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\Comentario hecho.")
    else:
        error = x.json()
        print(error)
        return("Error.")
    




"""___ELIMINAR COMENTARIO___"""
def borrarComentario(pelicula):

    url = (f"http://localhost:5000/pelicula/{pelicula}/comentario/eliminar") 
    x = requests.delete(url, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\nComentario eliminada.")
    else:
        error = x.json()
        print(error)
        return("Error.")
    



"""___EDITAR COMENTARIO___""" 
def editarComentario(pelicula, comentario):

    url = (f"http://localhost:5000/pelicula/{pelicula}/comentario/editar")
    comentarioModificar = {"comentario": comentario}
    x = requests.put(url, json=comentarioModificar, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\nComentario modificado.")
    else:
        error = x.json()
        print("ERROR")
        print(error)
        return("Error.")



"""___MENU GENEROS___"""
def menuGeneros():
    while True:
        print("-GENEROS-")
        print("Elija una opcion:")
        print(" ")
        print("\t1) Lista de generos registrados.")
        print("\t2) Agregar un genero.")
        print("\t3) Borrar un genero.")
        print("\t4) Modificar un genero.")
        print(" ")
        print("\t0) Salir.")

        opcion = int(input())
        match opcion:
            case 1:
                listaGeneros()
            case 2:
                print("-AGREGAR GENERO-")
                genero = input("\tIngrese el nombre del genero: ")
                altaGenero(genero)
            case 3:
                print("-BORRAR GENERO-")
                genero = input("\tIngrese el nombre del genero a borrar: ")
                borrarGenero(genero)
            case 4:
                print("-MODIFICAR GENERO-")
                generoAnterior= input("\tIngrese el nombre del genero a modificar: ")
                generoModificado= input("\tIngrese el nuevo nombre: ")
                modificarGenero(generoAnterior, generoModificado)
            case 0:
                menuPrivado()
                break
            case _:
                print("Opcion incorrecta.")



"""___LISTA DE GENEROS___"""
def listaGeneros():
    url = ("http://localhost:5000/generos")
    x = requests.get(url, cookies=sesion)

    if x.status_code == 200:        
        generos = x.json()
        print("\n\n\n\t-GENEROS-")
        print("\t", generos)

    else:
        return ("Error.")
    

"""___ALTA GENERO___"""
def altaGenero(genero):

    url = ("http://localhost:5000/genero/alta")
    genero = {"genero": genero}
    x = requests.post(url, json=genero, cookies=sesion)

    if x.status_code == 200:
        return ("\n\n\nGenero agregado.")
    else:
        return("Error.")
    

"""___ELIMINAR GENERO___"""
def borrarGenero(genero):

    url = ("http://localhost:5000/genero/baja")
    generoEliminar = {"genero": genero}    
    x = requests.delete(url, json=generoEliminar, cookies=sesion)

    if x.status_code == 200:
        return ("Genero eliminado.")
    else:
        return("Error.")
    

"""___EDITAR GENERO___""" 
def modificarGenero(generoAnterior, generoModificado):

    generoModificar= {"genero anterior": generoAnterior, "genero modificado": generoModificado}
    url = ("http://localhost:5000/genero/modificar")
    x = requests.put(url, json=generoModificar, cookies=sesion)

    if x.status_code == 201:
        return ("Genero modificado.")
    else:
        return("Error.")
        





sesion = None

"""___INICIAR SESION___"""
def inciarSesion(usuario, contraseña):

    global sesion
    datos = {"usuario": usuario, "contraseña": contraseña}

    x = requests.post("http://localhost:5000/iniciar sesion", json=datos)

    if x.status_code == 200:
        sesion = x.cookies
        print("\n\nHa iniciado sesion.")
    else:
        print("El usuario y/o contraseña son incorrectos.")
    


"""___CERRAR SESION___"""

def cerrarSesion():

    x = requests.post("http://localhost:5000/cerrar sesion", cookies=sesion)
    if x.status_code == 200:
        sesion = None
        print("Ha cerrado sesion.")
    else:
        print("No ha iniciado sesion.")



"""___REGISTRAR___"""
def registrar(usuario, contraseña):
    global sesion

    datos = {"usuario": usuario, "contraseña": contraseña}
    x = requests.post("http://localhost:5000/registrar", json=datos)

    if x.status_code == 200:
        sesion = x.cookies
        print("Se ha registrado correctamente..")
        return True
    else:
        print("No se puede registrar")




"""___VERIFICAR OPCION___"""




"""___MENU PUBLICO___"""
while True:
    print("BIENVENIDO! ELIJA UNA OPCION:")
    print(" ")
    print("\t1) Iniciar sesion.")
    print("\t2) Registrarse.")
    print("\t3) Cerrar Sesion.")
    print("\t4) Lista de las últimas 10 peliculas agregadas.")
    print(" ")
    print("\t0) Salir.")

    opcion = int(input())
    match opcion:
        case 1:
            usuario = input("Ingrese usuario: ")
            contraseña = input("Ingrese contraseña: ")
            inciarSesion(usuario, contraseña)
            menuPrivado()
        case 2:
            usuario = input("Ingrese usuario: ")
            contraseña = input("Ingrese contraseña: ")
            registrar(usuario, contraseña)
        case 3:
            cerrarSesion()
        case 4:
            publico = (requests.get("http://localhost:5000/publico")).json()

            for pelicula in publico:
                print("*" , pelicula['titulo'])
                print("\tAño:", pelicula['anio'])
                print("\tDirector:", pelicula['director'])
                print("\tGenero:", pelicula['genero'])
                print("\tSinopsis:", pelicula['sinopsis'])

                if len(pelicula['imagen']) > 0:
                    print("\tPortada:", pelicula['imagen'])
                else:
                    print("\tPortada: (No tiene portada registrada)")

                puntuaciones = pelicula['puntuacion']
                if puntuaciones:
                    puntuacionesTotal = len(puntuaciones)
                    suma = sum(puntuacion['puntuacion'] for puntuacion in puntuaciones)
                    promedio = suma / puntuacionesTotal
                    print("\tPuntuacion:", promedio)
                else:
                    print("\tPuntuacion: (No ha sido puntuada)", )

                if len(pelicula['comentarios']) > 0:
                    print("\tComentarios:")
                    for comentario in pelicula['comentarios']:
                        print("/t", comentario)
                        print("")
                else:
                    print("\tComentarios: (No tiene comentarios registrados.)")
                    print("")

                print("\tVisitas:", pelicula['contador'])
                
        case 0:
            print("Hasta luego.")
            break
        case _:
            print("Opcion incorrecta")