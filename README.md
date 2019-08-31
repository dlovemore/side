Side Project
------------

*SIDE* or *Simple Integrated Development Environment* is a poor man's IDE
inspired by Python's *doctest* module and built on the idea of simple,
modular and orthogonal components.

## Basic idea

**side** is a command line tool.

**side** transforms its input by re-running any embedded python
commands. These commands may be found in docstrings or comments.

By combining with **diff** a way of testing against known good
behaviour can be constructed. This allows us to use a simple log of
commands as a simple test suite.

Invoking **side** from within an editor (with appropriate editor
macros) makes an easy way of running and capturing interactive sessions
and turning them into a test suite.  (The projects **vide** and
**elide** will provide vim and emacs macros that use **side**.)

## Interactive use within editors

Code following a combination of spaces, a single *#* and a python
prompt is also run by **side**.

By using *!* in *vi* or *C-u M-x shell-command-on-region* in *emacs* we can
pipe these commands through **side** to see the results.

    # >>> def reversed(s): return s[::-1]
    # >>> 
    # >>> reversed("Madam I'm Adam")

when piped through **side** becomes:

    # >>> def reversed(s): return s[::-1]
    # ... 
    # >>> reversed("Madam I'm Adam")
    # "madA m'I madaM"

These snippets of interactive use can then become tests.

It's important to import code you need to run.

## Interactions with source control

It is a good practice to check diffs when committing changes. These
highlight any changes that may have happened to expected output. This
also allows test driven design.

Tests can either accompany source code, or become slightly more formal
separate tests.

Keepng expected output when the output changes may be desirable. A
syntax to indicate that may feature in a future version.

## Testing

By running

    ## $ side README.md >README.md.out
    ## $ diff -u README.md README.md.out

or using another tool that does this automatically, we have a way of
testing our docstrings or other tests.

## Docstrings

Indented python code following a python prompt '>>> ' or '... ' is
captured.

        >>> 'This is executed'
        'This is executed'
        >>> 
    Anything without the same indentation is kept.
        >>> print('''But anything with the same indentation is replaced
        ... with the output of the command.''')
        But anything with the same indentation is replaced
        with the output of the command.

The above can be embedded in multiline doc strings. It will be
necessary to import the functions being tested perhaps in a comment
before the docstrings.

## Installation

I'm sorry, but this is still a prototype installation is manual.

Installation steps:

* Download.
* Make **side** executable.
* Add to command line path.

## Troubleshooting

* The python prompt ">>> " ends in a space. Without the space nothing
is run.

* You need to import code you use.

## Simplicity, modularity, orthogonality

The idea being explored here is of small, modular components that can
be combined in powerful ways.

Although *SIDE* does not do the variety of things that *doctest* which
inspired this component does, similar things may be achieved through
judicious use of the right components.

### Advantages of approach

* Powerful tools can be constructed simply by using orthogonal
combinations of components.
* Swiss army knife tools that have a large number of functions or
options can still be built, but they themselves become simpler, by
being bullt out of combinations of simple components.
* Functionality buried within useful tools become exposed and made 
more generally available and useful.

## Related components

* vide - An IDE for vim built on top of side.
* elide - An IDE for emacs built on top of side.
* diff - A UN*X tool for comparing files

## Version information

The current version is version 0.

### Version 0

* Basic functionality
* No installer

### Version future

* May use subprocess or contextlib to capture output.
* Syntax for keeping previous/target output
* Installation
* Better examples
