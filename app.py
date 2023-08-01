from flask import Flask, jsonify

app = Flask(__name__)

from peliculas import peliculas

@app.route('/peliculas', methods=['GET'])
def devolverPeliculas():
    return jsonify({"peliculas": peliculas})


@app.route('/peliculas/<string:tituloPelicula>')
def devolverPelicula(tituloPelicula):
    peliculaEncontrada = [pelicula for pelicula in peliculas if pelicula['titulo'] == tituloPelicula]   
    if (len(peliculaEncontrada) > 0):
        return jsonify({"pelicula": peliculaEncontrada[0]})
    return jsonify({"mensaje": "No se encontro pelicula"})
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
