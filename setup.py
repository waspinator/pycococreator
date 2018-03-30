from distutils.core import setup
from distutils.extension import Extension

# To install library to Python site-packages run "python setup.py  install"

setup(name='pycococreatortools',
    packages=['pycococreatortools'],
    package_dir = {'pycococreatortools': 'pycococreatortools'},
    version='0.1.1',
    install_requires=[
        'numpy', 'pillow', 'skimage'
    ],
)