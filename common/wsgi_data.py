#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, sqlite3, uuid
import wsgi_util

sys.path.append("../..")
from  pydbase import twincore
from  pydbase import pypacker

# If this is set, use PYDB else use SQLITE

USE_PYDB    = True

# Do we have database handle already?

def soft_opendb(carry, modname, suffix = ""):

    if USE_PYDB:
        dbname = "data/%s%s.pydb" % (modname, suffix)
    else:
        dbname = "data/%s%s.sqlt" % (modname, suffix)

    #print("database name", dbname)

    needopen = False
    if not hasattr(carry, "localdb"):
        needopen = True
    else:
        # see if DB is OK
        try:
            if USE_PYDB:
                #conn = pyd
                pass
            else:
                conn = sqlite3.connect(file)
                c = conn.cursor()
                c.execute("select count(*) from " + self.table + "")
                conn.close()
        except:
            #print("Cannot open/create db:", file, sys.exc_info())
            needopen = True

    if needopen:
        try:
            if USE_PYDB:
                carry.localdb = wsgipydb(dbname)
            else:
                carry.localdb = wsgiSql(dbname)
        except:
            #print("Cannot open database", dbname)
            wsgi_util.put_exception("Open database %s") % dbname

class wsgipydb():

    '''! The data store for the web server. Simple PYDB data files.
      '''

    def __init__(self, file, table = "initial"):

        self.table = table
        self.file = file
        self.packer = pypacker.packbin()
        self.db = twincore.TwinCore(self.file)

    def getcount(self):
        ret = self.db.getdbsize()
        return ret

    def put(self, key, val, val2, val3, val4):
        #print("put", key, "vals", val, val2, val3, val4)
        sss = self.packer.encode_data("", (val, val2, val3, val4))
        #print("sss", sss)
        ddd = self.packer.decode_data(sss)
        #print("ddd", ddd)
        self.db.save_data(key, sss)

    def  getbyid(self, kkk):
        #print("byid", kkk)
        sss = self.db.get_rec(int(kkk))
        #print("sss[0]", sss[0], "sss[1]", sss[1].decode("utf-8") )
        ddd = self.packer.decode_data(sss[1].decode("utf-8"))
        #print("ddd", *ddd[0])
        return sss[0].decode("utf-8"), *ddd[0]

    def close(self):
        #print("Closed PYDB", self.file)
        #self.conn.close()
        #self.db.__del__()
        pass

    def __delete__(self):
        print("delete pydb", self)

# ------------------------------------------------------------------------

