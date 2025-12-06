import sqlite3


def connect_sql():
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    return cursor,connect


def create_table():
    cursor,connect = connect_sql()
    sql = """CREATE TABLE if not exists requisicao (

    name varchar(255),
    symbol varchar(10),
    price varchar(30),
    timestamp varchar(30)
    )"""
    try:
        cursor.execute(sql)
    except Exception as e:
        print('Ocorreu um erro ')
    finally:
        cursor.close()


def insert_table(table,placeholders,columns,data_to_insert):
    sql_insert = f"""
    INSERT INTO {table} ({columns}) values ({placeholders})
    """
    cursor,connect = connect_sql()
    try:
        cursor.execute(sql_insert,data_to_insert)
        connect.commit()
        print("Dados inseridos com suscesso")
        return "Dados inseridos com suscesso"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    return 

    