#!flask/bin/python

#DB connector
#Author: Chiraag

import psycopg2
from psycopg2.extensions import AsIs
import psycopg2.extensions
from psycopg2.extras import RealDictCursor
import psycopg2.extras
import logging
import logging.handlers


class DB(object):
    def __init__(self, conn_str=None, logger=None):
        self.conn_str = conn_str
        self.conn = None
        self.logger =logger

    def connect(self):
        '''
            Connect to the Db
        '''
        try:
            self.conn = psycopg2.connect(self.conn_str)
            self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        except Exception, e:
            if s.logger:
                self.logger.critical("Connecting to the DB failed: %s"%(str(e)))
            else:
                print "I am unable to connect to the database :", str(e)

    def run_select_query(self, query):
        '''
            Run query
        '''
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception, e:
            if self.logger:
                self.logger.critical("run_select_query failed in DB: %s"%(str(e)))
            else:
                print "Unable to run query", str(e)
            return None

    def call_proc(self, proc,data):
        '''
            Run proc
        '''
        try:
            row_data = None
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.callproc(proc, data)
            row_data = cur.fetchone()
            self.conn.commit()
            cur.close()
            if row_data:
                row = row_data[0]
                if row:
                    return row
            return None
        except Exception, e:
            if self.logger:
                self.logger.critical("call_proc failed in DB: %s"%(str(e)))
            else:
                print "Issue with ret proc :", str(e)
            return None

    def disconnect(self):
        '''
            Disconnect
        '''
        try:
            self.conn.close()
        except Exception, e:
            if self.logger:
                self.logger.critical("disconnect failed in DB: %s"%(str(e)))
            else:
                print "I am unable to disconnect :", str(e)
