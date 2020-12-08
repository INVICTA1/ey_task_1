import mysql.connector
from mysql.connector import Error

'''Connected to mysql server'''
def insert_request_in_database(request):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='ey',
                                       user='admin',
                                       password='admin',
                                       auth_plugin='mysql_native_password',
                                       port=3306)
        try:
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(request)
                if str(request).__contains__("select"):
                    response = []
                    for i in cursor:
                        response.append(i)
                    return response
                conn.commit()
            else:
                return 'database is not connected'

        except Error as e:
            print(e)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.close()



    except Error as e:
        print(e)


if __name__ == '__main__':
    pass
