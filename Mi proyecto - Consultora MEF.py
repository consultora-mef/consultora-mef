from flask import Flask, render_template, request
import csv
from datetime import datetime
import os

app = Flask(__name__)

def guardar_en_excel(datos):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_nombre = os.path.join(base_dir, 'consultas.csv')
    archivo_existe = os.path.isfile(archivo_nombre)

    with open(archivo_nombre, mode='a', newline='', encoding='utf-8') as archivo:
        columnas = ['Fecha', 'Hora', 'Nombre', 'Email', 'Actividad', 'Mensaje']
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        if not archivo_existe:
            escritor.writeheader()
        escritor.writerow(datos)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    actividad = request.form.get('actividad')
    mensaje = request.form.get('mensaje')
    
    ahora = datetime.now()
    fecha = ahora.strftime('%d/%m/%Y')
    hora = ahora.strftime('%H:%M:%S')

    nueva_consulta = {
        'Fecha': fecha, 'Hora': hora, 'Nombre': nombre, 
        'Email': email, 'Actividad': actividad, 'Mensaje': mensaje
    }

    guardar_en_excel(nueva_consulta)
    
    print(f"\n[AVISO] NUEVA CONSULTA ESTRATÉGICA RECIBIDA DE: {nombre}\n")
    
    return render_template('exito.html', nombre_cliente=nombre)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')