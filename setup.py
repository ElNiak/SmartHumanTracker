from setuptools import setup, find_packages
import codecs
import os
import platform


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
try:
  with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()
except:
  # This happens when running tests
  long_description = None

# TODO test if good

setup(name='smarthumaintracker',
      version='0.1',
      description='Smart Humain Tracker',
      long_description=long_description,
      url='https://github.com/ElNiak/SmartHumanTracker',
      author='A-Team from UCLouvain',
      author_email='nomail@uclouvain.com',
      license='MIT', # lol we dont know
      packages=find_packages(),
      setup_requires=['wheel'],
      install_requires=[
            'numpy',
            'scapy'
      ],
      zip_safe=False)