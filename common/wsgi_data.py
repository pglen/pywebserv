#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, sqlite3, uuid
import wsgi_util, wsgi_func, wsgi_str

sys.path.append("..")
from  pydbase import twincore
from  pydbase import pypacker

# If this is set, use PYDB else use SQLITE

USE_PYDB    = True

def soft_dbfile(modname, suffix = ""):

    if USE_PYDB:
        dbname = "data/%s%s.pydb" % (modname, suffix)
    else:
        dbname = "data/%s%s.sqlt" % (modname, suffix)

    return dbname

# Do we have database handle already?
# This is a regular function, however it interacts with objects ...
# So object oriented paradigmes apply

def soft_opendb(carry, modname, suffix = ""):

    #print("softopen", carry, modname)

    dbname = soft_dbfile(modname, suffix)

    try:
        if USE_PYDB:
            localdb = wsgipydb(dbname)
        else:
            localdb = wsgiSql(dbname)
    except:
        #print("Cannot open database", dbname)
        wsgi_util.put_exception("Cannot open database %s") % carry.localdb

    return localdb

def soft_closedb(db):

    db.close()
    db = None
    pass

def soft_openauthdb(carry, modname, suffix = ""):

    #print("softopen", carry, modname)

    if USE_PYDB:
        carry.authdbname = "data/%s%s.pydb" % (modname, suffix)
    else:
        carry.authdbname = "data/%s%s.sqlt" % (modname, suffix)

    needopen = False
    if not hasattr(carry, "authdb"):
        needopen = True
    else:
        if not carry.authdb:
            ccc = True

    if needopen:
        try:
            if USE_PYDB:
                carry.authdb = wsgipydb(carry.authdbname)
            else:
                carry.authdb = wsgiSql(carry.authdbname)
        except:
            #print("Cannot open database", dbname)
            wsgi_util.put_exception("Open auth database %s") % carry.localdb

def soft_closeauthdb(carry, modname, suffix = ""):

    #print("Soft closing:", carry.dbname, carry.localdb)
    carry.authdb = None

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

    def put(self, key, val, val2, val3, val4, val5):
        #print("put", key, "vals", val, val2, val3, val4)
        sss = self.packer.encode_data("", (val, val2, val3, val4, val5))
        #print("sss", sss)
        ddd = self.packer.decode_data(sss)
        #print("ddd", ddd)
        self.db.save_data(key, sss)

    def delrecall(self, rec):

        # Delete all keys on this record
        #print("delete", rec)
        rec = self.getbyord(int(rec))
        if rec:
            #print("delrec", rec)
            #self.db.core_verbose = 2
            try:
                self.db.del_rec_bykey(rec[0], maxrec = twincore.INT_MAX)
            except:
                #wsgi_util.put_exception("While deleting rec %d" % int(rec))
                #print("exceWhile deleting rec %d", sys.exc_info()) # % int(rec))
                pass

    def getrange(self, beg, count = 1):
        # Get a range of records[ careful dldted records in between
        ccc = self.db.getdbsize()
        print("getrange", beg, count)
        res =  self.getbyord(beg)
        return res

    def  getall(self, checker):
        # get all data, return array
        ccc = self.db.getdbsize()
        arr = []
        for aa in range(ccc - 1, -1, -1):
            aaa = self.getbyord(aa)
            #print("aaa", aaa)
            if not aaa:
                continue
            ccc = aaa[0].decode()
            if ccc not in checker:
                checker.append(ccc)
                #print("checker", ccc)
                # Save ordinal and key and data
                arr.append((aa, aaa[0], *aaa[1:] ))
        check = []
        return arr

    def  getbyord(self, numx):
        # Get ordinal, unscramle it
        #print("by ord", numx)
        sss = self.db.get_rec(int(numx))
        if not sss:
            return None
        #print("sss[0]", sss[0] )#, "sss[1]", sss[1].decode("utf-8") )
        eee = self.packer.decode_data(sss[1].decode("utf-8"))[0]
        ddd = []
        for aa in eee:
            #print("'" +  aa, end="' ")
            ddd.append(aa)

        # Patch filename if none
        if not ddd[4]:
            ddd[4] = "none"
        #print()

        return sss[0], *ddd

    def  getbykey(self, numx):
        pass

    def close(self):
        #print("Soft Closed PYDB", self.file)
        self.db = None
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

    def  getbyord(self, kkk):

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

    def  getrange(self, skip, count = 1):

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

    def   getall(self, checker):
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

class Empty():
    pass

def     load_data_func(strx, context):

    '''
    # ------------------------------------------------------------------------
     Get a row's data; pre load database table as macros.

       Arguments:
           arg[0]      command name
           arg[1]      name of module to get the data from

     Example:
               { loadData proj-edit }
    '''

    ddd = wsgi_func.parse_args(strx, context)

    if context.configx.pgdebug > 2:
        print("load_data_func() ddd", ddd)

    # Fri 03.Mar.2023 data is now returned as an var on the carryon
    # Here we add a class to the context, keyed with the data base / results
    if not hasattr(context, ddd[1]):
        setattr(context, ddd[1], Empty())
    var = getattr(context, ddd[1])
    var.fname   = ddd[1]        # Just for verification
    var.db      = None
    var.data    = None
    var.res     = None

    # Get data from the editor project;
    # Careful, passing the wrong filename, it will be created
    try:
        var.db = soft_opendb(context, ddd[1])
    except Exception as e:
        #print("Could not create / open local data for '%s'" % ddd[1], e)
        wsgi_util.put_exception("Open database")
        return res

    if context.configx.pgdebug > 3:
        print("load_data_func() ddd", ddd, var.db)

    checker = []
    # The data is added to the top of the context object
    try:
        var.res = var.db.getall(checker)
    except:
        wsgi_util.put_exception("Getting Data")
        pass

    # Dump it
    if context.configx.pgdebug > 2:
        if not var.res:
            print("Empty database")
        else:
            for aa in var.res:
                print("res", wsgi_str.strpad(wsgi_str.strupt(str(aa[0]))),
                            wsgi_str.strupt(str(aa[1:])))

    # Sat 25.Feb.2023 deactivted -- data is now in context variable
    # The data is returned as macros, the page can reference
    #wsgi_global.gl_table.add_one_func(prefix + "DLen", str(len(res)))
    #wsgi_global.gl_table.add_one_func(prefix + "Data", res )
    #localdb.close()

    #wsgi_util.printobj(context)
    #wsgi_util.printobj(var)

    return ""

# EOF
