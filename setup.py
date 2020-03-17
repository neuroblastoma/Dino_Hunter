from setuptools import setup

setup(
    name='Dino_Hunter',
    version='1.0.0',
    url='https://github.com/neuroblastoma/Dino_Hunter',
    license='',
    author='',
    author_email='',
    description='Defender clone with dinosaurs',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'pygame>=1.9.6',
        'thorpy>=1.6.3',
        'mock'
    ],
    packages=['tests', 'utils']
)
