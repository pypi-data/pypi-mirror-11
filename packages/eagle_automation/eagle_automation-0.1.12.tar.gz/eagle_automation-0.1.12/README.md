Eagle automation
================

Python's Eagle Automation (`PEA`) provides a more Unix-like and scriptable
interface to the CadSoft Eagle electronics design package. It is meant to make
open hardware development a bit more convenient for anyone that is used to the
procedures usually employed by open source software projects (for example using
source control tools and one-step builds).

This repository currently contains the following:

- `pea diff`
   - Commandline diff tool for schematics, board layouts and
   libraries that is compatible with git-difftool.
   For schematics and board layouts, a visual diff is
   displayed. <br />
   For libraries, a textual comparison of library elements is
   shown.

- `pea export`
   - A tool that exposes a unified commandline interface to various
   different ways Eagle offers for exporting artwork. <br />
   It currently supports exporting Eagle files to Gerber, PDF and
   PNG formats, generating Excellon drill files and files needed
   for pick & place machines.

- `pea drill`
   - Generate `.drl` files from `.dri` without any annoying dialogs.

- `pea bom`
   - Generate .json file with the full list of components

- `skel/Makefile` 
   - An example Makefile that demonstrates how fabrication and
   assembly documentation for a project can be generated
   automatically with GNU Make.



Installation
============

Using pypi, do:

    % pip install eagle_automation

Using the sources, run:

    % python setup.py install
    % git config --global --add difftool.eaglediff.cmd 'pea diff $LOCAL $REMOTE'

Note these scripts have only been tested using Eagle ≥5.11.0 (and 7.2)



Usage
=====

You can find a `Makefile` in the `skel/` subdirectory that shows how you can
automatically build your project's documentation using make from `.sch` and
.brd files.

To show differences to the design that have not yet been committed:

    % git difftool -t eaglediff

To show differences between two tagged versions:

    % git difftool -t eaglediff v1.0..v2.0

Note that Eagle windows will blink on and off during the use of these
tools. Try not to touch anything while they are doing that. 

Also, Eagle sometimes behaves weirdly if more than one instance of it is
running: it might occasionally stop in the middle of a script or throw a
random error dialog. Because of the closed nature of this software there is
nothing that can be done about that. If that bothers you, consider
switching to a free EDA tool.


Develop
=======

install buildout `pip install zc.buildout` and run:

    % buildout
    % bin/pea --help

from the sources' root.

Then you can run `python setup.py develop` to install a global instance linked to 
current sources. Or `python setup.py install` to install it the old fashion way.


Configuration
=============

These tools make a distinction between "export layers" (e.g. layer names
used on the `pea export` command line) and "Eagle layers" (layer names as they
appear in the Eagle user interface). One export layer typically corresponds to
one mask and consists of one or more Eagle layers.

For example `topcopper` export layer by default includes `Top`, `Pads` and
`Vias` Eagle layers.

A configuration file provides a mapping between export layers and Eagle layers
and some other tweakable settings. Default configuration is installed by
`setup.py`. It should work for most simple one- or two-layer boards.

Should you want to adjust something, you can place your own configuration file
to one of the following locations. Settings in later locations override earlier
ones:

	/etc/eagle_automation.conf
	$HOME/.config/eagle_automation.conf
	$HOME/.eagle_automation.conf
	./eagle_automation.conf
	./.eagle_automation.conf

You can use the `skel/eagle_automation.conf` file as a template.

You can specify configuration options on the commandline by giving `key=value` just
after the `pea` command:

    pea -c EAGLE=/usr/local/bin/eagle export example.sch bom example-bom.json

And you can as well give configuration files the same way (only restriction: the configuration
file shall not contain the character `=` or it will be interpreted as a key/value setting).

e.g.:

    pea -c ../config/pea.conf export example.sch bom example-bom.json


Known problems
==============

When exporting to PDF using `pea export`, default print settings are used.
To set them, go to File -> Print setup, make changes, then quit Eagle so
that the settings are saved.


Contributors
============

    Copyright (C) 2014  Tomaz Solc <tomaz.solc@tablix.org>
    Copyright (C) 2015  Bernard Pratz <guyzmo+github@m0g.net>

License
=======

    Eagle automation, set of commandline tools for use with CadSoft Eagle
    Copyright (C) 2014  Tomaz Solc <tomaz.solc@tablix.org>

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
