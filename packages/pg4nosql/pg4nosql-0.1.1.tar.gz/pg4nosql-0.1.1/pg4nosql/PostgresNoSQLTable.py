import json
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
from pg4nosql import DEFAULT_JSON_COLUMN_NAME, DEFAULT_ROW_IDENTIFIER
from pg4nosql.PostgresNoSQLResultItem import PostgresNoSQLResultItem


class PostgresNoSQLTable(object):

    __SQL_INSERT_JSON = "INSERT INTO %s("+DEFAULT_JSON_COLUMN_NAME+" %s) VALUES(%s %s) RETURNING "+DEFAULT_ROW_IDENTIFIER
    __SQL_QUERY_JSON = 'SELECT %s FROM %s WHERE %s'
    __SQL_GET_JSON = 'SELECT * FROM %s WHERE '+DEFAULT_ROW_IDENTIFIER+'=%s'
    __SQL_GET_COLUMNS = 'select column_name from information_schema.columns where table_name = %s'
    __SQL_DELETE_JSON = 'DELETE FROM %s WHERE '+DEFAULT_ROW_IDENTIFIER+'=%s'
    __SQL_UPDATE_JSON = 'UPDATE %s SET '+DEFAULT_JSON_COLUMN_NAME+'=%s %s WHERE '+DEFAULT_ROW_IDENTIFIER+'=%s;'

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.cursor_factory = RealDictCursor
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def put(self, data, relational_data={}):
        # todo: replace string concatenation with a beautiful solution
        relational_data_columns = ''
        relational_data_values = ''

        if relational_data:
            relational_data_columns = ',' + ",".join(relational_data.keys())
            relational_data_values = ",'" + "','".join(relational_data.values()) + "'"

        self.cursor.execute(self.__SQL_INSERT_JSON, (AsIs(self.name),
                            AsIs(relational_data_columns), json.dumps(data), AsIs(relational_data_values)))
        return self.cursor.fetchone()[DEFAULT_ROW_IDENTIFIER]

    def save(self, record):
        record = record.get_record()

        data = record.pop(DEFAULT_JSON_COLUMN_NAME)
        object_id = record.pop(DEFAULT_ROW_IDENTIFIER)

        relational_data_sql = ''.join(", %s='%s'" % (key, val) for (key, val) in record.iteritems())

        self.cursor.execute(self.__SQL_UPDATE_JSON, (AsIs(self.name),
                            json.dumps(data), AsIs(relational_data_sql), object_id))

    def get(self, object_id):
        self.cursor.execute(self.__SQL_GET_JSON, (AsIs(self.name), object_id))
        return PostgresNoSQLResultItem(self.cursor.fetchone())

    def query(self, query='True', columns='*'):
        self.cursor.execute(self.__SQL_QUERY_JSON, (AsIs(columns), AsIs(self.name), AsIs(query)))
        rows = [item for item in self.cursor.fetchall()]
        items = map(lambda r: PostgresNoSQLResultItem(r), rows)
        return items

    def query_one(self, query='True', columns='*'):
        result = self.query(query, columns)
        if not result:
            return None
        return result[0]

    def get_columns(self):
        self.cursor.execute(self.__SQL_GET_COLUMNS, (self.name,))
        columns = map(lambda m: m['column_name'], self.cursor.fetchall())
        return columns

    def delete(self, object_id):
        self.cursor.execute(self.__SQL_DELETE_JSON, (AsIs(self.name), object_id))
