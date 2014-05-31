from setuptools import setup, find_packages


setup(name='uiso',
      version='0.2.0',
      packages=find_packages(),
      package_data = {
          'uiso': [
            'centos/isolinux.cfg.5',
            'centos/isolinux.cfg.6',
            'centos/ks.cfg.5',
            'centos/ks.cfg.6',
            'centos/post_install.sh',
            'ubuntu/autoinst.seed',
            'ubuntu/post_install.sh',
            'ubuntu/txt.cfg',
            ]
      },
      entry_points={
          'console_scripts': [
              'uiso-ubuntu = uiso.ubuntu.build:main',
              'uiso-centos = uiso.centos.build:main',
          ]
      })
