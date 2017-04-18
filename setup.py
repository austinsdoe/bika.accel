from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='bika.accel',
      version=version,
      description="A Bika Health's accelised add-on for ACCEL Group",
      long_description=open("README.md").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Naralabs',
      author_email='info@naralabs.com',
      url='https://www.naralabs.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bika'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'bika.health',
          'z3c.unconfigure',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
