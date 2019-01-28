from setuptools import setup

setup(name='ficticious_corporeality',
        version='0.1',
        description='General 3D physics simulator.',
        url='https://github.com/dcax/ficticious_corporeality',
        author='Dylan Alexander',
        author_email='dylan@postriver.com',
        license='GNU',
        scripts=['bin/verse'],
        install_requires=[
            'matplotlib','numpy','scipy','pandas',
            ],
        packages=['ficticious_corporeality'],
        zip_safe=False)