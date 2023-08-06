# pyblosxommtimecache

pyblosxommtimecache is a [PyBlosxom](https://pyblosxom.github.io/) filestat
plugin that caches your entries mtimes in a `.mtimes.yaml` file in your
datadir.

The first time it sees each new blog entry, pyblosxommtimecache will add the
entry's mtime to the `.mtimes.yaml` file. It then makes PyBlosxom use these
cached mtimes as the mtimes of your blog entries, instead of using the mtimes
of the files themselves.

This means that if you edit an entry its mtime won't change and it won't jump
to the top of your blog. It also means that PyBlosxom isn't doing costly
`os.stat()` calls on every entry file every time it renders a page.

pyblosxommtimecache will automatically create the `.mtimes.yaml` file for you
the first time it runs.

The `.mtimes.yaml` file is a simple [YAML](http://yaml.org/)-formatted text
file. If you want to change the mtime of an entry you can just edit this file
by hand. If an entry is deleted from the file, or if the entire file is
deleted, it'll just be regenerated using the current mtimes of your entry
files.


## Installation

Install the pyblosxommtimecache package from pip:

    pip install pyblosxommtimecache

Then add it to the `load_plugins` setting in your `config.py`:

    py["load_plugins"] = [
        'pyblosxommtimecache.mtimecache',
    ]
