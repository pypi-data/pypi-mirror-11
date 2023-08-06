from setuptools import setup, find_packages
import sys, os

version = '0.3.2.5'

setup(name='crackqcli',
      packages=['crackqcli'],
      version=version,
      description="Hashcrack Crackq command-line client",
      long_description="""\
Hashcrack Crackq command-line client for submitting hashes to the Crackq. Supported hash formats: NTLM, MD5, SHA1, WPA/WPA2, PDF, descrypt, md5crypt, PHPass""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='hashcrack crackq password bruteforce hash NTLM MD5 SHA1 WPA WPA2 DESCRYPT MD5CRYPT PDF Wordpress Joomla phpBB3',
      author='Hashcrack',
      author_email='support@hashcrack.org',
      scripts=['crackqcli/crackqcli.py', 'crackqcli/thirdparty'],
      url='http://hashcrack.org',
      license='GPLv3',
      package_data={'thirdparty': ['thirdparty/*.py']},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
