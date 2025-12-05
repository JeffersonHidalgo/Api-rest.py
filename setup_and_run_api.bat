
@echo off
:: Script para crear entorno virtual, instalar dependencias y ejecutar la API

:: Crear entorno virtual
python -m venv .venv

:: Activar entorno virtual
call .venv\Scripts\activate

:: Actualizar pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Instalar dependencias
python -m pip install fastapi uvicorn[standard] pydantic pytest httpx

echo.
echo =============================================
echo Instalación completada.
echo Ejecutando la API...
echo =============================================

:: Ejecutar la API
python -m uvicorn app.main:app --reload
