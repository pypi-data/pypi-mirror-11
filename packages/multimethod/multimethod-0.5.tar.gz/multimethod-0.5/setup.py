from setuptools import setup
import multimethod

setup(
    name='multimethod',
    version=multimethod.__version__,
    description='Multiple argument dispatching.',
    long_description=open('README.rst').read(),
    author='Aric Coady',
    author_email='aric.coady@gmail.com',
    url='https://bitbucket.org/coady/multimethod',
    license='Apache Software License',
    py_modules=['multimethod'],
    tests_require=['pytest-cov'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
