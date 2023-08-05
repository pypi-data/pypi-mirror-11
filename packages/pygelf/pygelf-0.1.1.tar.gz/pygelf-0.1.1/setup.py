from setuptools import setup


setup(
    name='pygelf',
    version='0.1.1',
    packages=['pygelf'],
    description="Python logging implementation of GELF (graylog extended log format)",
    keywords='logging udp tcp graylog2 graylog gelf',
    author='Ivan Mukhin',
    author_email='muhin.ivan@gmail.com',
    url='https://github.com/keeprocking/pygelf',
    long_description=open('README.rst').read(),
    license='MIT'
)
