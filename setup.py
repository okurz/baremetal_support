import setuptools


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='baremetal_support',
    version='0.1.0',
    description='iPXE http server for chainloaded bootscripts',
    long_description=readme,
    author='Michael Moese',
    author_email='mmoese@suse.de',
    url='https://github.com/frankenmichl/ipxe_http',
    license=license,
    packages='baremetal_support'
)
