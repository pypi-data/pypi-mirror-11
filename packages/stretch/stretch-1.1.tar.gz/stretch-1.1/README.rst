=======
stretch
=======
stretch is a command line tool that uses `PBKDF2`_ from Python's `passlib`_ to
derive a key, given a secret and a salt.

Installation
------------
You can, of course, clone the repo or download the ``stretch`` script and
call it from its directory, but I'd rather have it "installed" so it can be
called from anywhere. The easiest way to install it::

    [sudo] pip install stretch

Instead, you could just copy the script to a convenient location::

    [sudo] curl https://raw.githubusercontent.com/felipedau/stretch/master/stretch -o /usr/local/bin/stretch

Finally, stretch the secret ``foo`` with the salt ``bar`` using the defaults
``hmac-sha512`` and ``10000`` rounds::

    $ stretch foo bar
    FUMV4GHTdgpdEbseRSkUNiTd6CYktCUr3XPqy+pp7cPk7R7Ho0L1JJDXMbcYQkA/gkWQ7BoSOtRcMnvnD8qqhg==

+---------------------------------------+-------------------------------------+
| Optional Arguments                    | Description                         |
+=======================================+=====================================+
| ``-h``, ``--help``                    | show this help message and exit     |
+---------------------------------------+-------------------------------------+
| ``-b BEGIN``, ``--begin BEGIN``       | define where to start slicing the   |
|                                       | result (equivalent to               |
|                                       | ``result[b:]``)                     |
+---------------------------------------+-------------------------------------+
| ``-e END``, ``--end END``             | define where to stop slicing the    |
|                                       | result (equivalent to               |
|                                       | ``result[:e]``)                     |
+---------------------------------------+-------------------------------------+
| ``-f {md5,sha1,sha256,sha512}``,      | choose a pseudo-random family.      |
| ``--family {md5,sha1,sha256,sha512}`` |                                     |
+---------------------------------------+-------------------------------------+
| ``-r ROUNDS``,                        | define the number of rounds to use  |
| ``--rounds ROUNDS``                   | on the generation (an integer       |
|                                       | greater than zero). (Default:       |
|                                       | ``10000``)                          |
+---------------------------------------+-------------------------------------+
| ``-c``, ``--copy``                    | copy the output to the clipboard by |
|                                       | piping it to xclip instead of       |
|                                       | printing                            |
+---------------------------------------+-------------------------------------+

.. _`passlib`: https://pythonhosted.org/passlib
.. _`pbkdf2`: https://pythonhosted.org/passlib/lib/passlib.utils.pbkdf2.html
