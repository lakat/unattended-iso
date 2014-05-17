from setuptools import setup

setup(name='uuiso',
      version='0.0.0',
      packages=['uuiso'],
      entry_points={
          'console_scripts': [
              'uuiso-build = uuiso.ubuntu:build',
          ]
      })
