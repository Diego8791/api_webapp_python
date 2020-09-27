#!/usr/bin/env python
'''
API Personas
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las personas registradas.

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
NOTA: Si es la primera vez que se lanza este programa crear la base de datos
entrando a la siguiente URL
http://127.0.0.1:5000/reset

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.0"

# Realizar HTTP POST --> https://www.codepunker.com/tools/http-requests

import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect
import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

import persona
from config import config


app = Flask(__name__)

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db = config('db', config_path_name)
server = config('server', config_path_name)

persona.db = db


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /reset --> borrar y crear la base de datos</h3>"
        result += "<h3>[GET] /personas --> mostrar la tabla de personas (el HTML)</h3>"
        result += "<h3>[POST] /personas --> enviar el JSON para completar la tabla</h3>"
        result += "<h3>[GET] /registro --> mostrar el HTML con el formulario de registro de persona</h3>"
        result += "<h3>[POST] /registro --> ingresar nuevo registro de pulsaciones por JSON</h3>"
        result += "<h3>[GET] /comparativa --> mostrar tabla con datos para gráfico"
        result += "<h3>[GET] /comparativa/gráfico --> mostrar un gráfico que compare cuantas personas hay de cada nacionalidad"

        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos
        persona.create_schema()
        result = "<h3>Base de datos re-generada!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/personas")
def personas():
    try:
        # Alumno: Implemente
        result = '''<h3>Alumno: Implementar la llamada
                    al HTML tabla.html
                    con render_template</h3>'''
        result = render_template('tabla.html')
        return result
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/personas/tabla")
def personas_tabla():
    try:
        # Mostrar todas las personas en JSON
        result = persona.report()
        return jsonify(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/comparativa")
def comparativa():
    try:
        # Mostrar todos los registros en um gráfico
        result = '''<h3>Implementar una función en persona.py
                    nationality_review</h3>'''
        result += '''<h3>Esa funcion debe devolver los datos que necesite
                    para implementar el grafico a mostrar</h3>'''
       
       # Tabla HTML, header y formato
        result += '<table border="1">'
        result += '<thead cellpadding="1.0" cellspacing="1.0">'
        result += '<tr>'
        result += '<th>Nombre</th>'
        result += '<th>Edad</th>'
        result += '<th>Nacionalidad</th>'
        result += '</tr>'
        
        data = persona.report()
        print(data)

        # return (result)

        for row in data:
        
            # Fila de una tabla HTML
            result += '<tr>'
            result += '<td>' + str(row['name']) + '</td>'
            result += '<td>' + str(row['age']) + '</td>'
            result += '<td>' + str(row['nationality']) + '</td>'
            result += '</tr>'

        # Fin de la tabla HTML
        result += '</thead cellpadding="0" cellspacing="0" >'
        result += '</table>'

        return (result)
              
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/comparativa/grafico")
def grafico():
    
    data = persona.report()
    print(data)
    nac_nombre, nac_cant = persona.graphics_factory(data)

    try:  
        # confección de gráfico
        fig = plt.figure()
        fig.suptitle('Nacionalidades', fontsize=16)
        ax = fig.add_subplot()
        ax.bar(nac_nombre, nac_cant, label='Nacionalidad')
        ax.legend()
        # plt.show()
        
        # convertir gráfico en imagen
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        try:
            return render_template('registro.html')
        except:
            return jsonify({'trace': traceback.format_exc()})
    
    if request.method == 'POST':
        try:
            # Alumno: Implemente
            # Obtener del HTTP POST JSON el nombre y los pulsos
                        
            name = str(request.json['name'])
            age = str(request.json['age'])
            nationality = str(request.json['nationality'])
            persona.insert(name, int(age), nationality)
            return Response(status=200)
        except:
            return jsonify({'trace': traceback.format_exc()})
    

if __name__ == '__main__':
    print('Servidor arriba!')

    app.run(host=server['host'],
            port=server['port'],
            debug=True)
