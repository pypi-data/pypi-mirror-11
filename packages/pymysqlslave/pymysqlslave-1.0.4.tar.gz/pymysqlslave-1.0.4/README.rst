Pymysqlslave
============

SQLAlchemy Simple Master Slave Load Balancing(***beta***)

You can install PyKafka from PyPI with

.. sourcecode:: bash

    $ pip install pykafka


Version update
--------------

- 1.0.3 add is_auto_allocation(Automatic Identification master and slave)
- 1.0.1 initialize project


Getting Started
---------------

.. sourcecode:: python

    #!/usr/bin/env python
    # coding=utf-8

    import logging
    logging.basicConfig(level=logging.DEBUG)
    from sqlalchemy import select

    from pymysqlslave import MySQLDBSlave

    jianv1 = MySQLDBSlave(
        masters=[
            {
                "name": "mysql+mysqldb://jianxun:jianxun@jianxun.dev:3306/jianxunv2?charset=utf8",
                "echo": False,
                "pool_size": 5,
                "pool_recycle": 1,
            }

        ],
        slaves=[
        ],
        is_auto_allocation=True)


    def get_info_by_email(email):
        _t = jianv1.table.customer_member_t
        sql = select([_t]).where(_t.c.email == email)
        return jianv1.execute(sql).fetchone()


    def update_info_by_email(email):
        _t = jianv1.table.customer_member_t
        sql = _t.update().where(_t.c.email == email).values(name=u"穿完")
        jianv1.execute(sql)


    if __name__ == "__main__":
        result = get_info_by_email("592030542@qq.com")
        logging.warn(result)
        update_info_by_email("592030542@qq.com")


TODO
----

- add retry connecting(bug: interactive_timeout)
- add is_auto_allocation(Automatic Identification master and slave)
- Thread Safety


Support
-------

If you need help using pymysqlslave or have found a bug, please open a `github issue`_.

.. _github issue: https://github.com/nashuiliang/pymysqlslave/issues
