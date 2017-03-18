# encoding: utf-8

import sqlite3
from datetime import datetime

class SQLiteLogger:
    """
    Class defining a logger using a SQLite database
    """

    def __init__(self, filename="logs.db"):
        self.filename = filename
        
        self.conn_write = sqlite3.connect(self.filename)
        c = self.conn_write.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()

        if len(tables) == 0:
            c.execute("CREATE TABLE api_calls (id INTEGER PRIMARY KEY, type TEXT NOT NULL, ip TEXT, application TEXT, date TIMESTAMP, duration REAL DEFAULT 0.0)")
            c.execute("CREATE TABLE text (id INTEGER PRIMARY KEY, api_call_id INTEGER, text TEXT)")
            c.execute("CREATE TABLE tokens (id INTEGER PRIMARY KEY, text_id INTEGER, token TEXT, tag TEXT)")
            c.execute("CREATE TABLE tokenised_text (id INTEGER PRIMARY KEY, text_id INTEGER, result TEXT)")
            self.conn_write.commit()
        
        c.close()
        self.conn_write.close()

    def log_api_call(self, call_type, ip, application):
        now = datetime.now()

        conn_write = sqlite3.connect(self.filename)
        curs = conn_write.cursor()
        curs.execute("INSERT INTO api_calls(type, ip, application, date) VALUES(?, ?, ?, ?)", (call_type, ip, application, now))
        last_row_id = curs.lastrowid
        
        conn_write.commit()
        curs.close()
        conn_write.close()

        return last_row_id

    def log_api_call_time(self, api_id, duration):
        conn_write = sqlite3.connect(self.filename)
        curs = conn_write.cursor()

        curs.execute("UPDATE api_calls SET duration = ? WHERE id = ?", (duration, api_id))

        conn_write.commit()
        curs.close()
        conn_write.close()

    def log_tokens(self, text_id, tokens_list):
        conn_write = sqlite3.connect(self.filename)
        curs = conn_write.cursor()
        for token in tokens_list:
            if type(token) == str:
                curs.execute("INSERT INTO tokens(text_id, token) VALUES(?, ?)", (text_id, token))
            else: # It is the result of a tag
                curs.execute("INSERT INTO tokens(text_id, token, tag) VALUES(?, ?, ?)", (text_id, token[0], token[1]))
                
        conn_write.commit()
        curs.close()
        conn_write.close()

    def log_text(self, api_call_id, text):
        conn_write = sqlite3.connect(self.filename)
        curs = conn_write.cursor()
        curs.execute("INSERT INTO text(api_call_id, text) VALUES(?, ?)", (api_call_id, text))
        last_row_id = curs.lastrowid
        
        conn_write.commit()
        curs.close()
        conn_write.close()

        return last_row_id

    def log_tokenised_text(self, text_id, tokenised_text):
        conn_write = sqlite3.connect(self.filename)
        curs = conn_write.cursor()
        curs.execute("INSERT INTO tokenised_text(text_id, result) VALUES(?, ?)", (text_id, tokenised_text))
        last_row_id = curs.lastrowid

        conn_write.commit()
        curs.close()
        conn_write.close()

        return last_row_id

    ###########
    # Getters #
    ###########
    def get_api_calls(self):
        """
        Returns all the API calls made to the tokeniser
        Contains the method (type), the ip and the app which made the call
        """
        conn_read = sqlite3.connect(self.filename, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        curs = conn_read.cursor()

        curs.execute("SELECT * FROM api_calls")

        api_calls = curs.fetchall()
        curs.close()
        conn_read.close()

        return api_calls

    def get_api_call_id(self, id_call):
        """
        Returns a specific API call, identified by its ID
        """
        conn_read = sqlite3.connect(self.filename, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        curs = conn_read.cursor()

        curs.execute("SELECT a.id, type, ip, application, date, text, result, duration FROM api_calls a JOIN text t ON a.id = t.api_call_id JOIN tokenised_text tt ON tt.text_id = t.id WHERE a.id=?", (id_call,))

        api_call = curs.fetchone()
        curs.close()
        conn_read.close()

        return api_call

    def get_unique_ips(self):
        """
        Returns a list of all the IPs which used the API and the number of times they did
        """
        conn_read = sqlite3.connect(self.filename, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        curs = conn_read.cursor()

        curs.execute("SELECT ip, COUNT(ip) FROM api_calls GROUP BY ip ")

        ips = curs.fetchall()
        curs.close()
        conn_read.close()

        return ips

    def get_list_tokens(self):
        """
        Returns all the tokens ever tokenised.
        """
        conn_read = sqlite3.connect(self.filename)
        curs = conn_read.cursor()

        curs.execute("SELECT * FROM tokens ORDER BY id ASC")

        tokens = curs.fetchall()
        curs.close()
        conn_read.close()

        return tokens

    def get_unique_tokens(self):
        """
        Returns every unique token and the number of times it appears in the DB
        """
        conn_read = sqlite3.connect(self.filename)
        curs = conn_read.cursor()

        curs.execute("SELECT token, COUNT(token) FROM tokens GROUP BY token")

        tokens = curs.fetchall()
        curs.close()
        conn_read.close()

        return tokens

    def get_list_texts(self):
        """
        Retrieves all the texts tokenised
        """
        conn_read = sqlite3.connect(self.filename)
        curs = conn_read.cursor()

        curs.execute("SELECT * FROM text ORDER BY id ASC")

        texts = curs.fetchall()
        curs.close()
        conn_read.close() 

        return texts

    def get_tokenised_text(self, text_id):
        """
        Gets the tokenised result corresponding to a given text
        """
        conn_read = sqlite3.connect(self.filename)
        curs = conn_read.cursor()

        curs.execute("SELECT * FROM tokenised_text WHERE text_id = ?", (text_id,))

        tokenised = curs.fetchone()[0]
        curs.close()
        conn_read.close()

        return tokenised

    def get_tokens_for_text(self, text_id):
        """
        Gets the tokens corresponding to a given text
        """
        conn_read = sqlite3.connect(self.filename)
        curs = conn_read.cursor()

        curs.execute("SELECT * FROM tokens WHERE text_id = ?", (text_id,))

        tokens = curs.fetchall()
        curs.close()
        conn_read.close()

        return tokens

    def get_tags_for_token(self, token):
        """
        Gets the tags which where assigned to a given token
        """
        conn_read = sqlite3.connect(self.filename)
        curs = conn_read.cursor()

        curs.execute("SELECT tag, api_call_id FROM tokens t JOIN text tx ON t.text_id=tx.id WHERE token = ?", (token,))

        tags = curs.fetchall()
        print(tags)
        curs.close()
        conn_read.close()

        return tags
