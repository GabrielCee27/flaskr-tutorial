'''
Describes your project and the files that belong to it.
'''

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    # indicates what package dirs (and their Python files) to include
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
