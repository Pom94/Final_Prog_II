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
        return jsonify({'mensaje': 'Ha iniciado sesión.'}), 200
    else:
        return jsonify({'mensaje': 'Usuario o contraseña incorrecta.'}), 400
    


"""___CERRAR SESION___"""
@app.route('/cerrar sesion', methods=['POST'])
def cerrarSesion():
    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesión.'}), 400
    session.pop('usuario', None)
    return jsonify({'mensaje': 'Ha cerrado su sesión.'}), 200




"""___REGISSTRAR___"""
@app.route('/registrar', methods=['POST'])
def registrar():
    datos = request.get_json()
    usuario = datos['usuario']
    contraseña = datos['contraseña']

    with open('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    usuarios[usuario] = contraseña

    if usuario in usuarios:
        return jsonify({'mensaje': 'El usuario ya existe.'}), 400

    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    return jsonify({'mensaje': 'Se ha registrado correctamente.'}), 200


    
    

"""___AGREGAR PELICULAS___"""

@app.route('/agregar pelicula', methods=['POST'])
def agregarPelicula():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))
    
    peliculaAgregar = request.get_json()
    nuevaPelicula = {
        'titulo': peliculaAgregar.get('titulo'),
        'anio': peliculaAgregar.get('anio'),
        'director': peliculaAgregar.get('director'),
        'genero': peliculaAgregar.get('genero'),
        'sinopsis': peliculaAgregar.get('sinopsis'),
        'imagen': peliculaAgregar.get('imagen'),
        "comentarios": [],
        "puntuacion": [],
        "puntuaciones totales": 0,
        "contador": 0
    }

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion.'}), 401
    
    if not nuevaPelicula['titulo'] or not nuevaPelicula['anio'] or not nuevaPelicula['director'] or not nuevaPelicula['genero'] or not nuevaPelicula['sinopsis'] or not nuevaPelicula['imagen']:
        return jsonify({'mensaje': 'Faltan datos.'}), 400


    for pelicula in peliculas:
        if pelicula['titulo'] == nuevaPelicula['titulo']:
            return jsonify({'mensaje': 'La pelicula ya existe.'}, paginado(peliculas, pagina, porPagina)), 400
        if nuevaPelicula['director'] not in directores or nuevaPelicula['genero'] not in generos :
            return jsonify({'mensaje': 'El director o genero de la pelicula no se encuentra.'}), 404
        
        peliculas.append(nuevaPelicula)

        with open('data/peliculas.json', 'w') as f:
            json.dump(peliculas, f)
        return jsonify({'mensaje': 'Su pelicula ha sido agregada'}, nuevaPelicula), 200
    


    

"""___DEVOLVER PELICULAS POR DIRECTOR___"""
@app.route('/peliculas por director/<string:director>', methods=['GET'])
def peliculasDirector(director):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 400
    else:
        peliculasDirector = [pelicula for pelicula in peliculas if pelicula['director'] == director]
        return jsonify(paginado(peliculasDirector, pagina, porPagina)), 200
    

    


"""___EDITAR PELICULA___"""        
@app.route('/<string:titulo>/editar', methods=['PUT'])    
def editarPelicula(titulo):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))
    
    peliculaVieja = request.get_json()
    nuevaPelicula = {
        'titulo': peliculaVieja.get('titulo'),
        'anio': peliculaVieja.get('anio'),
        'director': peliculaVieja.get('director'),
        'genero': peliculaVieja.get('genero'),
        'sinopsis': peliculaVieja.get('sinopsis'),
        'imagen': peliculaVieja.get('imagen'),
        "comentarios": [],
        "puntuacion": [],
        "puntuaciones totales": 0,
        "contador": 0
    }

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 401
    
    if not peliculaVieja or not nuevaPelicula['titulo'] or not nuevaPelicula['anio'] or not nuevaPelicula['director'] or not nuevaPelicula['genero'] or not nuevaPelicula['sinopsis'] or not nuevaPelicula['imagen']:
        return jsonify({'mensaje': 'Faltan datos.'}), 400

    peliculaEditar = None
    for pelicula in peliculas:        
        if nuevaPelicula['director'] not in directores or nuevaPelicula['genero'] not in generos :
            return jsonify({'mensaje': 'El director o genero de la pelicula no se encuentra.'}), 404
        if pelicula['titulo'] == titulo and len(pelicula['comentarios']) > 0:
            return jsonify({'mensaje': 'No se puede editar pelicula que contengan comentarios ya hechos.'}, pelicula), 401
        if pelicula['titulo'] == titulo and nuevaPelicula['titulo'] == titulo:
            peliculaEditar = pelicula
            peliculas.remove(pelicula)
            peliculas.append(peliculaEditar)
            with open('data/peliculas.json', 'w') as f:
                json.dump(peliculas, f)
            return jsonify({'mensaje': 'La pelicula fue editada.'}, pelicula), 200
    return jsonify({'mensaje': 'No se encontro pelicula'}, paginado(peliculas, pagina, porPagina)), 404

    
        

