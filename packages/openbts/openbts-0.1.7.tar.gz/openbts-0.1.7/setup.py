"""The openbts-python package."""

from setuptools import setup


with open('readme.md') as f:
  README = f.read()


VERSION = '0.1.7'


setup(
  name='openbts',
  version=VERSION,
  description='OpenBTS NodeManager client',
  long_description=README,
  url='http://github.com/endaga/openbts-python',
  download_url=('https://github.com/endaga/openbts-python/tarball/%s' %
                VERSION),
  author='Matt Ball',
  author_email='matt@endaga.com',
  license='MIT',
  packages=['openbts'],
  install_requires=[
    "enum34==1.0.4",
    "envoy==0.0.3",
    "pyzmq==14.5.0",
  ],
  zip_safe=False
)
