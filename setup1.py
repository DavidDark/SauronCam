#Si ejecutaste el primer setup, lo mas recomendable es ejecutar tambien el segundo, este es para agilizar entrenar el modelo
from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    ext_modules = cythonize("train_model.pyx")
)