"""___ELIMINAR PELICULA___"""
@app.route('/<string:titulo>/borrar', methods=['DELETE'])  
def borrarPelicula(titulo):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    peliculaE = request.get_json()
    peliculaEliminar = peliculaE.get('titulo')

    with open('data/peliculas.json', 'r') as f:
        peliculas  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 401
    if not peliculaEliminar:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    for pelicula in peliculas:
        if pelicula['titulo'] == titulo and len(pelicula['comentarios']) > 0:
            return jsonify({'mensaje': 'No se puede eliminar pelicula que contengan comentarios ya hechos.'}, pelicula), 401
        if pelicula['titulo'] == titulo and len(pelicula['comentarios']) == 0:
            peliculas.remove(pelicula)
            with open('data/peliculas.json', 'w') as f:
                json.dump(peliculas, f)
            return jsonify({'mensaje': 'La pelicula fue eliminada.'}, paginado(peliculas, pagina, porPagina)), 200        
    return jsonify({'mensaje': 'No se encontro pelicula'}, paginado(peliculas, pagina, porPagina)), 404
        
    

"""___DEVOLVER LISTA DE DIRECTORES___"""
@app.route('/directores', methods=['GET'])
def devolverDirectores():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 10))

    with open('data/directores.json', 'r') as f:
        directores = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 401
    else:
        return jsonify({'mensaje': 'Estos son los directores registrados en la plataforma'}, paginado(directores, pagina, porPagina)), 200




"""___DEVOLVER LISTA DE GENEROS___"""
@app.route('/generos', methods=['GET'])
def devolverGeneros():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 10))

    with open('data/generos.json', 'r') as f:
        generos = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 401
    else:
        return jsonify({'mensaje': 'Estos son los generos registrados en la plataforma'}, paginado(generos, pagina, porPagina)), 200
    



"""___ABM DE GENEROS___"""
"""___ALTA___"""
@app.route('/genero/alta', methods=['POST'])
def altaGenero():
    datos = request.get_json()
    generoNuevo = datos.get('genero')

    if not generoNuevo:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if generoNuevo in generos:
        return jsonify({'mensaje': "El genero ya existe."}), 400
        
    generos.append(generoNuevo)

    with open('data/generos.json', 'w') as f:
        json.dump(generos, f)

    return jsonify({'mensaje': 'Genero registrado.'}), 200



"""___BAJA___"""
@app.route('/genero/baja', methods=['DELETE'])
def bajaGenero():
    datos = request.get_json()
    generoEliminar = datos.get('genero')

    if not generoEliminar:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if generoEliminar not in generos:
        return jsonify({'mensaje': "El genero no existe."}), 400
        
    generos.remove(generoEliminar)

    with open('data/generos.json', 'w') as f:
        json.dump(generos, f)

    return jsonify({'mensaje': 'Genero eliminado.'}), 200



"""___MODIFICAR___"""
@app.route('/genero/modificar', methods=['PUT'])
def modificarGenero():
    datos = request.get_json()
    generoViejo = datos.get('genero anterior')
    generoNuevo = datos.get('genero modificado')

    if not generoViejo or not generoNuevo:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    with open('data/generos.json', 'r') as f:
        generos  = json.load(f)

    if generoViejo not in generos:
        return jsonify({'mensaje': "El genero no existe."}), 400
        
    generos.remove(generoViejo)
    generos.append(generoNuevo)

    with open('data/generos.json', 'w') as f:
        json.dump(generos, f)

    return jsonify({'mensaje': 'Genero modificado.'}), 200


    


    
"""___DEVOLVER LISTA DE PELICULAS CON IMAGEN DE PORTADA___"""
@app.route('/peliculas con portada', methods=['GET'])
def devolverPeliculasPortada():

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 401
    else:
        peliculasPortada = [pelicula for pelicula in peliculas if pelicula['imagen'] != ""]
        return jsonify(paginado(peliculasPortada, pagina, porPagina)), 200
    




"""___PAGINADO___"""
def paginado(i, pagina, porPagina):

    comienzo = (pagina - 1) * porPagina
    final = comienzo + porPagina

    subconjunto = i[comienzo:final]
    return subconjunto




"""___BUSCADOR DE PELICULAS___"""
"""@app.route('/pelicula/<string:titulo>/buscar', methods=['GET'])
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
        return jsonify({'mensaje': 'No se encontro pelicula'}, paginado(peliculas, pagina, porPagina))"""
    


