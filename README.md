# Wsgi Web Server

## WSGI compliant web server

 Web server with no dependencies (for security). One might say this is a framework-less framework.

###  Introduction

 This is a simple web server framework. To wet your apetite, here is how simple the
HTML web page becomes. This is the source for the example pages. The macros can be crafted
by you, so the simplicity is by no means a limitation.  (helps to know html/python)

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
   * Dynamic page gen
   * Template expansion { vars } are substituted recursively
   * connected to apache2 (tests OK)
   * image re-size from { vars } arguments ex: { image any.png 800 }
   * first test site (see below)
   * apache binding tested via the WSGI interface



 History:

    Sun 20.Mar.2022 First live site on the web
    Tue 28.Jun.2022 Created unitedplanetpeace.com proto site

 On the screen shot below, images are added, images are dynamically re sized with the PIL
 library;

  ![screen shot of image processing](content/siteicons/next_step.png)

 On the screen shot below, projects are added in a separate sub directory;
 The project is isolated, errors in the project do not influence the site;
 only the page with error, and only an error message shows.

  ![screen shot of project and tiles processing](content/siteicons/tiles.png)

  Variable subst regex: "{ .*? }"  (example: { header } )
  Command parameter subst regex: "\[ .*? \]"  (example: [ value_one ] )

  See index.html for examples.

| Directories          | Usage                    |
|  --------------------|--------------------------|
|  /content/proj*      |  applications / projects |
|  /content/siteicons/ |  icons                   |
|  /content/media/     |  image content           |
|  /content/common/    |  python scripts (wsgi interface) |
|  /content/static/    |  static (non changing) content |

### Flow of presenting the pages:

    url lookup in main ->
        if entry present
            if html file exists:
                expand macro -> present page
            else
                call function in url table
                function fills in everything -> present
        else
            if static file ->
                present it
            else
                if 404 file
                    present it
                else
                    404 message

 To create a new project:

    Add a directory to the web server's "content" directory
        that starts with 'proj' (like proj-hello or proj-sales)
    fill in the directory with content
        o Initial .py file to configure the project (any name)
        o Content that responds to the callbacks, or presented as is

    See proj-index for an example home page. Also proj* for more
    detailed examples. Please note how simple a calendar
    implementation becomes.


### History:

    Fri 16.Apr.2021 Skeleton project
    Sun 18.Apr.2021 Apache tests OK
    Mon 19.Apr.2021 Turned icons/ to siteicons/ (for apache not to redirect)
    Thu 22.Apr.2021 Projects in separate dir, reverse isolation
    Mon 27.Sep.2021 Moved user contents to the subdir 'content' (more isolation)
    Tue 28.Sep.2021 Cleanup, first useful site
    Sat 26.Mar.2022 World peace pages
    Tue 28.Jun.2022 united planet peace

## Licence

 Open source.

 PG