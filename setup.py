from setuptools import setup, find_packages

setup(
    name='marzneshein',
    version='0.1.0',
    description='Marzneshein Control API Client',
    author='Artem',
    author_email='contact@sm1ky.com',
    url='https://github.com/sm1ky/marzneshein_api',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'pydantic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)