from flask import Flask, jsonify, request
import json

app = Flask(__name__)

"""___INICIAR SESION___"""

@app.route('/iniciar sesion', methods=['POST'])
def iniciarSesion():
    datos = request.get_json()
    usuario = datos['usuario']
    contraseña = datos['contraseña']

    with open('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuario in usuarios and usuarios[usuario] == contraseña:
        return jsonify({'mensaje': 'Ha iniciado sesión.'})
    else:
        return jsonify({'mensaje': 'Usuario o contraseña incorrecta.'})
    
    
    

"""___AGREGAR PELICULAS___"""

@app.route('/agregar pelicula', methods=['POST'])
def agregarPelicula():
    peliculaAgregar = request.get_json()

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    for pelicula in peliculas:
        if pelicula['titulo'] == peliculaAgregar['titulo']:
            return jsonify({'mensaje': 'La pelicula ya existe.'}, peliculas)
        elif peliculaAgregar['director'] in directores or peliculaAgregar['genero'] in generos :
            peliculaAgregar['comentarios'] = [peliculaAgregar['comentario']]
            del peliculaAgregar['comentario']
            peliculas.append(peliculaAgregar)
            return jsonify({'mensaje': 'Su pelicula ha sido agregada'}, peliculas)
    
    return jsonify({'mensaje': 'El director o genero de la pelicula no se encuentra.'})


    

"""___DEVOLVER PELICULAS POR DIRECTOR___"""
@app.route('/peliculas por director/<string:director>', methods=['GET'])
def peliculasDirector(director):
    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)

    peliculasDirector = [pelicula for pelicula in peliculas if pelicula['director'] == director]

    return jsonify(peliculasDirector)

    


"""___EDITAR PELICULA___"""        
@app.route('/editar/<string:titulo>', methods=['PUT'])    
def editarPelicula(titulo):
    peliculaEditar = request.get_json()

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)
    
    for pelicula in peliculas:
        if 'titulo' not in peliculaEditar or 'anio' not in peliculaEditar or 'director' not in peliculaEditar or 'genero' not in peliculaEditar or 'sinopsis' not in peliculaEditar or 'imagen' not in peliculaEditar:
            return jsonify({'mensaje': 'Faltan datos de la pelicula.'})
        elif peliculaEditar['director'] not in directores or peliculaEditar['genero'] not in generos :
            return jsonify({'mensaje': 'El director o genero de la pelicula no se encuentra.'})
        elif pelicula['titulo'] == titulo and len(pelicula['comentarios']) > 0:
            return jsonify({'mensaje': 'No se puede editar pelicula que contengan comentarios ya hechos.'})
        elif pelicula['titulo'] == titulo and peliculaEditar['titulo'] == titulo:
            pelicula = peliculaEditar
            return jsonify({'mensaje': 'La pelicula fue editada.'}, pelicula)
        else:
            return jsonify({'mensaje': 'No se encontro pelicula'})

    
        





    
    





"""___RUTA PARA PAGINA PÚBLICA___"""

@app.route('/publico', methods=['GET'])
def devolverPublico():
    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)
    peliculasPublicas = peliculas
    return jsonify(peliculasPublicas)


    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
