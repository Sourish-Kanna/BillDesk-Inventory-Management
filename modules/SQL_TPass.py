#SQL_TPass Source Code
import mysql.connector as sql

def Pass():
    """Password Interface for debuging"""

    user = 'root'
    print("Enter Username:",user)
    pas = input('Enter Password: ')
    try:
        demodb = sql.connect(host="localhost", user=user, passwd=pas)
        demodb.close()
        return pas, user
    except sql.errors.ProgrammingError:
        print("Wrong password")
        return None, None


if __name__ == '__main__':
    print(Pass())
    from time import sleep
    sleep(2.5)

