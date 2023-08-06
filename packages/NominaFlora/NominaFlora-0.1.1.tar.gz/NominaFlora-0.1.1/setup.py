''' setup script '''
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='NominaFlora',
    version='0.1.1',

    description='Generates new flower names',
    long_description=long_description,

    url='https://github.com/mouse-reeve/nomina-flora',

    author='Mouse Reeve',
    author_email='mouse.reeve@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='generative language flowers',

    packages=['nominaflora'],
)
