connector = None

def set_connector(conn):
    global connector
    connector = conn

def get_connector():
    global connector
    return connector

def get_connection():
    return get_connector().connection

def get_cursor():
    return get_connection().cursor()

def execute(query, params=None):
  cursor = get_cursor()
  cursor.execute(query, params)
  return cursor

def fetchone(query, params=None):
  cursor = execute(query, params)
  return cursor.fetchone()

def fetchall(query, params=None):
  cursor = execute(query, params)
  return cursor.fetchall()