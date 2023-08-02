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
        return jsonify({'mensaje': "Usuario o contraseña incorrecta."})
    
    



"""___RUTA PARA PAGINA PÚBLICA___"""

@app.route('/publico', methods=['GET'])
def devolverPublico():
    with open('data/peliculas.json', 'r') as f:
        peliculas = json.load(f)
    peliculasPublicas = peliculas
    return jsonify(peliculasPublicas)


    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
