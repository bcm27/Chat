from datetime import datetime
import pymysql.cursors  # pip install PyMySQL
import time
import util.server.serverUtils as sUtils


class DBMethods:
    # Connect to the solar DB, static instance, always open, until closeConnection is called
    connection = pymysql.connect(host='solar-vh1', user='cs333', password='cs333',
                                 db='cs333group3', cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def register(username, hashed_password):
        """
        Check to see if there's already a username stored in the DB,
        if there's not, add a new user to the DB

        :param username: The username of the user
        :param hashed_password: The hashed password of the user
        :return: True if a user is successfully created, false if not
        """
        conn = DBMethods.connection  # shorthand variable
        try:
            with conn.cursor() as cursor:
                # Check if a user exists with the username already
                cursor.execute("SELECT * FROM user WHERE username = %s", [username])

                # If there's no user with that username in the DB (good)
                if not cursor.fetchone():
                    # Add a new user into the DB
                    cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)",
                                   (username, hashed_password))
                    conn.commit()
                    return True
                else:
                    return False
        except Exception as e:
            print("addUserToDB Error:", e)
            return False

    @staticmethod
    def login(username, hashed_password):
        """
        Connect to the DB, check for a user matcher |username|, and if the DB's
        hashed password matched |hashed_password|, then the user has provided
        valid credentials, so we send them a valid JWT to make future requests with

        :param username: The username of the account logging in
        :param hashed_password: The already hashed password, passed in by the client
        :return: Returns a JWT if successfully logged in, or None if not
        """
        conn = DBMethods.connection  # shorthand variable
        try:
            with conn.cursor() as cursor:
                # Ensure that a user exists that matches the provided username
                cursor.execute("SELECT * FROM user WHERE username = %s", [username])
                user = cursor.fetchone()
                if user is not None:
                    # If a user exists, go ahead and test login conditions
                    lock_time = user["lock_until"]
                    attempts = user["login_attempts"]

                    # If the user hasn't made too many attempts, OR their account is unlocked, and should be
                    # allowed another attempt at logging in
                    if attempts < 4 or attempts >= 4 and lock_time is not None and lock_time < datetime.now():
                        # If the provided password matches the DB password
                        if user["password"] == hashed_password:
                            # If we have any attempts at all, we should reset them
                            if attempts > 0:
                                cursor.execute("UPDATE user "
                                               "SET login_attempts = 0, lock_until = NULL "
                                               "WHERE username = %s",
                                               [username])
                                conn.commit()
                            # Then return a JWT to the user, with their username embedded
                            return sUtils.encodeJWT(username)
                        # Else, if the user has less than 4 attempts made, and their password was incorrect
                        elif attempts < 4:
                            # Add an attempt to their account
                            cursor.execute("UPDATE user SET login_attempts = login_attempts + 1 WHERE username = %s",
                                           [username])
                            conn.commit()
                    # Otherwise, their account is not locked, and the user has attempted to login
                    # unsuccessfully too many times
                    elif attempts >= 4:
                        # So we go ahead and set their lock_until time to 5 minutes in the future
                        future = datetime.strptime(time.ctime(time.time() + 300), "%a %b %d %H:%M:%S %Y")
                        cursor.execute("UPDATE user SET lock_until = %s WHERE username = %s", [future, username])
                        conn.commit()
                        attempts = 1
                        return "<FAILED LOGIN ATTEMPTS>"
        except Exception as e:
            print("getUserFromDB Error:", e)

    @staticmethod
    def closeConnection():
        """
        Close the DB connection
        """
        DBMethods.connection.close()
