"""setuptools config for pyrecommend."""
import os
from setuptools import setup


def read(fname):
    """Get the contents of the named file as a string."""
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return u''


setup(
    name='pyrecommend',
    version='0.1.dev4',
    author='Dan Passaro',
    author_email='danpassaro@gmail.com',
    url='https://github.com/dan-passaro/pyrecommend/',
    description='A simple collaborative filtering algorithm for Python.',
    license='BSD',
    packages=['pyrecommend'],
    long_description=read('README.md'),
)
