import os
import json
import pandas as pd
import re
import shutil

def listar_archivos_json(carpeta):
    # Construir la ruta completa a la carpeta
    ruta_carpeta = os.path.join(os.getcwd(), carpeta)
    
    # Verificar si la carpeta existe
    if not os.path.isdir(ruta_carpeta):
        print(f"La carpeta {carpeta} no existe.")
        return
    
    archivos_json = []
    
    # Recorrer todos los directorios y subdirectorios
    for root, dirs, files in os.walk(ruta_carpeta):
        for file in files:
            if file.endswith('.json'):
                archivos_json.append(os.path.join(root, file))
    
    # Verificar si hay archivos JSON en la carpeta
    if not archivos_json:
        print(f"No se encontraron archivos JSON en la carpeta {carpeta}.")
        return
    return archivos_json

def extraer_informacion(texto):
    info = {}
    
    # Buscar cada patrón y asignar a la información correspondiente
    match_procedimiento = re.search(r'Procedimiento concursal (\d+/\d+)', texto)
    if match_procedimiento:
        info['procedimiento'] = match_procedimiento.group(1)
    else:
        info['procedimiento'] = None
    
    match_firme = re.search(r'FIRME: (Si|SI|No|NO)', texto)
    if match_firme:
        info['firme'] = match_firme.group(1)
    else:
        info['firme'] = None
    
    match_fecha_resolucion = re.search(r'Fecha de resolución ((\d{2}|\d{1})/\d{2}/\d{4})', texto)
    if match_fecha_resolucion:
        info['fecha_resolucion'] = match_fecha_resolucion.group(1)
    else:
        info['fecha_resolucion'] = None
    
    match_auto_juzgado = re.search(r'(\d{1,2}/\d{2}/\d{4}\.) (.+?) Juzgado', texto)
    if match_auto_juzgado:
        info['auto'] = match_auto_juzgado.group(2)
    else:
        info['auto'] = None
    
    match_admin = re.search(r'NIF/CIF \w+\. (.+)\.', texto)
    if match_admin:
        info['administrador_concursal'] = match_admin.group(1).strip()
    else:
        info['administrador_concursal'] = None
    
    match_juzgado = re.search(r'Juzgado: num\. \d+ ([^\.]+)', texto)
    if match_juzgado:
        info['juzgado'] = match_juzgado.group(1)
    else:
        info['juzgado'] = None
    
    match_juez = re.search(r'Juez: ([^\.]+)', texto)
    if match_juez:
        info['juez'] = match_juez.group(1)
    else:
        info['juez'] = None
    
    match_resoluciones = re.search(r'Resoluciones: ([^\.]+)', texto)
    if match_resoluciones:
        info['resoluciones'] = match_resoluciones.group(1)
    else:
        info['resoluciones'] = None
    
    return info

def leer_y_filtrar_json(archivos_json):
    data = []
    
    for archivo in archivos_json:
        with open(archivo, 'r', encoding='utf-8') as f:
            try:
                contenido = json.load(f)
                for anuncio_id, anuncio in contenido.get('anuncios', {}).items():
                    for acto in anuncio.get('actos', []):
                        for etiqueta, texto in acto.items():
                            if etiqueta == "Situación concursal":
                                info = extraer_informacion(texto)
                                anuncio_data = {
                                    'Numero': anuncio_id,
                                    'Empresa': anuncio.get('empresa'),
                                    'Datos registrales': anuncio.get('datos registrales'),
                                    'Liquidación': anuncio.get('liquidacion'),
                                    'N procedimiento': info['procedimiento'],
                                    'Firme': info['firme'],
                                    'Fecha resolución': info['fecha_resolucion'],
                                    'Tipo auto': info['auto'],
                                    'Juzgado': info['juzgado'],
                                    'Juez': info['juez'],
                                    'Resoluciones': info['resoluciones'], 
                                    'Administrador concursal': info['administrador_concursal']
                                }
                                data.append(anuncio_data)
            except json.JSONDecodeError as e:
                print(f"Error al leer el archivo {archivo}: {e}")
    
    df = pd.DataFrame(data)
    return df

def guardar_en_excel(df, nombre_archivo):
    df.to_excel(nombre_archivo, index=False)
    print(f"Archivo guardado como {nombre_archivo}")

# Nombre de la carpeta a buscar
carpeta_a_buscar = "downloads/json_folder"

# Llamar a la función para listar los archivos JSON
archivos_json = listar_archivos_json(carpeta_a_buscar)

if archivos_json:
    df = leer_y_filtrar_json(archivos_json)
    print(df)
    nombre_archivo_excel = "Situaciones concursales.xlsx"
    guardar_en_excel(df, nombre_archivo_excel)
else:
    print("No se encontraron archivos JSON para procesar.")

# Verificar si la carpeta existe
if os.path.exists(carpeta_a_buscar) and os.path.isdir(carpeta_a_buscar):
    # Eliminar la carpeta y todo su contenido
    shutil.rmtree(carpeta_a_buscar)
    print(f'La carpeta {carpeta_a_buscar} ha sido eliminada.')
else:
    print(f'La carpeta {carpeta_a_buscar} no existe o no es una carpeta.')