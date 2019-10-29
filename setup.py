#Set up del agilizador, no necesariamente debes ejecutarlo, pero igual no se toca, jaja saludos
from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    ext_modules = cythonize("extract_embeddings.pyx")
)