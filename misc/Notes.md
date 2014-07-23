
## Notes 

Each notebook, and the various nbconvert output files, should all contain links
to the other files in the 'set'.

Should also contain links to a generic info notebook that has any important
details that one wouldn't want to include in every single file.

Want an automatically generated TOC.

Need to have smart and appropriate facility for sets of files; work instalments;
updates; etc.

Perhaps some degree of automatic generation may be useful there.

(see other notes in notes file in my neurodebian thesis folder...)



A key design decision is going to be: how to have / filter comments
 - probably best to have a 'my personal' version of docs that include comments I
do or do not want to be shared with people
 - ...and then nbconvert - filter them out. With notebook cherry pick etc.
 - ...then THAT becomes the 'final' notebook that is seen and produces the
files.

Some people have done stuff like this based on contents of cells. Others have
done it based on cell metadata and tags.
which of those works best?


Need to figure out how best to deal with version control here.
Could to it intelligently with git.
Or probably better to just have separate files / folders for everything that is
handed over
...possible issue could be if there are lots of embedded images these could get
big
...probably not worth worrying about that


Have a 'classes' or 'functions' notebook / .py file that defines a load of
useful things
you would want to have relative file paths?


Make good use of git annex!


Thought: have a 'dependencies' section; e.g. 'uses data files x, x, x'; so that
you can know what the requirements are for running
...could perhaps generate that automatically from the master with some kind of
custom nbconvert stuff?
(BUT really don't want to go overkill here; there are sophisticated templating
systems; you don't want to emulate them here)


simple thing: use american style dates system at the start of filenames?
(either way: have some kind of system for naming things that is clear and that
will sort well in a folder)


Note: probably a good idea to get into the habit of writing reports that are
almost in paper-style format
...so can make use of nbconvert latex stuff there if needed
...so have your own nbconvert template, etc.

...maybe have a bibliographic nearby

...there my be other useful latex things?



Something to sort out: 'outsourcing' analysis things;
i.e. have some notebook code that calls some analysis thing
(e.g. R stuff)
...where you don't want to keep the terminal outputs in the notebook but you do
want to
keep them somewhere nearby
(for these reports could actually keep them in the notebook...)
but I'm thinking a useful alternative would be something like output to a text
file
(you could then, e.g., load in or append or LINK TO (that sounds like best idea)
the text file to see the 'raw' analysis / terminal outputs


related thing is nipype
...and nipype will produce various useful 'reproducibility' things. Might want
to think about how / whether to relate to those...
(be aware nipype outputs are really not transparent unless you make them that
way...)

...and I guess also sumatra or lancet, if you are doing sim things

this is gettign towards sophisticated stuff.
In general need to have a 'in this case I did something complicated and it can
be found here' type clause for such things


Important note :whilst doing this, can give some example 'just matlab'
notebooks, to entice matlab people to using ipynbs for documentation


might want to have alternative css options for small /wide screens (?)



Different kinds of notebook templates that might be of interest:
 - Tutorial
 - Non-data analysis talk (e.g. at conference?)
 - Something simple for nbviewer / gist
 - Literature review???


Useful information to have at top = approximately how long it takes to run
