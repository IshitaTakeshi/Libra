import os
from distutils.core import setup

packages = []
directory = 'libra'

for dirpath, dirnames, filenames in os.walk(directory):
    if('__init__.py' in filenames):
        packages.append(dirpath.replace(os.sep, '.'))

print(packages)

setup(
    name='libra',
    version='1.0',
    description="Photo analyzer", 
    packages=packages,
    author='Ishita Takeshi',
)
