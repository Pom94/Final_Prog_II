from flask import Flask, jsonify, request, session
import json

app = Flask(__name__)
app.secret_key = 'pomela'


"""___INICIAR SESION___"""

@app.route('/iniciar sesion', methods=['POST'])
def iniciarSesion():
    datos = request.get_json()
    usuario = datos['usuario']
    contraseña = datos['contraseña']

    with open('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuario in usuarios and usuarios[usuario] == contraseña:
        session['usuario'] = usuario
        return jsonify({'mensaje': 'Ha iniciado sesión.'})
    else:
        return jsonify({'mensaje': 'Usuario o contraseña incorrecta.'})
    
    

"""___AGREGAR PELICULAS___"""

@app.route('/agregar pelicula', methods=['POST'])
def agregarPelicula():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))
    
    peliculaAgregar = request.get_json()

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:

        for pelicula in peliculas:
            if pelicula['titulo'] == peliculaAgregar['titulo']:
                return jsonify({'mensaje': 'La pelicula ya existe.'}, paginado(peliculas, pagina, porPagina))
            elif peliculaAgregar['director'] in directores or peliculaAgregar['genero'] in generos :
                peliculaAgregar['comentarios'] = [peliculaAgregar['comentario']]
                del peliculaAgregar['comentario']
                peliculas.append(peliculaAgregar)
                return jsonify({'mensaje': 'Su pelicula ha sido agregada'}, pelicula)
    
        return jsonify({'mensaje': 'El director o genero de la pelicula no se encuentra.'})


    

"""___DEVOLVER PELICULAS POR DIRECTOR___"""
@app.route('/peliculas por director/<string:director>', methods=['GET'])
def peliculasDirector(director):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        peliculasDirector = [pelicula for pelicula in peliculas if pelicula['director'] == director]
        return jsonify({'mensaje': 'Peliculas por director'}, paginado(peliculasDirector, pagina, porPagina))
    

    


"""___EDITAR PELICULA___"""        
@app.route('/editar/<string:titulo>', methods=['PUT'])    
def editarPelicula(titulo):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))
    
    peliculaEditar = request.get_json()

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        for pelicula in peliculas:
            if 'titulo' not in peliculaEditar or 'anio' not in peliculaEditar or 'director' not in peliculaEditar or 'genero' not in peliculaEditar or 'sinopsis' not in peliculaEditar or 'imagen' not in peliculaEditar:
                return jsonify({'mensaje': 'Faltan datos de la pelicula.'})
            elif peliculaEditar['director'] not in directores or peliculaEditar['genero'] not in generos :
                return jsonify({'mensaje': 'El director o genero de la pelicula no se encuentra.'})
            elif pelicula['titulo'] == titulo and len(pelicula['comentarios']) > 0:
                return jsonify({'mensaje': 'No se puede editar pelicula que contengan comentarios ya hechos.'}, pelicula)
            elif pelicula['titulo'] == titulo and peliculaEditar['titulo'] == titulo:
                pelicula = peliculaEditar
                return jsonify({'mensaje': 'La pelicula fue editada.'}, pelicula)
        return jsonify({'mensaje': 'No se encontro pelicula'}, paginado(peliculas, pagina, porPagina))

    
        

"""___ELIMINAR PELICULA___"""
@app.route('/<string:titulo>/borrar', methods=['DELETE'])  
def borrarPelicula(titulo):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        for pelicula in peliculas:
            if pelicula['titulo'] == titulo and len(pelicula['comentarios']) == 0:
                peliculas.remove(pelicula)
                return jsonify({'mensaje': 'La pelicula fue eliminada.'}, paginado(peliculas, pagina, porPagina))
            elif pelicula['titulo'] == titulo and len(pelicula['comentarios']) > 0:
                return jsonify({'mensaje': 'No se puede eliminar pelicula que contengan comentarios ya hechos.'}, pelicula)
        return jsonify({'mensaje': 'No se encontro pelicula'}, paginado(peliculas, pagina, porPagina))
        
    

"""___DEVOLVER LISTA DE DIRECTORES___"""
@app.route('/directores', methods=['GET'])
def devolverDirectores():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 10))

    with open('data/directores.json', 'r') as f:
        directores = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        return jsonify({'mensaje': 'Estos son los directores registrados en la plataforma'}, paginado(directores, pagina, porPagina))




