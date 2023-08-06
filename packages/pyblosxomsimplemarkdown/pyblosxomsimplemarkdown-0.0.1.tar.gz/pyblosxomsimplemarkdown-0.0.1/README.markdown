# pyblosxomsimplemarkdown

pyblosxomsimplemarkdown is a [PyBlosxom](https://pyblosxom.github.io/)
entryparser plugin that lets you write your entries in
[Markdown](http://daringfireball.net/projects/markdown/). Specifically,
[Python Markdown](https://pythonhosted.org/Markdown/) is used.

pyblosxomsimplemarkdown differs from other PyBlosxom Markdown plugins in that
it treats the entire contents of the entry file as just the entry body.
Normally PyBlosxom treats the first line of an entry as its title, any
following lines that start with `#` as metadata, and the rest of the file as
the entry's body:

    This is the title
    #key value
    #foo bar

    The rest of the file is the Markdown-formatted entry body...

pyblosxomsimplemarkdown just treats the entire contents of the file as a
Markdown-formatted body. The entry dict won't have any value in its 'title'
field. If you want to write a traditional blog post with a title and body, just
insert the title yourself:

    # This is the title

    This is the contents...

If you want to create a differently-formatted post that doesn't start with a
title, such as a link, a quote or an image with a caption, just go ahead and
write that in Markdown.

pyblosxom-markdown currently parses entries with the filename extensions '.md'
and '.markdown' (these are currently hardcoded and not configurable).

pyblosxom-markdown currently uses Python Markdown's
[Extra](https://pythonhosted.org/Markdown/extensions/extra.html) and
[SmartyPants](https://pythonhosted.org/Markdown/extensions/smarty.html) plugins
(hardcoded, not configurable).

pyblosxom-markdown renders entries as HTML5 (hardcoded, not configurable).


## Installation

Install the pyblosxomsimplemarkdown package from pip:

    pip install pyblosxomsimplemarkdown

Then add it to the `load_plugins` setting in your `config.py`:

    py["load_plugins"] = [
        'pyblosxomsimplemarkdown.simplemarkdown',
    ]
