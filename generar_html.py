import csv
import random
import datetime
import statistics
from collections import Counter
import os

# Nombres de agentes simulados
NOMBRES_AGENTES = [
    "Ana García", "Carlos López", "María Rodríguez", "Juan Pérez", "Laura Martín",
    "Diego Silva", "Carmen Ruiz", "Roberto Torres", "Elena Vásquez", "Miguel Herrera"
]

ESTADOS_LLAMADA = ["En curso", "Finalizada", "Por finalizar"]

def crear_directorios():
    """Crea las carpetas necesarias si no existen"""
    carpetas = ['data', 'templates', 'static/css']
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)

def generar_hora_realista():
    """Genera horas con mayor probabilidad en horario laboral"""
    hora_base = datetime.datetime.now().replace(hour=8, minute=0, second=0)
    
    # Mayor probabilidad entre 9-12 y 14-17 horas
    probabilidades = [0.05, 0.15, 0.20, 0.15, 0.10, 0.05, 0.15, 0.10, 0.05]
    hora_offset = random.choices(range(9), weights=probabilidades)[0]
    
    minutos = random.randint(0, 59)
    segundos = random.randint(0, 59)
    
    return hora_base + datetime.timedelta(hours=hora_offset, minutes=minutos, seconds=segundos)

def generar_llamadas(num_llamadas=50):
    """Genera datos simulados de llamadas"""
    llamadas = []
    
    for i in range(num_llamadas):
        agente = random.choice(NOMBRES_AGENTES)
        duracion = random.randint(30, 600)  # 30 segundos a 10 minutos
        estado = random.choices(
            ESTADOS_LLAMADA, 
            weights=[0.3, 0.6, 0.1]  # Más llamadas finalizadas
        )[0]
        hora_inicio = generar_hora_realista()
        
        llamada = {
            'id': f"CALL-{i+1:03d}",
            'agente': agente,
            'duracion': duracion,
            'estado': estado,
            'hora_inicio': hora_inicio.strftime("%H:%M:%S")
        }
        llamadas.append(llamada)
    
    return llamadas

def guardar_datos_csv(llamadas):
    """Guarda los datos en archivo CSV"""
    with open('data/llamadas.csv', 'w', newline='', encoding='utf-8') as archivo:
        campos = ['id', 'agente', 'duracion', 'estado', 'hora_inicio']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(llamadas)

def calcular_estadisticas(llamadas):
    """Calcula estadísticas de las llamadas"""
    total_llamadas = len(llamadas)
    duraciones = [llamada['duracion'] for llamada in llamadas]
    duracion_promedio = statistics.mean(duraciones) if duraciones else 0
    
    estados = [llamada['estado'] for llamada in llamadas]
    contador_estados = Counter(estados)
    
    return {
        'total': total_llamadas,
        'duracion_promedio': round(duracion_promedio, 2),
        'estados': dict(contador_estados)
    }

def formatear_duracion(segundos):
    """Convierte segundos a formato mm:ss"""
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    return f"{minutos:02d}:{segundos_restantes:02d}"

def generar_pagina_inicio(estadisticas):
    """Genera la página principal con resumen"""
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Call Center UTP - Simulador</title>
    <link rel="stylesheet" href="../static/css/styles.css">
</head>
<body>
    <header>
        <h1>🎯 Call Center UTP</h1>
        <p>Simulador de Llamadas Académico</p>
    </header>
    
    <nav>
        <a href="inicio.html" class="active">Inicio</a>
        <a href="resumen.html">Resumen</a>
        <a href="tabla.html">Tabla de Llamadas</a>
    </nav>
    
    <main>
        <div class="dashboard">
            <div class="card">
                <h3>📞 Total de Llamadas</h3>
                <div class="metric">{total}</div>
            </div>
            
            <div class="card">
                <h3>⏱️ Duración Promedio</h3>
                <div class="metric">{duracion_promedio}s</div>
            </div>
            
            <div class="card">
                <h3>📊 Estados</h3>
                <div class="estados">
                    <div class="estado en-curso">En curso: {en_curso}</div>
                    <div class="estado finalizada">Finalizadas: {finalizadas}</div>
                    <div class="estado por-finalizar">Por finalizar: {por_finalizar}</div>
                </div>
            </div>
        </div>
        
        <div class="acciones">
            <button onclick="simularNuevaLlamada()" class="btn-principal">
                🔄 Simular Nueva Llamada
            </button>
        </div>
    </main>
    
    <script>
        function simularNuevaLlamada() {{
            alert('Generando nuevos datos...');
            // En un entorno real, esto ejecutaría el script Python
            location.reload();
        }}
    </script>
