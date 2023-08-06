=====================
docutils_react_docgen
=====================

Overview
========

docutils extension for documenting React modules.
Requires react-docgen

Example
-------

Here is the restructured text to display all of the
React modules in `static/js/lib/my`.  Source links 
to each module are relative to the `src` option::
 
    My JS/React Library
    ===================

    .. contents:: Table of Contents

    .. reactdocgen:: static/js/lib/my
            :src: https://bitbucket.org/.../my/src/tip

Installation
============

From PyPi
::

    $ pip install docutils-react-docgen 

From source
::

    $ hg clone ssh://hg@bitbucket.org/pwexler/docutils_react_docgen
    $ pip install -e docutils_react_docgen/

The installation is successful if you can import docutils_react_docgen.  
The following command must produce no errors::

    $ python -c 'import docutils_react_docgen'


Usage
-----

In your `conf.py` you must import docutils_react_docgen::

    import docutils_react_docgen
    
In your restructured text document(s) include the `reactdocgen` directive,
and the react-docgen command on the same line,
followed by zero or more option lines, 
followed by a blank line::

    .. reactdocgen::  /path/to/your/react/modules/ [react-docgen options]
        :option: value             
        
This will convert the output of::

    react-docgen /path/to/your/react/modules/ [react-docgen options]

into restructured text and insert it in place of the directive.

react-docgen lets you filter which modules to extract meta data from.
See::

    react-docgen --help

for an explanation of the react-docgen command line options.

Each module is displayed with a heading
showing the module name
(which can appear in the table of contents), 
optionally followed by a link to its source code,
followed by its description, 
followed by its properties shown alphabetically in a definition list.  

Options
-------

Each option is shown with its default value.

`exclude`
  default:

  Use this option to filter which modules appear in the output.

  If provided, this regular expression is compiled into a pattern
  using python's re module.
  Then if the pattern is found in a module's description (using re.search), 
  the module is excluded from the output.
  
`include`
  default:

  Use this option to filter which modules appear in the output.

  If provided, this regular expression is compiled into a pattern 
  using python's re module.
  Then a module is included in the output only if 
  the pattern is found in the module's description (using re.search). 
  
`module_description_missing`  
  default: Module doc string is missing!

  The string to display whenever a module's 'description' key value is empty.

`module_prop_description_missing`  
  default: Property doc string is missing!

  The string to display whenever a property's 'description' key value is empty.

`module_underline_character`  
  default: \-

  The underline character for the module heading.

.. _path_index:

`path_index`
  default: 0

  The index to the path argument.  

  This index is the number of arguments which preceed the path argument 
  in the argument string passed to the directive.

  When the `project_base`_ setting is used, 
  the directive uses ``path_index`` to identify the path argument
  from the list of arguments it was called with.
  The default index of 0, 
  means the path argument is the first in the list.

  Change this option if you want to pass additional arguments to react-docgen
  which preceed the path argument.

`show_prop_type`
  default: False

  If True, display the property type name.
     
`src`  
  default: 

  If empty, no link is displayed for each module.

  If not empty, it is the prefix used when linking to the source code.
  The url is the prefix followed by '/' followed by the module filename.

`tab_size`  
  default: 4

  The number of space characters to replace each tab character with.

`use_commonjs_module_name`   
  default: True

  If True, 
  a search for the CommonJS package proceeds 
  recursively starting with the given directory
  and working up the directory tree towards the root.

  If False, 
  or (if True and) no bower.json or package.json can be found,
  the module name will appear as its filename instead of its 
  CommonJS Module name.

  
Changing Default Options
------------------------

The default values of all the options 
may be changed directly.  
For example::

    import docutils_react_docgen
    docutils_react_docgen.DEFAULT_OPTIONS['module_description_missing'] = ''

Settings
--------

`react_docgen`  
  default: react-docgen

  The react-docgen command to run. 
   
  Use this setting to provide a path to the react-docgen executable.  
  The default assumes that react-docgen is in the PATH.

  This setting can contain spaces so it is possible to invoke an alternate 
  implementation of react-docgen with some leading options. 

.. _project_base:

`project_base`
  default: None

  The base address of the project at run-time.

  Use this setting in dynamic build environments, to establish the 
  absolute address of the project.

  Ordinarily, you would cd to the base of your project (where setup.py is) 
  and run::

      python setup.py build_sphinx
  
  However, some build environments are created dynamically.  
  In some cases it is not possible to know in advance 
  either the current directory
  or your project's relation to it.
  In these cases the directive is unable to find your React files to process
  unless you tell it how.
  
  As long as you know where conf.py is in relation to the project's base, 
  you can set ``project_base`` in conf.py by virtue of Python's built-in 
  __file__ attribute and os.path methods.  

  When this setting is not None (note that "" is not None), 
  and the path argument to the directive is a relative address,
  then the directive will construct an absolute path 
  by prepending the project base::

      path = os.path.abspath(os.path.join(
              SETTINGS['project_base'], 
              path_argument))

  .. note::

    You may want to adjust the `path_index`_ option when using this option.

`rst_output`
  default: None (no separate output file)

  The full path of a separate output file 
  to hold only the rst generated by the directive.

  When not None, 
  the output file is created each time the directive is executed.

  When there are rst errors in the JavaScript source
  sphinx reports the offending line numbers.
  Using this option you can locate the errors
  at the given line numbers in the separate output file.

Changing Settings
-----------------

The values of all the settings 
may be changed directly.  
For example to set the path to react-docgen::

    import docutils_react_docgen
    react_docgen = './static/js/node_modules/react-docgen/bin/react-docgen.js'
    docutils_react_docgen.SETTINGS['react_docgen'] = react_docgen

To make the project base absolute, let's suppose conf.py is in doc/
relative to the project's base, 
and the React modules are in static/js/lib/

Then in your conf.py::

    import docutils_react_docgen
    import os
    docutils_react_docgen.SETTINGS['project_base'] = os.path.join(
            '../',
            os.path.dirname(__file__))

And in your .rst file::

    .. react-docgen:: static/js/lib    

Providing a Custom Formatter
----------------------------

Proceed by creating a module,
sub-classing both Formatter and ReactDocgen,
and registering your directive::

    import docutils_react_docgen
    from docutils.parsers import rst
    
    class MyFormatter(docutils_react_docgen.Formatter):
        ... overwrite methods as necessary 
        
    class MyDirective(docutils_react_docgen.ReactDocgen):
        formatter_class = MyFormatter

    rst.directives.register_directive('mydirective', MyDirective)

The formatter_class will be invoked as follows::

    rst = self.formatter_class(options, dirname).run(doc_dict)

options
    A dict of the directive options.

dirname
    The path to search for the CommonJS package.

doc_dict
    A dict of module metadata loaded from the JSON blob 
    returned by react-docgen.  
    The keys are the module file names,
    and the values are dicts of React module metadata.
    
The run() method must return a string 
containing the desired restructured text.

Finally, insure that the module containing your directive is imported 
by conf.py

