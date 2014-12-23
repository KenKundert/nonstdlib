import distutils.core

# Uploading to PyPI
# =================
# $ python setup.py register -r pypi
# $ python setup.py sdist upload -r pypi

version = '0.0'
distutils.core.setup(
        name='nonstdlib',
        version=version,
        author='Kale Kundert',
        packages=['nonstdlib'],
        url='https://github.com/kalekundert/nonstdlib',
        download_url='https://github.com/kalekundert/nonstdlib/tarball/'+version,
        license='LICENSE.txt',
        description="A collection a general-purpose utilities.",
        long_description=open('README.rst').read(),
        keywords=['utilities', 'library'])