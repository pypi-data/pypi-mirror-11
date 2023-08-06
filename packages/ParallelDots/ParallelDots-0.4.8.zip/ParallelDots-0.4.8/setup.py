from setuptools import setup, find_packages
from codecs import open
from os import path

def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='ParallelDots',
    version='0.4.8',
    description='Python Wrapper for ParallelDots API',
    long_description=read("README.rst"),
    url='https://github.com/ParallelDots/ParallelDots-Python-API.git',
    author='Ahwan Kumar',
    author_email='ahwan@paralleldots.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='paralleldots sentiment taxonomy ner semantic similarity deeplearning',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    setup_requires=[
        "urllib3 >= 1.11"
    ],
    install_requires=[
        "urllib3 >= 1.11"
    ],
    entry_points={
        'console_scripts': [
            'paralleldots=paralleldots:main',
        ],
    },
)
