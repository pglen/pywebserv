# PyFortune

  This project is an accumulation of several fortune projects. The program
is simplified. Just type (exec) 'pyfortune.py' for an informative fortune
display.

    Usage: pyfortune.py [options]

  Program options:

        -v        - Verbose
        -f file   - Show fortune from file
        -d dir    - Show fortune from directory
        -h        - Help
        -o        - Allow offensive material, 1:10 mixin

  The fortunes are displayed randomly, picking a random file from the
fortune directory, picking a random fortune. If the -o option is specified
pyfortune.py mixes in fortunes that are tagged offensive. The mix ratio
is set to one in ten, favoring normal fortunes.

 The fortunes are filtered for length, ant fortune that is between 5 and 100
characters long is presented.

  Please see the 'Selection' file for more description on what is deemed
offensive. Alternatively, you may see the 'offensive' subdirectory to see
if the fortunes exceed your audiences tolerance.

 When installed, the fortune files are in: /usr/share/pyfortune/datfiles/

Quote from parent project:

  The fortunes contained in the fortune database have been collected
haphazardly from a cacophony of sources. It is difficult to do any
meaningful quality control on attributions, or lack thereof, or
exactness of the quote. Since this database is not used for profit,
and the entire works are not published, it falls under fair use, as we
understand it.

Log:

    Fri 03.Mar.2023  added local dir test for running from source dir

    Peter Glen

