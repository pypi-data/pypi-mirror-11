#!/usr/bin/env python

import os, sys
from distutils.core import setup
from setuptools.command.install import install as _install

## Post-installation runninf of the core test-suite 
## Thanks to: 

def _post_install(dir):
    try:
        import petlib
        petlib.run_tests()
    except Exception as e:
        print("Tests failed.")
        import traceback
        traceback.print_exc()



class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")


## Need to import the CFFI module during installation to ensure it 
## builds the packages, and places them in the right context.
try:
      import petlib.bindings
      deps = [petlib.bindings._FFI.verifier.get_extension()]
except Exception as e:
      import traceback
      traceback.print_exc()
      print("Alter: Not compiling the library -- useful for readthedocs.")
      deps = []

import petlib


#from pip.req import parse_requirements
# parse_requirements() returns generator of pip.req.InstallRequirement objects
#install_reqs = parse_requirements("requirements.txt")
# reqs is a list of requirement
#reqs = [str(ir.req) for ir in install_reqs]

setup(name='petlib',
      version=petlib.VERSION,
      description='A library implementing a number of Privacy Enhancing Technologies (PETs)',
      author='George Danezis',
      author_email='g.danezis@ucl.ac.uk',
      url=r'https://pypi.python.org/pypi/petlib/',
      packages=['petlib'],
      ext_package='petlib',
      license="2-clause BSD",
      long_description="""A library wrapping Open SSL low-level cryptographic libraries to build Privacy Enhancing Technoloies (PETs)""",
      # install_requires=reqs,
      install_requires=[
            "cffi >= 0.8.2",
            "pycparser >=  2.10",
            "future >= 0.14.3",
            "pytest >= 2.6.4",
            "paver >= 1.2.3",
            "pytest-cov >= 1.8.1",
            "msgpack-python >= 0.4.6",
      ],
      zip_safe=False,
      ext_modules=deps,
      # Custom install with post processing
      cmdclass={'install': install},
)