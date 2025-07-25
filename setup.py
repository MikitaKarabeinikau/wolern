from setuptools import setup, find_packages

setup(
    name='wolern', 
    version='0.0.1', # Start with a version number
    packages=find_packages(),
    install_requires=[],
    package_data={
        'wolern':[
            'data/sources/frequencies_source/*.xls',
        ]
    },
    author='Mikita Karabeinikau',
    description='Coming soon...',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MikitaKarabeinikau/wolern', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Or whatever license you use
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', 
)
