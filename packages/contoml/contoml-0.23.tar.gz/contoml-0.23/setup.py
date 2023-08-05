from setuptools import setup, find_packages
from _version import VERSION

setup(
    name='contoml',
    packages=find_packages(),
    version=VERSION,
    description='Consistent TOML for Python',
    author='Amr Hassan',
    author_email='amr.hassan@gmail.com',
    url='https://github.com/Jumpscale/python-consistent-toml',
    keywords=['toml'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
    install_requires=[
        'six',
        'strict_rfc3339',
        'pytz',
        'timestamp'
    ]
)
