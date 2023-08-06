==========
pythonbase
==========

pythonbase provides a skeleton for creating Python projects, complete with Sphinx docs, PyPI integration, etc.

Basic setup
===========

#. Copy the directory structure and files of Pythonbase to your project.
#. Make changes to all these files as necessary (e.g., by grep'ing for "pythonbase" and replacing with your project).
#. Run ``python setup.py develop`` in your new project to install it on your system
#. Run ``python setup.py release`` to release your project to PyPI. Congratulations, your project can now be installed!

(The last step probably requires PyPI registration; fill in details once I get a good test case for a new user).

Docs setup
==========

#. Navigate to the ``pythonbase/docs`` directory
#. Run ``sphinx-apidoc -o . -f ../pythonbase; make html``
#. Go up one directory (``cd..``).
#. Release docs: ``python setup.py upload_docs --upload-dir=docs/_build/html``

CircleCI setup
==============

#. Log into CircleCI, and build your project.

The Pythonbase docs are located as `here <http://pythonhosted.org/pythonbase>`_