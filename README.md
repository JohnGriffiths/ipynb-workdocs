
# ipynb workdocs 

A simple system for reproducible research documentation.

---

## What's this then? 

The aim is to facilitate a document-as-you-go workflow for research and other
walks of life.

Three important features of such a workflow are:


1. **Reproducibility**. Including *speed of*, *transparency of* and *ease of*.
2. **Efficiency**. I don't want to spend additional time going back and
documenting what I've done. I want to do it along the way. And I don't want to
have to make different files for documenting and sharing and presenting stuff in
different contexts. That leads to diffusion of information (across multiple
files) and rapid propagation of multiple files.


This pitch is not original and in fact is becoming increasingly recognized and
en vogue. And as a result the good people at IPython have developed a number of
excellent tools that facilitate these objectives.


With *ipynb workdocs* I am simply applying these tools in the way that best
suits the needs of myself, my colleagues, and anyone else who might find it
useful.


The bread and butter of this is the simple research report, of the 'here you go
boss, this is what I did, and this is what the result was' variety. Could be the
summary of a few hours' work or a few days' work. The key thing is to have as an
end-product

- an ipython notebook, from which are generated
- a pdf
- a static html file ( + web link, e.g. nbviewer)
- a web-based slideshow (e.g. slideviewer or gh-pages)
- possibly also: sphinx web pages, rst, markdown
- if at all possible: something like a powerpoint type file

As far as possible the notebook should be one-click runnable to reproduce any
analysis and figures content. For long analyses or when data access is highly
restricted this may not be practicable all of the time, but this should be the
aim.

Again, these all come pretty easily from IPython tools that are becoming pretty
standard. I'm just providing templates and extra functions so that I one can sit
down and crack these out a rapid pace.

---

## Enough talk. How does it work?

The basis idea is that you have a 'master' notebook containing 'everything',
which is then wittled down for specific use cases.

There are two steps of 'wittling'.

- Remove all rough notes from the master notebook.
- Convert this smartened-up notebook to static html, PDF and slides.

The input to the first stage is the master notebook. The input to the second
stage is the output from the first stage.

What gets snipped is defined by a custom set of cell tags. To do this I am using
modified versions of the tools provided in jonathan frederic's 'notebook cherry
picker' repo.




![png](misc/readme_graph.png)



At present I have four 'modes of consumption' in mind:

- *in-notebook* - for everyday use and 'on the ground' discussion/sharing with
colleagues
- *nbviewer* - effectively a static website. All analysis and figures code is
retained; similar sharing function as above but with a more permanent reference
location
- *pdf* - For summaries and dissemination. Long analysis code is snipped out.
- *slides* - For meetings and talks. Only key summary bullet points and figures
used.

As a general rule, the idea is to try to use the same cells for nbviewer, PDF,
and slides. But the system allows for specific additions or exclusions for each
of these.


The repo provides template notebooks for a few different use cases - one-off
report, rolling documentation ('rolldoc'), quick notes, tutorials, general
notes, academic papers, dissertations, etc.


Each template has an nbconvert section at the end containing the code necesssary
to achieve all this.

---



example...



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
