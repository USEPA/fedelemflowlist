from setuptools import setup

setup(
    name='fedelemflowlist',
    version='0.1',
    packages=['fedelemflowlist'],
    package_dir={'fedelemflowlist': 'fedelemflowlist'},
    package_data={'fedelemflowlist': ["input/*.*", "output/*.*","flowmapping/*.*","candidate-flows/*.*"]},
    include_package_data=True,
    install_requires = ['pandas>=0.22'],
    url='https://github.com/USEPA/Federal-LCA-Commons-Elementary-Flow-List',
    license='CC0',
    author='Wesley Ingwersen',
    author_email='ingwersen.wesley@epa.gov',
    classifiers=[
        "Development Status :: Alpha",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: CC0",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description='Complies and provides a standardized list of elementary flows for life cycle assessment data'
)
