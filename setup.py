"""
Modern setup.py for Cython extension modules.
Extensions only used on CPython for PyPy compatibility.
Can disable extensions via BLACKSHEEP_NO_EXTENSIONS=1.
Reference: https://github.com/Neoteroi/BlackSheep/issues/539#issuecomment-2888631226
"""

import os
import platform
from pathlib import Path
from setuptools import Extension, setup

# Optimized compilation arguments
COMPILE_ARGS = ["-O2", "-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION"]

# Check if extension compilation should be skipped
skip_ext = (os.environ.get("BLACKSHEEP_NO_EXTENSIONS", "0") == "1" or 
           os.environ.get("BLACKSHEEP_BUILD_PURE", "0") == "1")

# Cython extension module definitions
EXTENSIONS = [
    "url",
    "exceptions", 
    "headers",
    "cookies",
    "contents",
    "messages",
    "scribe",
    "baseapp",
]


def create_extensions():
    """Create extension modules list"""
    extensions = []
    base_path = Path("blacksheep")
    
    for ext_name in EXTENSIONS:
        c_file = base_path / f"{ext_name}.c"
        
        # Check if C file exists
        if c_file.exists():
            extension = Extension(
                f"blacksheep.{ext_name}",
                [str(c_file)],
                extra_compile_args=COMPILE_ARGS,
                language="c",
            )
            extensions.append(extension)
        else:
            print(f"Warning: C file not found for {ext_name}, skipping extension")
    
    return extensions


# Determine whether to compile extensions based on runtime environment
if platform.python_implementation() == "CPython" and not skip_ext:
    ext_modules = create_extensions()
    print(f"Building with {len(ext_modules)} Cython extensions")
else:
    ext_modules = []
    reason = "PyPy runtime" if platform.python_implementation() != "CPython" else "extensions disabled"
    print(f"Building without extensions ({reason})")

setup(ext_modules=ext_modules)
