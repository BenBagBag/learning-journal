learning_journal README
==================

This is where you should end up by the end of week 5. This repo contains the Pyramid alchemy scaffold
with the following changes:

Removed the MyModel class from models/mymodel.py
Added the Entries class to models/mymodel.py
Changed models/__init__.py to import Entry instead of MyModel
Removed references to MyModel in scripts/initializedb.py

Getting Started
---------------

- with your virtual environment active:

- cd <directory containing development.ini>

- run: setup_db development.ini

- run server: pserve development.ini
