Module wsgi_main
================
The simplest web server. This directory is at the root
of the web server, and sub directories may assume the following functions:

    data            for database related
    content         where the files live
        siteicons       icons for this site
        media           images, media
        static          files that may be presented as is
        proj*           python and html / css files that make up the site

  To create a <b>new project</b>, add a new directory that starts with "proj"
 (like "proj-000") and populate the files. At least one python file is needed.

    To create a <b>new page</b>, add a new python file, and call the
URL registration function(s) within. The server redirects the url
to the function you specify.

  add_one_url("/", got_index, "index.html")

 To create a new 'macro' use the add macro function with the macro name
and the name of the function that is executed by the macro. The macro
will be replaced by the return value of the function. The macro
is created by surrounding braces with a space. Like: { mymacro }
The macro regex is '{ .*? }' [the '?' is for non greedy wild card)

 add_one_func("mymacro", my_img_func)

 Builtin macros:

 { image nnn }          --  Put an image tag nnn in the output
 { image nnn www }      --  Put an image tag in the output, resize width to requested
 { image nnn www hhh }  --  Put an image tag in the output, resize to width / height

The first two forms of the { image } function will preserve the image's aspect ratio.

Functions
---------

    
`application(environ, respond)`
:   WSGI main entry point. The web server (like apache) will call this.

    
`tracex(xstr)`
:   Trace current fault.
    This was crafted, so the apache run time can access it without any includes.

    
`xhelp()`
:   

    
`xversion()`
:   

Classes
-------

`Myconf()`
:   Simplified config for propagating command line to runtime

`comline()`
:   Command line action defines

    ### Class variables

    `CLEAR_CONFIG`
    :

    `SHOW_CONFIG`
    :

    `SHOW_TIMING`
    :

    `USE_STDOUT`
    :

`xWebServer(environ, respond)`
:   This class has all the info we would need for page generation. Add urls and functions
    to complete the reply. The return value of the process_request function is the
    output to the client.
    
    Decorate the class instance with data from the environment

    ### Methods

    `parse_instance(self, environ, respond)`
    :

    `process_request(self, request, respond)`
    :   This executes the request, after the main initializer
        parsed everything