"""___BUSCADOR DE DIRECTORES___"""
@app.route('/director/<string:director>/buscar', methods=['GET'])
def buscarDirector(director):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 10))

    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)

    if 'usuario' not in session:
        return jsonify({'mensaje': 'No ha iniciado sesion'}), 401
    else:
        for i in directores:
            if i == director:
                return jsonify(i), 200
        return jsonify({'mensaje': 'No se encontro director'}, paginado(directores, pagina, porPagina)), 404
    


"""___ABM DE DIRECTORES___"""
"""___ALTA___"""
@app.route('/director/alta', methods=['POST'])
def altaDirector():
    datos = request.get_json()
    directorNuevo = datos.get('director')

    if not directorNuevo:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)

    if directorNuevo in directores:
        return jsonify({'mensaje': "El director ya existe."}), 400
        
    directores.append(directorNuevo)

    with open('data/directores.json', 'w') as f:
        json.dump(directores, f)

    return jsonify({'mensaje': 'Director registrado.'}), 200



"""___BAJA___"""
@app.route('/director/baja', methods=['DELETE'])
def bajaDirector():
    datos = request.get_json()
    directorEliminar = datos.get('director')

    if not directorEliminar:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)

    if directorEliminar not in directores:
        return jsonify({'mensaje': "El director no existe."}), 404
        
    directores.remove(directorEliminar)

    with open('data/directores.json', 'w') as f:
        json.dump(directores, f)

    return jsonify({'mensaje': 'Director eliminado.'}), 200



"""___MODIFICAR___"""
@app.route('/director/modificar', methods=['PUT'])
def modificarDirector():
    datos = request.get_json()
    directorViejo = datos.get('director anterior')
    directoNuevo = datos.get('director modificado')

    if not directorViejo or not directoNuevo:
        return jsonify({'mensaje': 'Faltan datos.'}), 400
    
    with open('data/directores.json', 'r') as f:
        directores  = json.load(f)

    if directorViejo not in directores:
        return jsonify({'mensaje': "El director no existe."}), 404
        
    directores.remove(directorViejo)
    directores.append(directoNuevo)

    with open('data/directores.json', 'w') as f:
        json.dump(directores, f)

    return jsonify({'mensaje': 'Director modificado.'}), 200





