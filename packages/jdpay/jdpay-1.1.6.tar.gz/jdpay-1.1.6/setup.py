import os
from setuptools import setup
from setuptools import find_packages

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_DIR, 'README.md')).read()
CHANGES = open(os.path.join(BASE_DIR, 'CHANGES.rst')).read()

setup(name='jdpay',
      version='1.1.6',
      description='This is an unofficial python JingDong pay API.',
      long_description=README + '\n\n' + CHANGES,
      author='Haotong Chen',
      author_email='hereischen@gmail.com',
      url='https://github.com/hereischen/jdpay',
      license='BSD License',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7',
      ],
      include_package_data=True,
      zip_safe=False,
      # test_suite='jdpay.tests'
      )
