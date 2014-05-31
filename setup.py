from setuptools import setup

setup(name='uiso',
      version='0.2.0-dev',
      packages=['uiso'],
      entry_points={
          'console_scripts': [
              'uiso-ubuntu = uiso.ubuntu.build:main',
              'uiso-centos = uiso.centos.build:main',
          ]
      })
