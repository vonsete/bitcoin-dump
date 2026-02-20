#!/bin/bash
# Script de instalación para Bitcoin Analyzer

echo "=================================="
echo "  Bitcoin Analyzer - Instalación"
echo "=================================="
echo ""

# Detectar si existe python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "   Instala con: sudo apt install python3"
    exit 1
fi

echo "✅ Python 3 detectado: $(python3 --version)"
echo ""

# Opción 1: Intentar con venv
echo "📦 Opción 1: Instalación en entorno virtual (recomendado)"
echo ""

if command -v python3 -m venv &> /dev/null; then
    echo "Creando entorno virtual..."
    python3 -m venv venv

    echo "Activando entorno virtual..."
    source venv/bin/activate

    echo "Instalando dependencias..."
    pip install -r requirements.txt

    echo ""
    echo "✅ Instalación completada!"
    echo ""
    echo "Para usar el script:"
    echo "  1. Activa el entorno virtual: source venv/bin/activate"
    echo "  2. Ejecuta: python bitcoin_analyzer.py [opciones] [dirección/tx]"
    echo "  3. Desactiva cuando termines: deactivate"

else
    echo "⚠️  python3-venv no está instalado"
    echo ""
    echo "📦 Opción 2: Instalación de paquetes del sistema"
    echo ""
    echo "Ejecuta los siguientes comandos:"
    echo ""
    echo "  sudo apt update"
    echo "  sudo apt install python3-requests python3-matplotlib python3-networkx python3-pandas"
    echo ""
    echo "Luego podrás ejecutar:"
    echo "  python3 bitcoin_analyzer.py [opciones] [dirección/tx]"
fi

echo ""
echo "=================================="
