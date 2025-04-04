import sys
from packaging.version import Version

OLD_PS1_SOURCE = """
New-Item -Path . -Name llvm-install -ItemType "directory"
$InstallPath = (Resolve-Path -Path .\\llvm-install).Path

Invoke-WebRequest -Uri "https://github.com/llvm/llvm-project/releases/download/llvmorg-{llvmver}/LLVM-{llvmver}-win{bits}.exe" -OutFile .\\llvm.exe
.\\llvm.exe /S /D=$InstallPath | Wait-Job

Remove-Item -Path $InstallPath\\Uninstall.exe
Compress-Archive -Path $InstallPath\\* -DestinationPath .\\clang+llvm-{llvmver}-win{bits}.zip
"""

NEW_PS1_SOURCE = """
Invoke-WebRequest -Uri "https://github.com/llvm/llvm-project/releases/download/llvmorg-{llvmver}/clang+llvm-{llvmver}-x86_64-pc-windows-msvc.tar.xz" -OutFile "llvm.tar.xz"

if (-not (Get-Command Expand-7Zip -ErrorAction Ignore)) {{
    Install-Module -Force -Name 7Zip4Powershell -Scope CurrentUser > $null
}}

Expand-7Zip -ArchiveFileName llvm.tar.xz -TargetPath .\\

Expand-7Zip -ArchiveFileName llvm.tar -TargetPath .\\

Remove-Item .\llvm.tar

Remove-Item .\llvm.tar.xz

Compress-Archive -Force -Path .\clang+llvm-{llvmver}-x86_64-pc-windows-msvc\\* -DestinationPath .\clang+llvm-{llvmver}-win{bits}.zip
"""

def no_target(llvmver):
    return Version(llvmver) < Version("18.1.0") or Version(llvmver) == Version("18.1.3")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python " + __file__ + " <version> <bits>")
        exit(1)
    llvmver = sys.argv[1]
    bits = "64"
    if len(sys.argv) > 2:
        bits = sys.argv[2]

    with open(f"get_llvm_{llvmver}_{bits}.ps1", "w") as f:
        if bits == "32":
            f.write(OLD_PS1_SOURCE.format(llvmver = llvmver, bits = bits))
        elif bits == "64":
            if no_target(llvmver):
                f.write(OLD_PS1_SOURCE.format(llvmver = llvmver, bits = bits))
            else:
                f.write(NEW_PS1_SOURCE.format(llvmver = llvmver, bits = bits))