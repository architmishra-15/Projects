from setuptools import setup, Extension

module = Extension('pointers', sources= ['pointers.c'])

setup (
    name = 'pointers',
    version = '1.1.0',
    description = 'Access memory address of an object and the value stored at a memory address and vice versa',
    ext_modules = [module],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Operating System :: OS Independent",
    ],
)