</body>
</html>""".format(
        total=estadisticas['total'],
        duracion_promedio=estadisticas['duracion_promedio'],
        en_curso=estadisticas['estados'].get('En curso', 0),
        finalizadas=estadisticas['estados'].get('Finalizada', 0),
        por_finalizar=estadisticas['estados'].get('Por finalizar', 0)
    )
    
    with open('templates/inicio.html', 'w', encoding='utf-8') as archivo:
        archivo.write(html_content)

def generar_pagina_resumen(estadisticas, llamadas):
    """Genera la página de resumen detallado"""
    agentes_activos = len(set(llamada['agente'] for llamada in llamadas))
    
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resumen - Call Center UTP</title>
    <link rel="stylesheet" href="../static/css/styles.css">
</head>
<body>
    <header>
        <h1>📊 Resumen Detallado</h1>
    </header>
    
    <nav>
        <a href="inicio.html">Inicio</a>
        <a href="resumen.html" class="active">Resumen</a>
        <a href="tabla.html">Tabla de Llamadas</a>
    </nav>
    
    <main>
        <div class="resumen-grid">
            <div class="card">
                <h3>Métricas Generales</h3>
                <ul>
                    <li>Total de llamadas: <strong>{total}</strong></li>
                    <li>Agentes activos: <strong>{agentes_activos}</strong></li>
                    <li>Duración promedio: <strong>{duracion_promedio}s</strong></li>
                </ul>
            </div>
            
            <div class="card">
                <h3>Distribución por Estado</h3>
                <div class="estado-detalle">
                    <div class="barra en-curso" style="width: {porcentaje_en_curso}%">
                        En curso: {en_curso} ({porcentaje_en_curso:.1f}%)
                    </div>
                    <div class="barra finalizada" style="width: {porcentaje_finalizadas}%">
                        Finalizadas: {finalizadas} ({porcentaje_finalizadas:.1f}%)
                    </div>
                    <div class="barra por-finalizar" style="width: {porcentaje_por_finalizar}%">
                        Por finalizar: {por_finalizar} ({porcentaje_por_finalizar:.1f}%)
                    </div>
                </div>
            </div>
        </div>
    </main>
</body>
</html>""".format(
        total=estadisticas['total'],
        agentes_activos=agentes_activos,
        duracion_promedio=estadisticas['duracion_promedio'],
        en_curso=estadisticas['estados'].get('En curso', 0),
        finalizadas=estadisticas['estados'].get('Finalizada', 0),
        por_finalizar=estadisticas['estados'].get('Por finalizar', 0),
        porcentaje_en_curso=(estadisticas['estados'].get('En curso', 0) / estadisticas['total']) * 100,
        porcentaje_finalizadas=(estadisticas['estados'].get('Finalizada', 0) / estadisticas['total']) * 100,
        porcentaje_por_finalizar=(estadisticas['estados'].get('Por finalizar', 0) / estadisticas['total']) * 100
    )
    
    with open('templates/resumen.html', 'w', encoding='utf-8') as archivo:
        archivo.write(html_content)

def generar_pagina_tabla(llamadas):
    """Genera la página con tabla de llamadas"""
    filas_tabla = ""
    for llamada in llamadas:
        clase_estado = llamada['estado'].lower().replace(' ', '-')
        filas_tabla += f"""
        <tr>
            <td>{llamada['id']}</td>
            <td>{llamada['agente']}</td>
            <td>{formatear_duracion(llamada['duracion'])}</td>
            <td><span class="estado {clase_estado}">{llamada['estado']}</span></td>
            <td>{llamada['hora_inicio']}</td>
        </tr>"""
    
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabla de Llamadas - Call Center UTP</title>
    <link rel="stylesheet" href="../static/css/styles.css">
