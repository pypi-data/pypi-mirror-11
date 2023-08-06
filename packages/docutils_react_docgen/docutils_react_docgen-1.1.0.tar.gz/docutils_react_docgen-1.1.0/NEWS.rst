*************
 Change Log
*************

1.1.0 (2015-09-17)
==================

* Added show_prop_type option.  Default is False for backwards compatibility.

1.0.0 (2015-09-08)
==================

* Added filters.  Use regular expressions to include and/or exclude modules
  from the output.
   
0.4.0 (2015-08-17)
==================

* Added SETTINGS['rst_output'] to facilitate debugging rst errors
  in the Javascript source.  The default is None (no separate output file).

* Fixed indentation error in module property definitions:  handle case of
  ``module_prop_description_missing == ''`` properly.

0.3.0 (2015-06-03)
==================

In some build environments it is not possible to know ahead of time 
either the current directory
or your project's relation to it.  
With this change you can set the project's base address
so that a relative path argument can be made absolute at run-time.

* Added SETTINGS['project_base'].  The default is None.

* SETTINGS['react_docgen'] may now include arguments.

* Added DEFAULT_OPTIONS['path_index'].  Default is 0.

* Added keyword argument to run_react_docgen(): options=DEFAULT_OPTIONS

* Added keyword option to Formatter.__init__() 
  and react_doc_to_rst(): args=''

0.2.0 (2015-05-31)
==================

react_docgen() has always referenced the initial value of REACT_DOCGEN.
With this change you can now set 
which react-docgen command to run 
within conf.py.


* Added SETTINGS

* Use run_react_docgen() instead of react_docgen().

* Deprecate REACT_DOCGEN, use SETTINGS['react_docgen'] instead.
  The next major release will not include REACT_DOCGEN. 

0.1.1 (2015-05-18)
==================

* Fix react_docgen() doc string, add link in README.rst

0.1.0 (2015-04-30)
==================

This release is not backward compatible as some options have been removed.

* Improved display of module. 
* Infer CommonJS module name from bower.json or package.json if available.
* Thanks to Andrey Popp for adding CommonJS support!
* Removed options\:
  missing, 
  module_dict_key_emphasis, 
  module_prop_emphasis
* Added options\:
  module_description_missing, 
  module_prop_description_missing, 
  tab_size, 
  use_commonjs_module_name, 
* Added formatter_class attribute to ReactDocgen to facilitate sub-classing.

0.0.2 (2015-04-27)
==================

* __init__.py: import from .docutils_react_docgen
* Converter and Formatter are subclasses of object.

0.0.1 (2015-04-23)
==================

* initial release
