from configparser import ConfigParser
# if spyder is part of the workflow, uncomment the next two lines
# import nest_asyncio
# nest_asyncio.apply()
import pymysql

# get config info
def get_config(fn, section):
    parser = ConfigParser()
    parser.read(fn)
    db = parser.items(section)
    return {name: value for name, value in db}

def create_table(conn):
    try:
        with conn.cursor() as cursor:
            q = "CREATE TABLE IF NOT EXISTS engagement(user varchar(32), score int);"
            cursor.execute(q)
            conn.commit()
    except Exception as e:
        print("Exception occured: {}".format(e))

# fetch the table from the SQL 
def fetch_users(conn):
    try:
        with conn.cursor() as cursor:
            q = "SELECT * FROM engagement;"
            cursor.execute(q)
            table = cursor.fetchall()
            return [[t['user'] for t in table],[t['score'] for t in table]]
    except Exception as e:
        print("Exception occured: {}".format(e))

# update the engagement table depending on user action
def add_engagement(user,score,conn):
    try:
        if user not in fetch_users(conn)[0]:
            with conn.cursor() as cursor:
                q = 'INSERT INTO engagement VALUES (%s, CAST(%s AS INT));'
                cursor.execute(q, (user,str(score)))
                conn.commit()
        else:
            index = fetch_users(conn)[0].index(user)
            with conn.cursor() as cursor:
                q = "UPDATE engagement SET score = CAST(%s AS INT) WHERE user = %s;"
                cursor.execute(q, (str(fetch_users(conn)[1][index]+score),user))
                conn.commit()
    except Exception as e:
        print("Exception occured: {}".format(e))