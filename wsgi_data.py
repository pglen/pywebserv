#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, sqlite3

class wsgiSql():

    def __init__(self, file, table = "initial"):

        self.table = table

        try:
            self.conn = sqlite3.connect(file)
        except:
            print("Cannot open/create db:", file, sys.exc_info())
            return

        try:
            self.c = self.conn.cursor()
            # Create table
            self.c.execute("create table if not exists " + self.table + "\
             (pri INTEGER PRIMARY KEY, key text, val text, val2 text, val3 text, val4 text)")
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
            self.c.execute("create index if not exists iconfig on " + self.table2 + " (key)")
            self.c.execute("create index if not exists pconfig on " + self.table2 + " (pri)")
            self.c.execute("PRAGMA synchronous=OFF")
            # Save (commit) the changes
            self.conn.commit()
        except:
            print("Cannot create sql table ", sys.exc_info())

    # --------------------------------------------------------------------
    # Return None if no data

    def   get(self, kkk):
        try:
            if os.name == "nt":
                self.c.execute("select * from " + self.table + " where key = ?", (kkk,))
            else:
                self.c.execute("select * from " + self.table + " indexed by iconfig where key = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("Cannot get sql data", sys.exc_info())
            rr = None
        finally:
            pass
        if rr:
            return rr[1:]
        else:
            return None

    # --------------------------------------------------------------------
    # Return False if cannot put data

    def   put(self, key, val, val2, val3, val4):

        #got_clock = time.clock()

        ret = True
        try:
            if os.name == "nt":
                self.c.execute("select * from " + self.table + " where key == ?", (key,))
            else:
                self.c.execute("select * from " + self.table + " indexed by iconfig where key == ?", (key,))
            rr = self.c.fetchall()
            if rr == []:
                #print( "inserting")
                self.c.execute("insert into " + self.table + " (key, val, val2, val3, val4) values (?, ?, ?, ?, ?)", (key, val, val2, val3, val4))
            else:

                #print ("updating")
                if os.name == "nt":
                    self.c.execute("update " + self.table + " set val = ?, val2 = ?, val3 = ?, val4 = ? where key = ?",\
                                     (val, val2, val3, val4, key))
                else:
                    self.c.execute("update " + self.table + " indexed by iconfig set val = ?, val2 = ?, val3 = ?, val4 = ? where key = ?",\
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
    # Get All

    def   getall(self):
        try:
            self.c.execute("select * from " + self.table + "")
            rr = self.c.fetchall()
        except:
            print("Cannot get sql data", sys.exc_info())
        finally:
            #c.close
            pass
        return rr

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

