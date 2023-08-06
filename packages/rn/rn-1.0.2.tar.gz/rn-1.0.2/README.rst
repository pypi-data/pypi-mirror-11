==
rn
==

A multiple renaming program for the console.

I started **rn** as a learning tool for my recently acquired Python 3
knowledge, and I really learned a lot programming it.

As it has become useful to me, I want to share it.

It was programmed using Python 3.4 in a computer running FreeBSD 10.1, and
tested in FreeBSD 10.1 and Windows XP. It should work unchanged in
GNU/Linux and OS X, too, but I have not tested it.

If you own  or have access to a Mac, I would really appreciate it if you
run the test program in it and let me know the results. The same goes for any
GNU/Linux system. See the test section for details.

Installation
============

To install the program:

``$ pip install rn``

Documentation
=============

To install the documentation you will have to download the package and untar it with your favorite program or through the console:

``$ tar -xz -f *packagename.tar.gz*``

Now you will find, in different formats, the manual under the doc folder.

**rn.1** is the manual in man format. If you are using a UNIX like system,
you can copy it to your man directory (as root) and access it anytime with
``man rn``.

As root:

``gzip rn.1``

``cp rn.1.gz /usr/local/man/man1/``

The path to your man pages may be different.

Features
========

- Delete any number of characters from your selection of file names starting at the beginning, at the
  end or in the middle.
- Crop text from the files names: words, letters, from a word to the end, from the beginning to a letter or word...
- Replace letter or words inside the names of the files.
- Change the capitalization or case.
- Add prefixes or suffixes.
- Apply all the above to directory names or file extensions.

Testing
=======

If you have downloaded the package (and not only install it with pip), you
will have a test folder containing two archives.

To run the test, make a copy of the executable rn as rn.py in the test 
directory, change to the test directory and execute the script *test* :

``$ ./test``

If some error raises, please, run the test again directing the output to a 
file and e-mail it to me with any details you may find important.

``$ ./test > test-results-file``

If there were not errors and you are running a system different of FreeBSD or Windows XP, please let me know that the program works in your operating system, too.

Contact
=======

You may contact the author of the program at: <rn-program at mundo-r dot com>

License
=======

The program **rn** is distributed under the GPLv3 license.

Copyright (C) 2015 Jose M. Casarejos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
