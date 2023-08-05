from setuptools import setup

#from setuptools import find_packages  
#from os import path
#from codecs import open  # To use a consistent encoding
#here = path.abspath(path.dirname(__file__))
#
# Get the long description from the relevant file
#with open(path.join(here, 'README'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='timml',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version = '4.0.0',

    description = 'Steady multi-layer AEM model',
    long_description = 'timml is an AEM model for simulating steady multi-aquifer flow',

    # The project's main homepage.
    url = 'https://github.com/mbakker7/timml',

    # Author details
    author='Mark Bakker',
    author_email='markbak@gmail.com',

    # Choose your license
    license = 'MIT',

    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        #'Intended Audience :: Groundwater Modelers',
        # Pick yor license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7'
        ],
    platforms='Windows, Mac OS-X',
    install_requires=['numpy>=1.9', 'matplotlib>=1.4'],
    packages=['timml'],
    include_package_data = True,
    package_data = {'timml': ['besselaes.f90', 'besselaes.so']}
    )