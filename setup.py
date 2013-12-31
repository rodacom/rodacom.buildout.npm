from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name="rodacom.buildout.npm",
    version='0.3',
    description='A buildout recipe to install NodeJS packages locally using npm',
    long_description=long_description,
    license='Apache Software License',
    keywords='buildout zc.buildout recipe nodejs npm',
    author='Michael Lemaire',
    author_email='m.lemaire@rodacom.fr',
    py_modules=['npm'],
    install_requires=[
        'zc.buildout',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'zc.buildout': ['default = npm:Npm']
    },
)
