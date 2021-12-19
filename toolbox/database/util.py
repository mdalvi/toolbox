import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy.pool import NullPool

from toolbox.requests.util import retry


def __q_large(session, model, _filters=None, page=0, page_size=None):
    """
    https://stackoverflow.com/questions/13258934/applying-limit-and-offset-to-all-queries-in-sqlalchemy
    :param session:
    :param model:
    :param _filters:
    :param page:
    :param page_size:
    :return:
    """
    if _filters is None:
        _filters = dict()

    query = session.query(model)
    query = __filter_query(model, query, _filters)

    if page_size:
        query = query.limit(page_size)
    if page:
        query = query.offset(page * page_size)
    return query


def __filter_query(model, query, _filters=None):
    """
    https://stackoverflow.com/questions/14845196/dynamically-constructing-filters-in-sqlalchemy
    :param model:
    :param query:
    :param _filters:
    :return:
    """
    for column_op, value in _filters.items():

        column_name, op_name = column_op.split(" ")
        column = getattr(model, column_name, None)

        if not column:
            raise RuntimeError('Invalid filter column: %s' % column_name)

        # https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.properties.ColumnProperty.Comparator
        if op_name == 'in':
            _filter = column.in_(value.split(','))
        else:
            try:
                attr = list(filter(lambda e: hasattr(column, e % op_name), ['%s', '%s_', '__%s__']))[0] % op_name
            except IndexError:
                raise RuntimeError('Invalid filter operator: %s' % op_name)

            if value == 'null':
                value = None
            _filter = getattr(column, attr)(value)
        query = query.filter(_filter)
    return query


@retry(Exception, tries=6, delay=15, back_off=2, logger=logging.getLogger(__name__))
def get_data(conn_str, model, _columns=None, _filters=None, page_size=1000):
    """
    https://stackoverflow.com/questions/11530196/flask-sqlalchemy-query-specify-column-names
    :param conn_str:
    :param model:
    :param _columns:
    :param _filters:
    :param page_size:
    :return:
    """
    s_inception = sessionmaker(bind=create_engine(conn_str, poolclass=NullPool))
    s = s_inception()

    i, result = 0, list()
    while True:
        if _columns is None:
            results = __q_large(s, model, _filters=_filters, page=i, page_size=page_size).all()
        else:
            results = __q_large(s, model, _filters=_filters, page=i, page_size=page_size).options(
                load_only(*_columns)).all()
        if not results:
            break
        for _table in results:
            result.append(_table.__dict__)
        i += 1

    s.close()
    return result