"""___ABM DE USUARIOS___"""
"""___ALTA___"""
@app.route('/registrar', methods=['POST'])
def altaUsuario():

    usuarioNuevo = request.get_json('usuario')
    contraseñaNueva = request.get_json('contraseña')

    if not usuarioNuevo or not contraseñaNueva:
        return jsonify({'mensaje': 'Faltan datos'}), 400
    
    with open('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuarioNuevo['usuario'] in usuarios:
        return jsonify({'mensaje': 'El nombre de usuario ya existe.'}), 400
    
    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    return jsonify({'mensaje': 'El usuario ha sido registrado.'}), 200


"""___BAJA___"""
@app.route('/baja', methods=['DELETE'])
def bajaUsuario():
    usuarioBaja = request.get_json()
    usuarioEliminar = usuarioBaja.get('usuario')
    contraseñaEliminar = usuarioBaja.get('contraseña')

    if not usuarioEliminar or not contraseñaEliminar:
        return jsonify({'mensaje': 'Faltan datos'}), 400
    
    with open ('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuarioEliminar not in usuarios or usuarios[usuarioEliminar] != contraseñaEliminar:
        return jsonify({'mensaje': 'El nombre de usuario y/o contraseña no son correctos.'}), 400
    
    
    usuarios = {usuario:contraseña for usuario, contraseña in usuarios.items() if usuario != usuarioEliminar and contraseña != contraseñaEliminar}

    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    if len(usuarios) == len(usuarioBaja):
        return jsonify({'mensaje': 'El usuario ha sido eliminado'}), 200


"""___MODIFICAR___"""
@app.route('/modificar', methods=['PUT'])
def moficarUsuario():
    usuarioModificar = request.get_json()
    usuarioNuevo = usuarioModificar.get('usuario')
    contraseñaNueva = usuarioModificar.get('contraseña')

    if not usuarioNuevo or not contraseñaNueva:
        return jsonify({'mensaje': 'Faltan datos'}), 400
    
    with open ('data/usuarios.json', 'r') as f:
        usuarios = json.load(f)

    if usuarioNuevo not in usuarios:
        return jsonify({'mensaje': 'El nombre de usuario ya existe.'}), 400
    
    usuarios[usuarioNuevo] = contraseñaNueva

    with open('data/usuarios.json', 'w') as f:
        json.dump(usuarios, f)

    return jsonify({'mensaje': 'El usuario ha sido modificado.'}), 200


"""___PUNTUACION___"""
"""___ALTA PUNTUACION___"""
@app.route('/pelicula/<string:titulo>/puntuar', methods=['POST'])
def puntuarPelicula(titulo):
    datos = request.get_json()
    puntuacion = datos.get('puntuacion')
    usuario = session.get('usuario')

    with open ('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)

    if not isinstance(puntuacion, int) or puntuacion < 0 or puntuacion > 10:
        return jsonify({'mensaje': 'La puntuación tiene que ser un entero entre 0 y 10.'}), 400
    
    for pelicula in peliculas:
        if pelicula['titulo'] == titulo:
            if 'usuario' in session:                
                puntuaciones = pelicula['puntuacion']
                for p in puntuaciones:
                    if usuario in p['usuarios']:
                        return jsonify({'mensaje': 'Ya has puntuado anteriormente esta pelicula.'}), 400
                pelicula['puntuaciones totales'] += 1
                puntuaciones.append({"puntuacion": puntuacion, "usuarios": [usuario]})
                
                with open ('data/peliculas.json', 'w') as f:
                    json.dump(peliculas, f)
                return jsonify({'mensaje': 'Ha puntuado la pelicula.'}, pelicula), 200
            else:
                return jsonify({'mensaje': 'No ha inciado sesion.'}), 401
    return jsonify({'mensaje': 'No se encontro la pelicula.'}), 404




"""___BAJA PUNTUACION___"""
@app.route('/pelicula/<string:titulo>/eliminar puntuacion', methods=['DELETE'])
def eliminarPuntuacion(titulo):
    datos = request.get_json()
    puntuacionEliminar = datos.get('puntuacion')
    usuario = session.get('usuario')

    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)

    for pelicula in peliculas:
        if pelicula['titulo'] == titulo:
            if 'usuario' in session:
                puntuaciones = pelicula['puntuacion']
                for puntuacion in puntuaciones:
                    if puntuacion['puntuacion'] == puntuacionEliminar and usuario in puntuacion['usuarios']:
                        puntuacion['usuarios'].remove(usuario)
                        pelicula['puntuaciones totales'] -= 1
                        if not puntuacion['usuarios']:
                            puntuaciones.remove(puntuacion)
                        with open('data/peliculas.json', 'w') as f:
                            json.dump(peliculas, f)
                        return jsonify({'mensaje': 'Puntuacion eliminada.'}), 200
                return jsonify({'mensaje': 'No se encontro puntuacion.'}), 404
            else:
                return jsonify({'mensaje': 'No ha iniciado sesion.'}), 401
    return jsonify({'mensaje': 'No se encontro la pelicula.'}), 404



"""___MODIFICAR PUNTUACION___"""
@app.route('/pelicula/<string:titulo>/editar puntuacion', methods=['PUT'])
def editarPuntuacion(titulo):
    datos = request.get_json()
    puntuacionNueva = datos.get('puntuacion')
    usuario = session.get('usuario')

    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)

    for pelicula in peliculas:
        if pelicula['titulo'] == titulo:
            puntuaciones = pelicula['puntuacion']
            for puntuacion in puntuaciones:
                if usuario in puntuacion['usuarios']:
                    puntuacion['puntuacion'] = puntuacionNueva
                    with open('data/peliculas.json', 'w') as f:
                        json.dump(peliculas, f)
                    return jsonify({'mensaje': 'Puntuacion editada.'}), 200
            return jsonify({'mensaje': 'No se encontro puntuacion para editar.'}), 404
    return jsonify({'mensaje': 'No se encontro la pelicula.'}), 404







"""___CONTADOR DE VISUALIZACIONES Y BUSCADOR DE PELICULAS___"""

@app.route('/pelicula/<string:titulo>/buscar', methods=['GET'])
def pelicula(titulo):

    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))

    with open ('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)

    for pelicula in peliculas:
        if pelicula['titulo'] == titulo:
            if 'usuario' in session:
                pelicula['contador'] += 1
                with open('peliculas.json', 'w') as f:
                    json.dump(peliculas, f)
                return jsonify(pelicula), 200
            else:
                return jsonify({'mensaje': 'No ha inciado sesion.'}), 401
    return jsonify({'mensaje': 'No se encontro la pelicula.'}, paginado(peliculas, pagina, porPagina)), 400

    






"""___RUTA PARA PAGINA PÚBLICA___"""

@app.route('/publico', methods=['GET'])
def devolverPublico():
    pagina = int(request.args.get('pagina', 1))
    porPagina = int(request.args.get('por pagina', 5))
    
    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)    

    peliculasPublicas = paginado(peliculas, pagina, porPagina)
    return jsonify(peliculasPublicas), 200


    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
