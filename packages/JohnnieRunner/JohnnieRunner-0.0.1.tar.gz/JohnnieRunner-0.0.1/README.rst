JohnnieRunner
=============

JohnnieRunner is SQLAlchemy Wrapper for Active Record pattern O/R Mapper

Dependencies
------------

-  Python2.7 or Later
-  SQLAlchemy >= 1.0.8
-  MySQL-Python >= 1.2.5

Support RDBMS
-------------

-  MySQL

Goal
----

-  Add Rails like ActiveRecord Api
-  Database Migration
-  All Supports of SQLAlchemy RDBMS

Usage
-----

Prepare
~~~~~~~

1. generate testing database

   .. code:: bash

       $ mysql -u root -p
       mysql> create database johnnie;
       Query OK, 1 row affected (0.01 sec)

       mysql> exit;
       Bye

2. define O/R Mapper structure

   .. code:: python

       from johnnie import AbstractModel, create_session
       from johnnie.types import Column, String, Integer

       session = create_session('localhost', 'root', 'root user password', 'johnnie')


       class Repositories(AbstractModel):
           class Meta:
               session = session

           id = Column('id', Integer(unsigned=True), primary_key=True)
           name = Column('name', String(255), nullable=False)
           author = Column('author', String(255), nullable=False)
           url = Column('url', String(255), nullable=False)

3. create model table

   .. code:: bash

       $ python
       >>> from hoge import Repositories
       >>> Repositories.metadata.create_all(Repositories.get_session_engine())
       >>> exit()

Example
~~~~~~~

1. create entity

   .. code:: bash

       >>> from hoge import Repositories
       >>> entity = Repositories(name="JohnnieRunner", author="teitei-tk", url="https://github.com/teitei-tk/JohnnieRunner")

       or 

       >>> entity_data = {"name": "JohnnieRunner", "author": "teitei-tk", "url": "https://github.com/teitei-tk/JohnnieRunner"}
       >>> entity = Repositories.new(entity_data)

2. create record

   .. code:: bash

       >>> entity.save()
       True

   .. code:: sql

       mysql> select * from repositories;
       +----+---------------+-----------+--------------------------------------------+
       | id | name          | author    | url                                        |
       +----+---------------+-----------+--------------------------------------------+
       |  1 | JohnnieRunner | teitei-tk | https://github.com/teitei-tk/JohnnieRunner |
       +----+---------------+-----------+--------------------------------------------+
       1 row in set (0.00 sec)
       mysql> 

3. read record

   .. code:: bash

       >>> entity = Repositories.get(1)

       or 

       >>> entity = Repositories.find(1)

       >>> entity.name
       u"JohnnieRunner"
       >>> entity.author
       u"teitei-tk"
       >>> entity.url
       u"https://github.com/teitei-tk/JohnnieRunner"

4. update record

   .. code:: bash

       >>> entity.name = u"update_test"
       >>> entity.save()
       True

   .. code:: sql

       mysql> select * from repositories;
       +----+-------------+-----------+--------------------------------------------+
       | id | name        | author    | url                                        |
       +----+-------------+-----------+--------------------------------------------+
       |  1 | update_test | teitei-tk | https://github.com/teitei-tk/JohnnieRunner |
       +----+-------------+-----------+--------------------------------------------+
       mysql>

5. delete record

   .. code:: bash

       >>> entity.delete()
       True

   .. code:: sql

       mysql> select * from repositories;
       Empty set (0.00 sec)

TODO
----

-  [ ] Add DB Data Types
-  [ ] Easy generate table index
-  [ ] Easy Table RelationShips
-  [ ] Database Migration
-  [ ] RDBMS Support other than MySQL

License
-------

-  MIT
