redshift_sqlalchemy
===================

Amazon Redshift dialect for SQLAlchemy.

.. image:: https://travis-ci.org/graingert/redshift_sqlalchemy.png?branch=master

Requirements
-------------
* psycopg2 >= 2.5
* SQLAlchemy 0.8


Usage
-----
The DSN format is similar to that of regular Postgres:

	from sqlalchemy import create_engine

	engine = create_engine("redshift+psycopg2://username@host.amazonaws.com:5439/database"

Notes
-----

Currently, constraints and indexes return nothing when introspecting tables. This is because Redshift implements version 8.0 of the PostgreSQL API.




0.1.2 (2015-08-11)
------------------

- Register postgresql.visit_rename_table for redshift's
  alembic RenameTable.
  Thanks `bouk <https://github.com/bouk>`_.
  (`Issue #7 <https://github.com/graingert/redshift_sqlalchemy/pull/7>`_)


0.1.1 (2015-05-20)
------------------

- Register RedshiftImpl as an alembic 3rd party dialect.


0.1.0 (2015-05-11)
------------------

- First version of sqlalchemy-redshift that can be installed from PyPI


