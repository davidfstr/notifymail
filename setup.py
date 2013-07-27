from distutils.core import setup
import os
import sys

def is_older_than(file1, file2):
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False
    return os.path.getmtime(file1) < os.path.getmtime(file2)

# Generate README.rst if missing or out of date
if not os.path.exists('README.rst') or is_older_than('README.rst', 'README.md'):
    os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
with open('README.rst') as file:
    long_description = file.read()

setup(
    # Identity
    name='notifymail',
    version='1.0',
    
    # Contents
    py_modules=['notifymail'],
    scripts=['notifymail.py'],
    
    # Metadata
    author='David Foster',
    author_email='davidfstr@gmail.com',
    url='https://github.com/davidfstr/notifymail/',
    description='Allows scripts to send email to a preconfigured address.',
    long_description=long_description,
    license='MIT',
    # see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        'Topic :: System :: Systems Administration',
    ]
)