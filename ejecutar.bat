@echo off
title Simulador LRU - Sistemas Operativos G2
echo ============================================
echo   Simulador LRU - Equipo 6
echo   Sistemas Operativos G2 - Proyecto 1
echo ============================================
echo.

:: Paso A - Validar Python
echo [1/3] Verificando instalacion de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    echo         Descargalo desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo       Python encontrado correctamente.
echo.

:: Paso B - Validar dependencias
echo [2/3] Verificando dependencias...
python -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo       Pillow no encontrado. Instalando automaticamente...
    pip install pillow >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] No se pudo instalar Pillow. Ejecuta manualmente:
        echo         pip install pillow
        echo.
        pause
        exit /b 1
    )
    echo       Pillow instalado correctamente.
) else (
    echo       Todas las dependencias estan instaladas.
)
echo.

:: Paso C - Lanzar el simulador
echo [3/3] Iniciando simulador...
cls
python main.py
