from setuptools import setup

setup(
    name='fedelemflowlist',
    version='1.3.2',
    packages=['fedelemflowlist'],
    package_dir={'fedelemflowlist': 'fedelemflowlist'},
    package_data={'fedelemflowlist': [
                        "input/*.*",
                        "flowmapping/*.*"]
        },
    include_package_data=True,
    python_requires=">=3.9",
    install_requires = [
        'pandas>=0.22',
        'olca-schema>=0.0.11',
        'esupy @ git+https://github.com/USEPA/esupy.git@develop#egg=esupy',
        ],
    url='https://github.com/USEPA/fedelemflowlist',
    license='CC0',
    author='Wesley Ingwersen',
    author_email='ingwersen.wesley@epa.gov',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: MIT",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description=('Complies and provides a standardized list of elementary '
                 'flows and flow mappings for life cycle assessment data')
)
