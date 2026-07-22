@echo off
setlocal

echo =====================================
echo      ScreenAgent Build Script
echo =====================================
echo.


REM Проверяем наличие venv

if not exist "venv\" (
    echo [INFO] Creating virtual environment...

    python -m venv venv

    if errorlevel 1 (
        echo [ERROR] Failed creating venv
        pause
        exit /b 1
    )
)


REM Активируем окружение

echo [INFO] Activating virtual environment...

call venv\Scripts\activate.bat


REM Обновляем pip

echo [INFO] Updating pip...

python -m pip install --upgrade pip


REM Устанавливаем зависимости

echo [INFO] Installing requirements...

pip install -r requirements.txt


if errorlevel 1 (
    echo [ERROR] Failed installing requirements
    pause
    exit /b 1
)


REM Проверяем PyInstaller

echo [INFO] Checking PyInstaller...

pyinstaller --version >nul 2>&1


if errorlevel 1 (
    echo [INFO] Installing PyInstaller...

    pip install pyinstaller
)


REM Сборка

echo.
echo [INFO] Building EXE...

pyinstaller ^
    --clean ^
    --onefile ^
    --noconsole ^
    --name PostgreSQLUtil ^
    main.py


if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)


REM Копирование конфигов

echo.
echo.
echo [INFO] Copying configuration files...


REM Создаем dist если нет

if not exist "dist\" (
    mkdir dist
)


REM Проверяем config.json

if exist "dist\config.json" (

    echo [INFO] Existing dist\config.json found. Keeping it.

) else (

    echo [INFO] Creating config.json from template...

    copy /Y config.example.json dist\config.json

)


REM events.json всегда обновляем

if exist "events.json" (

    copy /Y events.json dist\events.json

) else (

    echo [WARNING] events.json not found

)


if errorlevel 1 (
    echo [ERROR] Failed copying configs
    pause
    exit /b 1
)


echo.
echo =====================================
echo BUILD SUCCESS
echo =====================================
echo.
echo Output:

dir dist


pause