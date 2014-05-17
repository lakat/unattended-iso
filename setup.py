from setuptools import setup

setup(name='uiso',
      version='0.0.0',
      packages=['uiso'],
      entry_points={
          'console_scripts': [
              'uiso-build = uiso.ubuntu:build',
          ]
      })