class wsgiSql():

    '''! The data store for the web server. Simple sqlite data files.
      one global file is created, and a local file may be created on
      a per project basis
      '''

    def __init__(self, file, table = "initial"):

        self.table = table
        self.file = file
        try:
            self.conn = sqlite3.connect(file)
        except:
            print("Cannot open/create db:", file, sys.exc_info())
            return

        try:
            self.c = self.conn.cursor()
            # Create table
            self.c.execute("create table if not exists " + self.table + "\
             (pri INTEGER PRIMARY KEY, key text, uuid text, val text, val2 text, val3 text, val4 text)")
            self.c.execute("create index if not exists iconfig on " + self.table + " (key)")
            self.c.execute("create index if not exists pconfig on " + self.table + " (pri)")
            self.c.execute("PRAGMA synchronous=OFF")
            # Save (commit) the changes
            self.conn.commit()
        except:
            print("Cannot create sql table ", sys.exc_info())

        finally:
            # We close the cursor, we are done with it
            #c.close()
            pass

        self.table2 = "weblog"
        try:
            # Create table
            self.c.execute("create table if not exists " + self.table2 + "\
             (pri INTEGER PRIMARY KEY, key text, val text, val2 text, val3 text, val4 text)")
            self.c.execute("create index if not exists ilogconfig on " + self.table2 + " (key)")
            self.c.execute("create index if not exists plogconfig on " + self.table2 + " (pri)")
            self.c.execute("PRAGMA synchronous=OFF")
            # Save (commit) the changes
            self.conn.commit()
        except:
            print("Cannot create sql table ", sys.exc_info())

        #print("Created/Opened SQl", self.file)

    # --------------------------------------------------------------------
    # Return None if no data

    def  get(self, kkk):
        rr = None
        try:
            self.c.execute("select * from " + self.table + " indexed by iconfig where key = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("Cannot get sql data", sys.exc_info())
            rr = None
            raise
        finally:
            pass
        if rr:
            return rr[1:]
        else:
            return None

    # --------------------------------------------------------------------
    # Return None if no data

    def  getbyid(self, kkk):

        #print("byid", kkk)
        rr = None
        try:
            self.c.execute("select * from " + self.table + \
                             " indexed by iconfig where pri = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("Cannot get sql data", sys.exc_info())
            rr = None
            raise
        finally:
            pass
        if rr:
            return rr
        else:
            return None

    # --------------------------------------------------------------------
    # Return None if no data

    def  getrange(self, skip, count):

        #print("byid", kkk)
        rr = None
        try:
            self.c.execute("select * from " + self.table + \
                             " limit %d offset %d" % (int(count), int(skip) ) )

            rr = self.c.fetchall()
        except:
            wsgi_util.put_exception("getrange ")
            print("Cannot get sql data", sys.exc_info())
            rr = None
            raise
        finally:
            pass
        if rr:
            return rr
        else:
            return None

    # --------------------------------------------------------------------
    # Return False if cannot put data

    def   put(self, key, val, val2, val3, val4):

        #got_clock = time.clock()

        ret = True
        try:
            self.c.execute("select * from " + self.table + \
                            " indexed by iconfig where key == ?", (key,))
            rr = self.c.fetchall()
            if rr == []:
                #print( "inserting")
                uuidx = str(uuid.uuid4())
                self.c.execute("insert into " + self.table + \
                        " (key, uuid, val, val2, val3, val4) \
                            values (?, ?, ?, ?, ?, ?)", \
                                (key, uuidx, val, val2, val3, val4))
            else:
                #print ("updating")
                self.c.execute("update " + self.table +
                    " indexed by iconfig set " \
                        " val = ?, val2 = ?, val3 = ?, val4 = ? " \
                            " where key = ?", \
                                (val, val2, val3, val4, key))
            self.conn.commit()
        except:
            print("Cannot put sql data", sys.exc_info())
            ret = False
        finally:
            #c.close
            pass

        #self.take += time.clock() - got_clock

        return ret

    # --------------------------------------------------------------------
    # Return False if cannot put data

    def   putlog(self, key, val, val2, val3, val4):

        ''' Special function to write to the log.
            Use sqliteviewer to see it.
            Usinf Sqlite prevents all sorts of cross log issues
        '''

        #got_clock = time.clock()

        ret = True
        try:
            self.c.execute("select * from " + self.table2 + " indexed by ilogconfig where key == ?", (key,))
            rr = self.c.fetchall()
            if rr == []:
                #print( "inserting")
                self.c.execute("insert into " + self.table2 + " (key, val, val2, val3, val4) values (?, ?, ?, ?, ?)", (key, val, val2, val3, val4))
            else:
                #print ("updating")
                self.c.execute("update " + self.table2 + " indexed by ilogconfig set val = ?, val2 = ?, val3 = ?, val4 = ? where key = ?",\
                                     (val, val2, val3, val4, key))
            self.conn.commit()
        except:
            print("Cannot put sql log data", sys.exc_info())
            ret = False
        finally:
            #c.close
            pass

        #self.take += time.clock() - got_clock

        return ret

    # --------------------------------------------------------------------
    # Get All

    def   getall(self):
        rr = None
        try:
            self.c.execute("select * from " + self.table + "")
            rr = self.c.fetchall()
        except:
            print("Cannot get ALL sql data", sys.exc_info())
        finally:
            #c.close
            pass
        return rr

    # --------------------------------------------------------------------
    # Get Count of records

    def   getcount(self):
        rr = None
        try:
            self.c.execute("select count(*) from " + self.table + "")
            rr = self.c.fetchall()
        except:
            print("Cannot get count sql data", sys.exc_info())
        finally:
            #c.close
            pass
        #print("rr", rr)
        return rr[0][0]

    # --------------------------------------------------------------------
    # Return None if no data

    def   rmall(self):
        print("removing all")
        try:
            self.c.execute("delete from " + self.table + "")
            rr = self.c.fetchone()
        except:
            print("Cannot delete sql data", sys.exc_info())
        finally:
            pass
        if rr:
            return rr[1]
        else:
            return None

    def close(self):
        #print("Closed SQL", self.file)
        self.conn.close()

    def __delete__(self):
        print("delete", self)
