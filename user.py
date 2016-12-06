import sqlite3
import hashlib

DATABASE = "data.db"

def add_user(username, password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    query = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)"
    c.execute(query, (username, hashlib.sha1(password).hexdigest(), '', '',))

    db.commit()
    db.close()

def get_user(**kwargs):
    if not kwargs:
        return None

    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    criterion = []
    params = []
    for k,v in kwargs.items():
        criterion.append("%s = ?" % k)
        params.append(str(v))

    query = "SELECT * FROM users WHERE %s" % " AND ".join(criterion)
    c.execute(query, params)

    result = c.fetchone()
    db.close()
    return result


