from distutils.core import setup
import os, sys

setup(name="d51_admin_autofk",
      version="0.0.1",
      description="Provide combo-boxes for foreign key fields in Django admin",
      author="Chris Dickinson",
      author_email="chris@neversaw.us",
      url="http://github.com/chrisdickinson/d51_admin_autofk",
      packages=["d51_admin_autofk"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: Common Development and Distribution License (CDDL)",
                   "License :: OSI Approved :: GNU Public License (GPL)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Framework :: Django",])

