@echo off
echo =========================================
echo  Wormhole - Build Script
echo =========================================

REM Step 1: Install dependencies
echo [1/4] Checking / installing dependencies...
pip install pyinstaller pillow --quiet
if errorlevel 1 (
    echo ERROR: pip failed. Make sure Python is installed and on your PATH.
    pause
    exit /b 1
)

REM Step 2: Convert wormhole.png to wormhole.ico if needed
if not exist wormhole.ico (
    if exist wormhole.png (
        echo [2/4] Converting wormhole.png to wormhole.ico...
        python -c "from PIL import Image; img = Image.open('wormhole.png'); img.save('wormhole.ico', format='ICO', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])"
        if errorlevel 1 (
            echo ERROR: PNG to ICO conversion failed.
            pause
            exit /b 1
        )
    ) else (
        echo [2/4] No icon found - building without a custom icon.
        powershell -Command "(gc wormhole.spec) -replace \"    icon='wormhole.ico',\", '' | Out-File -Encoding utf8 wormhole.spec"
    )
) else (
    echo [2/4] wormhole.ico found - using it directly.
)

REM Step 3: Build the executable
echo [3/4] Building wormhole.exe...
pyinstaller wormhole.spec --clean
if errorlevel 1 (
    echo ERROR: PyInstaller build failed. See output above.
    pause
    exit /b 1
)

REM Step 4: Done!
echo [4/4] Done!
echo.
echo Your executable is ready at:
echo   dist\wormhole.exe
echo.
echo ---- LEADERBOARD NOTE ----
echo leaderboard.txt is NOT bundled inside the exe.
echo Place your leaderboard.txt in the SAME FOLDER as wormhole.exe
echo so scores persist between sessions. If missing, the game creates
echo a fresh one automatically on first completion.
echo --------------------------
echo.
echo (No Python installation needed on the target machine.)
echo =========================================
pause
