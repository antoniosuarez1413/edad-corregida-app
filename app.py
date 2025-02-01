from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def calcular_edad_corregida(fecha_nacimiento, fecha_consulta, edad_gestacional):
    # Convertir las fechas a objetos datetime
    fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    fecha_con = datetime.strptime(fecha_consulta, "%Y-%m-%d")

    # Calcular la edad cronológica en días
    edad_cronologica_dias = (fecha_con - fecha_nac).days

    # Convertir la edad cronológica a meses y días
    meses = edad_cronologica_dias // 30
    dias_restantes = edad_cronologica_dias % 30

    # Calcular las semanas de prematuridad
    semanas_prematuridad = 40 - edad_gestacional

    # Convertir la edad cronológica a semanas
    edad_cronologica_semanas = meses * 4

    # Calcular la edad corregida en semanas
    edad_corregida_semanas = edad_cronologica_semanas - semanas_prematuridad

    # Convertir la edad corregida a meses y días
    edad_corregida_dias = edad_corregida_semanas * 7
    meses_corregidos = edad_corregida_dias // 30
    dias_corregidos = edad_corregida_dias % 30

    # Resultados
    resultados = {
        "edad_cronologica": {
            "dias": edad_cronologica_dias,
            "meses": meses,
            "dias_restantes": dias_restantes
        },
        "edad_corregida": {
            "semanas": edad_corregida_semanas,
            "meses": meses_corregidos,
            "dias": dias_corregidos
        }
    }
    return resultados

@app.route('/calcular', methods=['GET'])
def calcular():
    # Obtener los parámetros de la URL
    fecha_nacimiento = request.args.get('fecha_nacimiento')
    fecha_consulta = request.args.get('fecha_consulta')
    edad_gestacional = int(request.args.get('edad_gestacional'))

    # Calcular la edad corregida
    resultados = calcular_edad_corregida(fecha_nacimiento, fecha_consulta, edad_gestacional)

    # Devolver los resultados en formato JSON
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)