from setuptools import setup, find_packages

setup(name='uiso',
      version='0.2.0-dev',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'uiso-ubuntu = uiso.ubuntu.build:main',
              'uiso-centos = uiso.centos.build:main',
          ]
      })
