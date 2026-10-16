# Compila OneDriveResetter.exe en la MISMA carpeta que el .py, con icon.ico y sin consola.
# Uso:  powershell -ExecutionPolicy Bypass -File build.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

python -m pip install --upgrade -r requirements.txt

# --onefile: un solo .exe | --noconsole: app GUI | --distpath .: deja el .exe junto al .py
# (rutas absolutas porque --specpath cambia la base relativa)
# --add-data: empaqueta el icono para la ventana | --workpath/--specpath: temporales fuera del código
python -m PyInstaller --noconfirm --clean --onefile --noconsole `
    --name OneDriveResetter `
    --icon "$PSScriptRoot\icon.ico" `
    --add-data "$PSScriptRoot\icon.ico;." `
    --distpath . --workpath build --specpath build `
    onedriverresetter.py

if ($LASTEXITCODE -ne 0) { throw "PyInstaller falló" }
Write-Host "Listo: $PSScriptRoot\OneDriveResetter.exe"