</head>
<body>
    <header>
        <h1>📋 Tabla de Llamadas</h1>
    </header>
    
    <nav>
        <a href="inicio.html">Inicio</a>
        <a href="resumen.html">Resumen</a>
        <a href="tabla.html" class="active">Tabla de Llamadas</a>
    </nav>
    
    <main>
        <div class="tabla-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Agente</th>
                        <th>Duración</th>
                        <th>Estado</th>
                        <th>Hora Inicio</th>
                    </tr>
                </thead>
                <tbody>
                    {filas}
                </tbody>
            </table>
        </div>
    </main>
</body>
</html>""".format(filas=filas_tabla)
    
    with open('templates/tabla.html', 'w', encoding='utf-8') as archivo:
        archivo.write(html_content)

def generar_css():
    """Genera el archivo CSS minimalista"""
    css_content = """/* Estilos minimalistas para Call Center UTP */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

header {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    color: white;
    text-align: center;
    padding: 2rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

header p {
    font-size: 1.1rem;
    opacity: 0.9;
}

nav {
    background: white;
    padding: 1rem 0;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

nav a {
    text-decoration: none;
    color: #2c3e50;
    margin: 0 2rem;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: all 0.3s ease;
}

nav a:hover, nav a.active {
    background: #3498db;
    color: white;
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
}

.card h3 {
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

.metric {
    font-size: 3rem;
    font-weight: bold;
    color: #3498db;
    margin: 1rem 0;
}

.estados {
    text-align: left;
}

.estado {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border-radius: 5px;
    font-weight: bold;
}

.estado.en-curso {
    background: #f39c12;
    color: white;
}

.estado.finalizada {
    background: #27ae60;
    color: white;
}

.estado.por-finalizar {
    background: #e74c3c;
    color: white;
}

.acciones {
    text-align: center;
    margin: 3rem 0;
}

.btn-principal {
    background: #3498db;
    color: white;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-principal:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.resumen-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
}

.estado-detalle {
    margin-top: 1rem;
}

.barra {
    padding: 0.8rem;
    margin: 0.5rem 0;
    border-radius: 5px;
    color: white;
    font-weight: bold;
    min-width: 200px;
}

.tabla-container {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #eee;
}

th {
    background: #2c3e50;
    color: white;
    font-weight: bold;
}

tr:hover {
    background: #f8f9fa;
}

@media (max-width: 768px) {
    .dashboard {
        grid-template-columns: 1fr;
    }
    
    nav a {
        margin: 0 0.5rem;
        font-size: 0.9rem;
    }
    
    .metric {
        font-size: 2rem;
    }
    
    table {
        font-size: 0.9rem;
    }
    
    th, td {
        padding: 0.5rem;
    }
}"""
    
    with open('static/css/styles.css', 'w', encoding='utf-8') as archivo:
        archivo.write(css_content)

def main():
    """Función principal que ejecuta todo el simulador"""
    print("🎯 Iniciando simulador Call Center UTP...")
    
    # Crear estructura de carpetas
    crear_directorios()
    print("✅ Carpetas creadas")
    
    # Generar datos simulados
    llamadas = generar_llamadas(50)
    print(f"✅ Generadas {len(llamadas)} llamadas simuladas")
    
    # Guardar en CSV
    guardar_datos_csv(llamadas)
    print("✅ Datos guardados en CSV")
    
    # Calcular estadísticas
    estadisticas = calcular_estadisticas(llamadas)
    print("✅ Estadísticas calculadas")
    
    # Generar páginas HTML
    generar_pagina_inicio(estadisticas)
    generar_pagina_resumen(estadisticas, llamadas)
    generar_pagina_tabla(llamadas)
    print("✅ Páginas HTML generadas")
    
    # Generar CSS
    generar_css()
    print("✅ Estilos CSS generados")
    
    print("\n🚀 Simulador completado!")
    print("📁 Archivos generados:")
    print("   - data/llamadas.csv")
    print("   - templates/inicio.html")
    print("   - templates/resumen.html") 
    print("   - templates/tabla.html")
    print("   - static/css/styles.css")
    print("\n💡 Abre templates/inicio.html en tu navegador para ver el simulador")

if __name__ == "__main__":
    main()
