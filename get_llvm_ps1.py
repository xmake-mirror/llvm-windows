import sys

PS1_SOURCE = """
New-Item -Path . -Name llvm-install -ItemType "directory"
$InstallPath = (Resolve-Path -Path .\\llvm-install).Path

Invoke-WebRequest -Uri "https://github.com/llvm/llvm-project/releases/download/llvmorg-{llvmver}/LLVM-{llvmver}-win{bits}.exe" -OutFile .\\llvm.exe
.\\llvm.exe /S /D=$InstallPath | Wait-Job

Remove-Item -Path $InstallPath\\Uninstall.exe
Compress-Archive -Path $InstallPath\\* -DestinationPath .\\clang+llvm-{llvmver}-win{bits}.zip
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python " + __file__ + " <version> <bits>")
        exit(1)
    llvmver = sys.argv[1]
    bits = "64"
    if len(sys.argv) > 2:
        bits = sys.argv[2]

    with open(f"get_llvm_{llvmver}_{bits}.ps1", "w") as f:
        f.write(PS1_SOURCE.format(llvmver=llvmver, bits=bits))
