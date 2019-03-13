from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ipxe_http',
    version='0.1.0',
    description='iPXE http server for chainloaded bootscripts',
    long_description=readme,
    author='Michael Moese',
    author_email='mmoese@suse.de',
    url='https://github.com/frankenmichl/ipxe_http',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
