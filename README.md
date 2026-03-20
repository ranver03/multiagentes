# 🏆 Proyecto Quiniela Mundial - Multi-Agentes (CrewAI)

Este proyecto utiliza **CrewAI** y **Google Gemini** para automatizar el diseño y desarrollo de una aplicación de quiniela.

## 🛠️ Configuración del Entorno (Ubuntu 24.04)

### 1. Requisitos Previos
Asegúrate de tener Python 3.10+ instalado:
```bash
python3 --version
2. Levantar el Entorno Virtual
Desde la carpeta del proyecto:

Bash
# Crear el entorno si no existe
python3 -m venv venv

# ACTIVAR EL ENTORNO (Hacer esto siempre antes de trabajar)
source venv/bin/activate
3. Instalación de Librerías
Con el entorno activo (venv), instala las dependencias necesarias:

Bash
pip install crewai crewai-tools langchain-google-genai
4. Configuración de la API Key
Exporta tu llave de Gemini (puedes añadirlo a tu .bashrc para que sea permanente):

Bash
export GEMINI_API_KEY="TU_LLAVE_AQUI"
5. Ejecución del Script
Bash
python3 main.py