"""___DEVOLVER LISTA DE GENEROS___"""
@app.route('/generos', methods=['GET'])
def devolverGeneros():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 10))

    with open('data/generos.json', 'r') as f:
        generos = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        return jsonify({'mensaje': 'Estos son los generos registrados en la plataforma'}, paginado(generos, pagina, porPagina))
    


    
"""___DEVOLVER LISTA DE PELICULAS CON IMAGEN DE PORTADA___"""
@app.route('/peliculas con portada', methods=['GET'])
def devolverPeliculasPortada():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        peliculasPortada = [pelicula for pelicula in peliculas if pelicula['imagen'] != ""]
        return jsonify({'mensaje': 'Peliculas que poseen imagen de portada.'}, paginado(peliculasPortada, pagina, porPagina))
    




"""___PAGINADO___"""
def paginado(i, pagina, porPagina):

    comienzo = (pagina - 1) * porPagina
    final = comienzo + porPagina

    subconjunto = i[comienzo:final]
    return subconjunto




"""___BUSCADOR DE PELICULAS___"""
@app.route('/pelicula/<string:titulo>/buscar', methods=['GET'])
def buscarPelicula(titulo):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        for pelicula in peliculas:
            if pelicula['titulo'] == titulo:
                return jsonify(pelicula)
        return jsonify({'mensaje': 'No se encontro pelicula'}, paginado(peliculas, pagina, porPagina))
    


"""___BUSCADOR DE DIRECTORES___"""
@app.route('/director/<string:director>/buscar', methods=['GET'])
def buscarDirector(director):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 10))

    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'})
    else:
        for i in directores:
            if i == director:
                return jsonify(i)
        return jsonify({'mensaje': 'No se encontro director'}, paginado(directores, pagina, porPagina))
    



"""___ABM DE USUARIOS___"""
"""___ALTA___"""
@app.route('/registrar', methods=['POST'])
def altaUsuario():

    usuarioNuevo = request.get_json('usuario')
    contraseñaNueva = request.get_json('contraseña')

    if not usuarioNuevo or not contraseñaNueva:
        return jsonify({'mensaje': 'Faltan datos'})
    
    with open('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuarioNuevo['usuario'] in usuarios:
        return jsonify({'mensaje': 'El nombre de usuario ya existe.'})
    
    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    return jsonify({'mensaje': 'El usuario ha sido registrado.'})


"""___BAJA___"""
@app.route('/baja', methods=['DELETE'])
def bajaUsuario():
    usuarioBaja = request.get_json()
    usuarioEliminar = usuarioBaja.get('usuario')
    contraseñaEliminar = usuarioBaja.get('contraseña')

    if not usuarioEliminar or not contraseñaEliminar:
        return jsonify({'mensaje': 'Faltan datos'})
    
    with open ('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuarioEliminar not in usuarios or usuarios[usuarioEliminar] != contraseñaEliminar:
        return jsonify({'mensaje': 'El nombre de usuario y/o contraseña no son correctos.'})
    
    
    usuarios = {usuario:contraseña for usuario, contraseña in usuarios.items() if usuario != usuarioEliminar and contraseña != contraseñaEliminar}

    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    if len(usuarios) == len(usuarioBaja):
        return jsonify({'mensaje': 'El usuario ha sido eliminado'})


"""___MODIFICAR___"""
@app.route('/modificar', methods=['PUT'])
def moficarUsuario():
    usuarioModificar = request.get_json()
    usuarioNuevo = usuarioModificar.get('usuario')
    contraseñaNueva = usuarioModificar.get('contraseña')

    if not usuarioNuevo or not contraseñaNueva:
        return jsonify({'mensaje': 'Faltan datos'})
    
    with open ('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuarioNuevo not in usuarios:
        return jsonify({'mensaje': 'El nombre de usuario ya existe.'})
    
    usuarios[usuarioNuevo] = contraseñaNueva

    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    return jsonify({'mensaje': 'El usuario ha sido modificado.'})

    
    
    



 


"""___RUTA PARA PAGINA PÚBLICA___"""

@app.route('/publico', methods=['GET'])
def devolverPublico():
    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))
    
    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)    

    peliculasPublicas = paginado(peliculas, pagina, porPagina)
    return jsonify(peliculasPublicas)


    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
