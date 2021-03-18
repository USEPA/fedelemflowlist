from setuptools import setup

install_requires = ['pandas>=0.22',
                    'olca-ipc>=0.0.8']

import struct
bit_size = struct.calcsize("P") * 8
if bit_size == 32:
    install_requires.append('fastparquet>=0.4')
else:
    install_requires.append('pyarrow>=0.14') 

setup(
    name='fedelemflowlist',
    version='1.0.7',
    packages=['fedelemflowlist'],
    package_dir={'fedelemflowlist': 'fedelemflowlist'},
    package_data={'fedelemflowlist': [
        "input/*.*", "output/*.*", "flowmapping/*.*"]},
    include_package_data=True,
    install_requires = install_requires,
    url='https://github.com/USEPA/Federal-LCA-Commons-Elementary-Flow-List',
    license='CC0',
    author='Wesley Ingwersen',
    author_email='ingwersen.wesley@epa.gov',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: CC0",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description='Complies and provides a standardized list of elementary flows and flow mappings for life cycle assessment data'
)
