from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='apalib',
    version='1.0.0',
    description='Advanced Protein Analysis library',
    long_description=open('README.md').read() +'\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Nate McMurray',
    author_email='natemresearch@gmail.com',
    licence='MIT',
    classifiers=classifiers,
    keywords='Protein',
    packages=find_packages(),
    install_requires=['numpy']
)