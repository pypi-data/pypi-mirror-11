network-docopt
==============

NetworkDocopt is a command line argument parser for networking focused
applications. This was heavily inspired by the docopt module at
http://docopt.org/ (no code from docopt was used however). The key
differences are:

-  Support for partial command line options. If your program foo has a
   "foo show summary" option you can also enter "foo sh sum"

-  Support for integration into bash's auto-complete mechanism

Example
=======

-  See network-docopt-example for an example of how to use this module
-  For bash <tab> auto-completion and bash <tab><tab> "show me available
   options" you must create a small bash script in
   /usr/share/bash-completion/completions/ like so:
-  cp completions/network-docopt-example
   /usr/share/bash-completion/completions/

This bash script will call network-docopt-example with 'options' as the
last argument. For instance if you type "network-docopt-example show ip
" the bash script will call "network-docopt-example show ip options"
which will return "route" and "interface". This tells bash what the next
options are.

Contributing
------------

1. Fork it.
2. Create your feature branch (``git checkout -b my-new-feature``).
3. Commit your changes (``git commit -am 'Add some feature'``).
4. Push to the branch (``git push origin my-new-feature``).
5. Create new Pull Request.

License and Authors
-------------------

Original Author:: Daniel Walton

Copyright:: 2015 Cumulus Networks Inc.

.. figure:: http://cumulusnetworks.com/static/cumulus/img/logo_2014.png
   :alt: Cumulus icon

   Cumulus icon

Cumulus Linux
~~~~~~~~~~~~~

Cumulus Linux is a software distribution that runs on top of industry
standard networking hardware. It enables the latest Linux applications
and automation tools on networking gear while delivering new levels of
innovation and ﬂexibility to the data center.

For further details please see:
`cumulusnetworks.com <http://www.cumulusnetworks.com>`__

This project is licensed under MIT

