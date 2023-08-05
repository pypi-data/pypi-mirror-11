from setuptools import setup, find_packages

with open('.version') as f:
    VERSION = f.readline().strip()

setup(
    name='ocflib',
    version=VERSION,
    author="Open Computing Facility",
    author_email='help@ocf.berkeley.edu',
    description="libraries for account and server management",
    url='https://www.ocf.berkeley.edu',
    packages=find_packages(),
    install_requires=(
        'colorama',
        'cracklib',
        'dnspython3',
        'ldap3',
        'paramiko',
        'pexpect',
        'pycrypto',
        'pysnmp',
        'requests',
    )
)
