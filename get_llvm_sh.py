import sys
from packaging.version import Version

OLD_BASH_SOURCE = """#!/bin/bash
set -e

mkdir -p llvm-install
InstallPath=$(pwd)/llvm-install

wget -O llvm.tar.xz "https://github.com/llvm/llvm-project/releases/download/llvmorg-{llvmver}/clang+llvm-{llvmver}-x86_64-linux-gnu.tar.xz"

tar -xf llvm.tar.xz -C "$InstallPath" --strip-components=1

rm llvm.tar.xz

tar -czf clang+llvm-{llvmver}-linux-x86_64.tar.gz -C "$InstallPath" .
"""

NEW_BASH_SOURCE = """#!/bin/bash
set -e

wget -O llvm.tar.xz "https://github.com/llvm/llvm-project/releases/download/llvmorg-{llvmver}/clang+llvm-{llvmver}-{target}.tar.xz"

tar -xf llvm.tar.xz

rm llvm.tar.xz

tar -czf clang+llvm-{llvmver}-{target}.tar.gz clang+llvm-{llvmver}-{target}
"""

def get_target(llvmver, arch):
    """Map architecture to LLVM release target"""
    arch_map = {
        'x86_64': 'x86_64',
        'aarch64': 'aarch64',
        'arm64': 'aarch64',  # macOS uses arm64, LLVM uses aarch64
    }

    if Version(llvmver) >= Version("18.0.0"):
        # Newer versions use separate targets for Linux and macOS
        target_arch = arch_map.get(arch, arch)
        # This is a simplified version - actual targets may vary
        return f"{target_arch}-linux-gnu"
    else:
        return "x86_64-linux-gnu"

def no_target(llvmver):
    return Version(llvmver) < Version("18.1.0") or Version(llvmver) == Version("18.1.3")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python " + __file__ + " <version> <arch>")
        exit(1)
    llvmver = sys.argv[1]
    arch = "x86_64"
    if len(sys.argv) > 2:
        arch = sys.argv[2]

    with open(f"get_llvm_{llvmver}_{arch}.sh", "w") as f:
        if no_target(llvmver):
            f.write(OLD_BASH_SOURCE.format(llvmver=llvmver, arch=arch))
        else:
            target = get_target(llvmver, arch)
            f.write(NEW_BASH_SOURCE.format(llvmver=llvmver, target=target))

    # Make the script executable
    import os
    import stat
    os.chmod(f"get_llvm_{llvmver}_{arch}.sh", os.stat(f"get_llvm_{llvmver}_{arch}.sh").st_mode | stat.S_IEXEC)
