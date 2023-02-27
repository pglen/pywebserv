# pywebserv Wsgi Web Server

## WSGI compliant web server

 Web server with no dependencies (for security). One might say this is a framework-less framework.

###  Introduction

 This is a web server framework. To wet your apetite, here is how simple the
HTML web page becomes. Below, is the source for the example pages. The macros can be crafted
by you, so the simplicity is by no means a limitation.  (Helps to know html/python)

        { sitestyle }
        { header }

        <table width=100%  cellspacing=2 cellpadding=0 border=0>
            <tr><td bgcolor=#eeeeee width=15% valign=top>
                { left }
                { center }
                { nav }
                { right }
        </table>
        <table width=100% { sitecolor }>
            { footer }
        </table>

  What works:

   * First page delivered
   * Dynamic page gen.
   * Template expansion { vars } are substituted recursively
   * Connected to apache2 (tests OK)
   * Image re-size from { vars } arguments ex: { image any.png 800 }
   * First test site (see below)
   * Apache binding tested via the WSGI interface
   * Working out the details

 The web site 'upp' can be seen as a working example.

### Development

   Assuming Linux / Firefox setup; start the ./mock_server.py in a terminal. This will
   start a web server, and serve the site on port 8000. Connect firefox to localhost:8000.
   Edit away; When a file is modified, the 'wsgi_server' utility will refresh
   the firefox page. Instant feedback without the load / refresh cycle. Natually, other
   setups can be adjusted for, see source for details.

 On the screen shot below, images are added, images are dynamically re sized with the PIL
 library;

  ![screen shot of image processing](content/siteicons/next_step.png)

 Projects are added in a separate sub directory;
 The projects are isolated, errors in the project do not influence (down) the site;
 only the page with the error, and (only) an error message shows.

  ![screen shot of project and tiles processing](content/siteicons/tiles.png)

#### Driving the macros:

      Variable subst regex: "{ .*? }"  (example: { header } )
      Command parameter subst regex: "[ .*? ]"  (example: [ value_one ] )

      See index.html for examples.

| Directories          | Usage                    |
|  --------------------|--------------------------|
|  /content/proj*      |  applications / projects |
|  /content/siteicons/ |  icons                   |
|  /content/media/     |  image content           |
|  /content/css/       |  global css files        |
|  /content/common/    |  python scripts (wsgi interface) |
|  /content/static/    |  static (non changing) content |

### Flow of presenting the pages:

    url lookup in main ->
        if entry present
            if html file exists:
                expand macro -> present page
            else
                call function in url table
                function fills in everything -> present it
        else
            if static file ->
                present it
            else
                if 404 or error file
                    present it
                else
                    404 error message

 To create a new project:

    Add a directory to the web server's "./content/" directory
        that starts with 'proj' (like proj-hello or proj-sales)
    fill in the directory with content
        o Initial .py file to configure the project (index.py)
        o Content that responds to the callbacks, or ..
		...  content presented as is

    See proj-index for an example home page. Also proj* for more
    detailed examples.
    Please note how simple a calendar implementation becomes.

 ## Encryption:

 The encrytion is a simple module in python. It is using the
 techniques the big boys are using ... backward forward scans an all.
 Do not be fooled; onece you encrypt; make sure you have the
 keys etc .. to recover.

 Strength:

  The following section should point to some good (and needed) properties.
 Changing the cyphertext by one digit, scrambles the whole cyphertext.
 Same happens with the key; Changing one digit will scramble the cyphertext.

        ./wsgi_crypt.py 1235 qrs
        tdelta 0.2280 ms
        org  1235
        enco b'HnUEIw=='
        org4 1235

        ./wsgi_crypt.py 1235 qrt
        tdelta 0.0336 ms
        org  1235
        enco b'JJc1zw=='
        org4 1235

        ./wsgi_crypt.py 1234 qrt
        tdelta 0.0342 ms
        org  1234
        enco b'HYMZwQ=='
        org4 1234

  The cookie handing is using this encryption for self check. See source
for details.

### History:

    Fri 16.Apr.2021 Skeleton project
    Sun 18.Apr.2021 Apache tests OK
    Mon 19.Apr.2021 Turned icons/ to siteicons/ (for apache not to redirect)
    Thu 22.Apr.2021 Projects in separate dir, reverse isolation
    Mon 27.Sep.2021 Moved user contents to the subdir 'content' (more isolation)
    Tue 28.Sep.2021 Cleanup, first useful site
    Sun 20.Mar.2022 First live site on the web
    Sat 26.Mar.2022 World peace pages
    Tue 28.Jun.2022 Created unitedplanetpeace.com proto site
    Sat 16.Jul.2022 Site dev continues
    Sun 13.Aug.2022 Restructured main OBJ creation
    Sun 13.Nov.2022 Added dynamic / responsive page feature
    Sun 26.Feb.2023 Added encryption and safe cookies

    Also see 'git log' for more

## Apache config (example on port 7777)

 Please replace your directory / script location as appropriate. Note that
the server is in test mode, exposes itself on port 7777;

	Listen 7777

	<VirtualHost *:7777>
	  ServerName localhost
	  LogLevel error
	  WSGIScriptAlias / /home/myhome/pgpygtk/webserver/wsgi_main.py
	  DocumentRoot /home/myhome/pgpygtk/webserver
	<Directory /home/myhome/pgpygtk/webserver>
	  SetHandler wsgi-script
	  Options ExecCGI
	  Require all granted
	    <Files wsgi_main.py>
	      Require all granted
	    </Files>
	</Directory>
	</VirtualHost>

## License

 Open source.

 PG
