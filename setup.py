from distutils.core import setup
from distutils.extension import Extension

# To install library to Python site-packages run "python setup.py  install"

setup(name='pycocoextra',
    packages=['pycocoextra'],
    package_dir = {'pycocoextra': 'pycocoextra'},
    version='0.1.0',
    install_requires=[
        'numpy',
    ],
)