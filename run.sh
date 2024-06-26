#!/bin/bash

# Ruta al entorno virtual
VIRTUALENV_PATH="autoborme"
echo "Entorno virtual"
# Ruta al archivo de variables de entorno
ENV_VARS_FILE="env_vars.sh"

# Activar el entorno virtual
source "$VIRTUALENV_PATH/Scripts/activate"
echo "Entorno virtual activado"

# Cargar las variables de entorno
if [ -f "$ENV_VARS_FILE" ]; then
    source "$ENV_VARS_FILE"
    echo "Variables de entorno cargadas"
else
    echo "Error: archivo de variables de entorno no encontrado."
    exit 1
fi

#Ejecutar el script de Python
python download_borme_pdfs.py
python borme_json_all.py
python parse_json.py

# Desactivar el entorno virtual (opcional)
deactivate
