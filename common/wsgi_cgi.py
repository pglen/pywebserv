#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import sys, os, time, re, traceback, datetime, base64
import wsgi_global, wsgi_parse, wsgi_crypt, wsgi_util

def parse_cgi(environ, configx):

    ''' Module to deal with CGI '''

    request = []

    try:
        # This was a great pain to get this to work ....
        import cgi
        fields = cgi.FieldStorage(fp=environ['wsgi.input'],
                            environ=environ, keep_blank_values=1)

        # The multipart form needed a lot of parsing ...
        for aa in fields:
            if not aa:      # Maybe?
                continue
            #print("aa", aa, fields[aa] )

            try:
                #import wsgi_util
                #wsgi_util.printobj(fields[aa])

                # Is it a multipart entry?
                if  hasattr(fields[aa], "disposition_options") and \
                            fields[aa].disposition_options != {}:
                    #print("disposition_options", fields[aa].disposition_options)
                    # File entry?
                    if fields[aa].filename:
                        dt = datetime.datetime.now()
                        fdt = dt.strftime('%y%m%d-%H_%M-')

                        encname = fdt + fields[aa].filename
                        fname = configx.datapath + "media" + os.sep + encname
                        #print("Decode / Save file", fname)

                        try:
                            fp = open(fname, "wb")
                            fp.write(fields[aa].value)
                            fp.close()
                        except:
                            wsgi_util.put_exception("Cannot save uplooded file %s" % encname)

                        # Remember the file name as a submit variable
                        #if hasattr(fields[aa], "disposition_options") \
                        #        and hasattr( fields[aa].disposition_options, "name"):
                        #    nnn = fields[aa].disposition_options['name']

                        request.append( \
                            (fields[aa].disposition_options['name'], encname) )
                    else:
                        nn = fields[aa].disposition_options['name']
                        vv =  fields[aa].value
                        #print("Multipart regular", nn, vv)
                        request.append((nn, vv))
                else:
                    if hasattr(fields[aa], "name"):
                        nnn =  fields[aa].name
                    else:
                        nnn = fields[aa][0]

                    if hasattr(fields[aa], "value"):
                        vvv =  fields[aa].value
                    else:
                        vvv = fields[aa][2]

                    #print("field", nnn, vvv)
                    request.append((nnn, vvv))

            except:
                wsgi_util.put_exception("Error on cgi parse")

        #print("got file len = ", len(fff))
        #print("Request_org", request_org)
        #request = parse_qsl(str(request_org), keep_blank_values=True)

        # Deliver a sorted list so the original field order is preserved
        if request:
            request.sort()

            if configx.pgdebug > 4:
                for aa in request:
                    print("Request", aa)

    except:
        #print("No post data", sys.exc_info())
        wsgi_util.put_exception("No post data")
        pass

    return request