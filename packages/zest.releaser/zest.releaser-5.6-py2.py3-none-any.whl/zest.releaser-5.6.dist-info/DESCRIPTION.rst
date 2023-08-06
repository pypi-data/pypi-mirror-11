Package releasing made easy: zest.releaser overview and installation
====================================================================

zest.releaser is collection of command-line programs to help you automate the
task of releasing a Python project.

It does away with all the boring bits. This is what zest.releaser automates
for you:

* It updates the version number. The version number can either be in
  ``setup.py`` or ``version.txt`` (or in a ``__versions__`` attribute in a
  Python file). For example, it switches you from ``0.3.dev0`` (current
  development version) to ``0.3`` (release) to ``0.4.dev0`` (new development
  version).

* It updates the history/changes file. It logs the release date on release and
  adds a new heading for the upcoming changes (new development version).

* It tags the release. It creates a tag in your version control system named
  after the released version number.

* It optionally uploads a source release to PyPI. It will only do this if the
  package is already registered there (else it will ask, defaulting to 'no');
  zest releaser is careful not to publish your private projects!


Most important URLs
-------------------

First the three most important links:

- The full documentation is at `zestreleaser.readthedocs.org
  <http://zestreleaser.readthedocs.org>`_.

- We're `on PyPI <http://pypi.python.org/pypi/zest.releaser>`_, so we're only
  an ``pip install zest.releaser`` away from installation on your computer.

- The code is at `github.com/zestsoftware/zest.releaser
  <https://github.com/zestsoftware/zest.releaser>`_.

And... we're automatically being tested by Travis and Landscape:

.. image:: https://secure.travis-ci.org/zestsoftware/zest.releaser.png?branch=master
   :target: https://travis-ci.org/#!/zestsoftware/zest.releaser

.. image:: https://landscape.io/github/zestsoftware/zest.releaser/master/landscape.svg?style=flat
   :target: https://landscape.io/github/zestsoftware/zest.releaser/master
   :alt: Code Health


Compatibility / Dependencies
----------------------------

``zest.releaser`` works on Python 2.7.  Python 2.6 is not officially
supported anymore since version 4.0: it may still work, but we are no
longer testing against it.  Python 3.3+ is supported.

To be sure: the packages that you release with ``zest.releaser`` may
very well work on other Python versions: that totally depends on your
package.

We depend on:

- ``setuptools`` for the entrypoint hooks that we offer.

- ``colorama`` for colorized output (some errors printed in red).

- ``six`` for python2/python3 compatibility.

Since version 4.0 there is a ``recommended`` extra that you can get by
installing ``zest.releaser[recommended]`` instead of ``zest.releaser``.  It
contains a few trusted add-ons that we feel are useful for the great majority
of ``zest.releaser`` users:

- wheel_ for creating a Python wheel that we upload to PyPI next to
  the standard source distribution.  Wheels are the new Python package
  format.  Create or edit ``setup.cfg`` in your project (or globally
  in your ``~/.pypirc``) and create a section ``[zest.releaser]`` with
  ``create-wheel = yes`` to create a wheel to upload to PyPI.  See
  http://pythonwheels.com for deciding whether this is a good idea for
  your package.  Briefly, if it is a pure Python 2 *or* pure Python 3
  package: just do it.

- `check-manifest`_ checks your ``MANIFEST.in`` file for completeness,
  or tells you that you need such a file.  It basically checks if all
  version controlled files are ending up the the distribution that we
  will upload.  This may avoid 'brown bag' releases that are missing
  files.

- pyroma_ checks if the package follows best practices of Python
  packaging.  Mostly it performs checks on the ``setup.py`` file, like
  checking for Python version classifiers.

- chardet_, the universal character encoding detector. To do the right thing
  in case your readme or changelog is in a non-utf-8 character set.

- readme_ to check your long description in the same way as pypi does. No more
  unformatted restructured text on your pypi page just because there was a
  small error somewhere. Handy.

- twine_ for secure uploading via https to pypi. Plain setuptools doesn't
  support this.

.. _wheel: https://pypi.python.org/pypi/wheel
.. _`check-manifest`: https://pypi.python.org/pypi/check-manifest
.. _pyroma: https://pypi.python.org/pypi/pyroma
.. _chardet: https://pypi.python.org/pypi/chardet
.. _readme: https://pypi.python.org/pypi/readme
.. _twine: https://pypi.python.org/pypi/twine


Installation
------------

Just a simple ``pip install zest.releaser`` or ``easy_install zest.releaser`` is
enough. If you want the recommended extra utilities, do a ``pip install
zest.releaser[recommended]``.

Alternatively, buildout users can install zest.releaser as part of a specific
project's buildout, by having a buildout configuration such as::

    [buildout]
    parts =
        scripts

    [scripts]
    recipe = zc.recipe.egg
    eggs = zest.releaser[recommended]


Version control systems: svn, hg, git, bzr
------------------------------------------

Of course you must have a version control system installed.  zest.releaser
currently supports:

- Subversion (svn).

- Mercurial (hg).

- Git (git).

- Git-svn.

- Bazaar (bzr).

Others could be added if there are volunteers! Git and mercurial support
have been contributed years ago when we were working with bzr and subversion,
for instance.


Available commands
------------------

Zest.releaser gives you four commands to help in releasing python
packages.  They must be run in a version controlled checkout.  The commands
are:

- **prerelease**: asks you for a version number (defaults to the current
  version minus a 'dev' or so), updates the setup.py or version.txt and the
  CHANGES/HISTORY/CHANGELOG file (with either .rst/.txt/.markdown or no
  extension) with this new version number and offers to commit those changes
  to subversion (or bzr or hg or git)

- **release**: copies the the trunk or branch of the current checkout and
  creates a version control tag of it.  Makes a checkout of the tag in a
  temporary directory.  Offers to register and upload a source dist
  of this package to PyPI (Python Package Index).  Note: if the package has
  not been registered yet, it will not do that for you.  You must register the
  package manually (``python setup.py register``) so this remains a conscious
  decision.  The main reason is that you want to avoid having to say: "Oops, I
  uploaded our client code to the internet; and this is the initial version
  with the plaintext root passwords."

- **postrelease**: asks you for a version number (gives a sane default), adds
  a development marker to it, updates the setup.py or version.txt and the
  CHANGES/HISTORY/CHANGELOG file with this and offers to commit those changes
  to version control. Note that with git and hg, you'd also be asked to push
  your changes (since 3.27). Otherwise the release and tag only live in your
  local hg/git repository and not on the server.

- **fullrelease**: all of the above in order.

There are two additional tools:

- **longtest**: small tool that renders a setup.py's long description
  and opens it in a web browser. This assumes an installed docutils
  (as it needs ``rst2html.py``).

- **lasttagdiff**: small tool that shows the diff of the currently committed
  trunk with the last released tag.  Handy for checking whether all the
  changes are adequately described in the changes file.


Credits
=======

* `Reinout van Rees <http://reinout.vanrees.org>`_ (Nelen & Schuurmans) is the
  originator and main author.

* `Maurits van Rees <http://maurits.vanrees.org>`_ (Zest Software) added
  a heapload of improvements.

* `Kevin Teague <http://bud.ca>`_ (Canada's Michael Smith Genome Sciences
  Center) added support for multiple version control systems, most notable
  Mercurial.

* `Wouter vanden Hove <http://ugent.be>`_ (University of Gent) added
  support for uploading to multiple servers, using collective.dist.

* `Godefroid Chapelle <http://bubblenet.be>`_ (BubbleNet) added /tag besides
  /tags for subversion.

* `Richard Mitchell <https://github.com/mitchellrj>`_
  (`Isotoma <https://www.isotoma.com/>`_) added Python 3 support.


Changelog for zest.releaser
===========================

5.6 (2015-09-23)
----------------

- Add support for PyPy.
  [jamadden]


5.5 (2015-09-05)
----------------

- The ``bin/longtest`` command adds the correct utf-8 character encoding hint
  to the resulting html so that non-ascii long descriptions are properly
  rendered in all browsers.
  [reinout]


5.4 (2015-08-28)
----------------

- Requiring at least version 0.6 of the (optional, btw) readme package. The
  API of readme changed slightly. Only needed when you want to check your
  package's long description with ``bin/longtest``.
  [reinout]


5.3 (2015-08-21)
----------------

- Fixed typo in svn command to show the changelog since the last tag.
  [awello]


5.2 (2015-07-27)
----------------

- When we find no version control in the current directory, look a few
  directories up.  When looking for version and history files, we look
  in the current directory and its sub directories, and not in the
  repository root.  After making a tag checkout, we change directory
  to the same relative path that we were in before.  You can use this
  when you want to release a Python package that is in a sub directory
  of the repository.  When we detect this, we first offer to change to
  the root directory of the repository.
  [maurits]

- Write file with the same encoding that we used for reading them.
  Issue #109.
  [maurits]


5.1 (2015-06-11)
----------------

- Fix writing history/changelog file with non-ascii.  Issue #109.
  [maurits]

- Release zest.releaser as universal wheel, so one wheel for Python 2
  and 3.  As usual, we release it also as a source distribution.
  [maurits]

- Regard "Skipping installation of __init__.py (namespace package)" as
  warning, printing it in magenta.  This can happen when creating a
  wheel.  Issue #108.
  [maurits]


5.0 (2015-06-05)
----------------

- Python 3 support.
  [mitchellrj]

- Use the same `readme` library that PyPI uses to parse long
  descriptions when we test and render them.
  [mitchellrj]


4.0 (2015-05-21)
----------------

- Try not to treat warnings as errors.
  [maurits]

- Allow retrying some commands when there is an error.  Currently only
  for commands that talk to PyPI or another package index.  We ask the
  user if she wants to retry: Yes, no, quit.
  [maurits]

- Added support for twine_.  If the ``twine`` command is available, it
  is used for uploading to PyPI.  It is installed automatically if you
  use the ``zest.releaser[recommended]`` extra.  Note that if the
  ``twine`` command is not available, you may need to change your
  system ``PATH`` or need to install ``twine`` explicitly.  This seems
  more needed when using ``zc.buildout`` than when using ``pip``.
  Added ``releaser.before_upload`` entry point.  Issue #59.
  [maurits]

- Added ``check-manifest`` and ``pyroma`` to the ``recommended``
  extra.  Issue #49.
  [maurits]

- Python 2.6 not officially supported anymore.  It may still work, but
  we are no longer testing against it.
  [maurits]

- Do not accept ``y`` or ``n`` as answer for a new version.
  [maurits]

- Use ``colorama`` to output errors in red.
  Issue #86
  [maurits]

- Show errors when uploading to PyPI.  They were unintentionally
  swallowed before, so you did not notice when an upload failed.
  Issue #84.
  [maurits]

- Warn when between the last postrelease and a new prerelease no
  changelog entry has been added.  '- Nothing changed yet' would still
  be in there.
  Issue #26.
  [maurits]

- Remove code for support of collective.sdist.  That package was a backport
  from distutils for Python 2.5 and earlier, which we do not support.
  [maurits]

- Add optional support for uploading Python wheels.  Use the new
  ``zest.releaser[recommended]`` extra, or run ``pip install wheel``
  yourself next to ``zest.releaser``.  Create or edit ``setup.cfg`` in
  your project (or globally in your ``~/.pypirc``) and create a section
  ``[zest.releaser]`` with ``create-wheel = yes`` to create a wheel to
  upload to PyPI.  See http://pythonwheels.com for deciding whether
  this is a good idea for your package.  Briefly, if it is a pure
  Python 2 *or* pure Python 3 package: just do it.
  Issue #55
  [maurits]

- Optionally add extra text to commit messages.  This can be used to
  avoid running Travis Continuous Integration builds.  See
  http://docs.travis-ci.com/user/how-to-skip-a-build/.  To activate
  this, add ``extra-message = [ci skip]`` to a ``[zest.releaser]``
  section in the ``setup.cfg`` of your package, or your global
  ``~/.pypirc``.  Or add your favorite geeky quotes there.
  [maurits]

- Fix a random test failure on Travis CI, by resetting ``AUTO_RESPONSE``.
  [maurits]

- Added clarification to logging: making an sdist/wheel now says that it is
  being created in a temp folder. Fixes #61.
  [reinout]


3.56 (2015-03-18)
-----------------

- No need anymore to force .zip for sdist.
  Issue #76
  [reinout]

- Still read ``setup.cfg`` even if ``~/.pypirc`` is wrong or missing.
  Issue #74
  [tomviner]


3.55 (2015-02-03)
-----------------

- Experimental work to ignore setuptools' stderr output. This might help with
  some of the version warnings, which can break zest.releaser's output
  parsing. [reinout]

- Fix for #72. Grabbing the version from the ``setup.py`` on windows can fail
  with an "Invalid Signature" error because setuptools cannot find the
  crypto dll. Fixed by making sure setuptools gets the full ``os.environ``
  including the ``SYSTEMROOT`` variable. [codewarrior0]


3.54 (2014-12-29)
-----------------

- Blacklisting ``debian/changelog`` when searching for changelog-like
  filenames as it gets picked in favour of ``docs/changelog.rst``. The
  debian one is by definition unreadable for us.


3.53.2 (2014-11-21)
-------------------

- Additional fix to 3.53: ``version.rst`` (and .md) also needed to be looked
  up in a second spot.


3.53 (2014-11-10)
-----------------

- Also allowing .md extension in addition to .rst/.txt/.markdown for
  ``CHANGES.txt``.
  [reinout]

- Similarly, ``version.txt`` (if you use that for non-setup.py-projects) can
  now be ``version.rst`` or .md/.markdown, too.
  [reinout]


3.52 (2014-07-17)
-----------------

- Fixed "longtest" command when run with a python without setuptools
  installed. Similar fix to the one in 3.51.
  See https://github.com/zestsoftware/zest.releaser/issues/57
  [reinout]


3.51 (2014-07-17)
-----------------

- When calling ``python setup.py`` use the same PYTHONPATH environment
  as the script has.
  https://github.com/zestsoftware/zest.releaser/issues/24
  [maurits]


3.50 (2014-01-16)
-----------------

- Changed command "hg manifest" to "hg locate" to list files in Mercurial.
  The former prints out file permissions along with the file name, causing a bug.
  [rafaelbco]


3.49 (2013-12-06)
-----------------

- Support git-svn checkouts with the default "origin/" prefix.
  [kuno]


3.48 (2013-11-26)
-----------------

- When using git, checkout submodules.
  [dnozay]


3.47 (2013-09-25)
-----------------

- Always create an egg (``sdist``), even when there is no proper pypi
  configuration file.  This helps plugins that use our entry points.
  Fixes https://github.com/zestsoftware/zest.releaser/issues/45
  [maurits]


3.46 (2013-06-28)
-----------------

- Support actually updating ``VERSION`` as well.
  Issue #43.


3.45 (2013-04-17)
-----------------

- Supporting ``VERSION`` (without extension) in addition to the
  old-zope-products-``VERSION.txt`` files.


3.44 (2013-03-21)
-----------------

- Added optional ``python-file-with-version`` setting for the
  ``[zest.releaser]`` section in ``setup.cfg``. If set, zest.releaser extracts
  the version from that file's ``__version__`` attribute. (See `PEP 396
  <http://www.python.org/dev/peps/pep-0396/>`_).

- File writes now use the platform's default line endings instead of always
  writing ``\n`` unix style line endings. (Technically, we write using ``w``
  instead of ``wb`` mode).

- Added link to other documentation sources in the sphinx docs.

- Noting in our pypi classifiers that we support python 2.6+, not python
  2.4/2.5. Slowly things will creep into zest.releaser's code that break
  compatibility with those old versions. And we want to get it to work on
  python 3 and that's easier with just 2.6/2.7 support.


3.43 (2013-02-04)
-----------------

- Added ``--no-input`` commandline option for running automatically without
  asking for input. Useful when started from some build tool. See the
  documentation at the end of
  http://zestreleaser.readthedocs.org/en/latest/uploading.html .
  [reinout, based upon a patch by j-san]


3.42 (2013-01-07)
-----------------

- When finding multiple version, changes or history files, pick the
  one with the shortest path.
  [maurits]

- Support project-specific hooks listed in setup.cfg.
  [iguananaut]


3.41 (2012-11-02)
-----------------

- Getting the version from setup.py can give a traceback if the
  setup.py has an error.  During prerelease this would result in a
  proposed version of 'Traceback'.  Now we print the traceback and
  quit.
  [maurits]


3.40 (2012-10-13)
-----------------

- Support svn (1.7+) checkouts that are not directly in the root. Only applies
  when someone checks out a whole tree and wants to release one of the items
  in a subdirectory. Fixes #27.


3.39 (2012-09-26)
-----------------

- Only search for files in version control.  This is when finding a
  history file or version.txt file.  We should not edit files that
  are not in our package.  Fixes issue #22.
  [maurits]


3.38 (2012-09-25)
-----------------

- Fixed svn tag extraction on windows: a ``\r`` could end up at the
  end of every tag name. Thanks Wouter Vanden Hove for reporting it!

- Small fixes to the developers documentation and to the automatic
  `travis CI <http://travis-ci.org/#!/zestsoftware/zest.releaser/>`_
  tests configuration.


3.37 (2012-07-14)
-----------------

- Documentation update! Started sphinx documentation at
  `zestreleaser.readthedocs.org <http://zestreleaser.readthedocs.org>`_.
  Removed documentation from the README and put it into sphinx.

- Actually ask if the user wants to continue with the release when
  there is no MANIFEST.in.  We asked for a yes/no answer, but the
  question was missing.
  [maurits]


3.36 (2012-06-26)
-----------------

- Improved changes/history file detection and fixed the documentation at this
  point. We now recognize CHANGES, HISTORY and CHANGELOG with .rst, .txt,
  .markdown and with no extension.

- Set up `travis CI <http://travis-ci.org/#!/zestsoftware/zest.releaser/>`_
  integration. Our tests pass on python 2.5, 2.6 and 2.7.


3.35 (2012-06-21)
-----------------

- When checking for recommended files, ask if the user wants to
  continue when we suspect the created PyPI release may be broken.
  See issue #10.
  [maurits]

- Preserve existing EOL in setup.py and history file (See
  http://docs.python.org/tutorial/inputoutput.html#reading-and-writing-files)
  [tom_gross]


3.34 (2012-03-20)
-----------------

- In the warning about a missing MANIFEST.in file, also suggest to
  install setuptools_subversion/git, etc.
  Fixes issue #4.
  [maurits]


3.33 (2012-03-20)
-----------------

- Fix python 2.4 issues with tarfile by always creating a zip file.
  Formerly we would only do this when using python2.4 for doing the
  release, but a tarball sdist created by python2.6 could still break
  when the end user is using python 2.4.
  [kiorky]


3.32 (2012-03-09)
-----------------

- In prerelease recommend the user to add a MANIFEST.in file.
  See http://docs.python.org/distutils/sourcedist.html for
  more info.
  [maurits]


3.31 (2012-02-23)
-----------------

- Fixed test for unadvised egg_info commands on tag, which could
  result in a ConfigParser error.
  [maurits]


3.30 (2011-12-27)
-----------------

- Added some more PyPI classifiers.  Tested with Python 2.4, 2,4, 2.6,
  and 2.7.
  [maurits]

- Moved changes of 3.15 and older to docs/HISTORY.txt.
  [maurits]

- Added GPL license text in the package.
  [maurits]

- Updated README.txt.  Added MANIFEST.in.
  [maurits]


3.29 (2011-12-27)
-----------------

- In postrelease create a version number like 1.0.dev0.
  See http://www.python.org/dev/peps/pep-0386
  [maurits]

- Offer to cleanup setup.cfg on the tag when releasing.  You do not
  want tag_build or tag_svn_revision options in a release usually.
  [maurits]

- For convenience also print the tag checkout location when only doing
  a release (instead of a fullrelease).
  [maurits]


3.28 (2011-11-18)
-----------------

- Git: in pre/postrelease only check for uncommitted changes in files
  that are already tracked.
  [maurits]


3.27 (2011-11-12)
-----------------

- Postrelease now offers (=asks) to push your changes to the server if you're
  using hg or git.

- Support for some legacy projects, often converted from CVS, have multiple
  subprojects under a single trunk. The trunk part from the top level project
  isn't erroneously stripped out anymore. Thanks to Marc Sibson for the fix.


3.26 (2011-11-01)
-----------------

- Added sanity check before doing a prerelease so you are warned when
  you are about to commit on a tag instead of a branch (or trunk or
  master).
  [maurits]


3.25 (2011-10-28)
-----------------

- Removed special handling of subversion lower than 1.7 when searching
  for the history/changes file.  In corner cases it may be that we
  find a wrong HISTORY.txt or CHANGES.txt file when you have it buried
  deep in your directory structure.  Please move it to the root then,
  which is the proper place for it.
  [maurits]

- Fixed finding a history/changes file that is in a sub directory when
  using subversion 1.7 or higher or bazaar.
  [maurits]


3.24 (2011-10-19)
-----------------

- Note: you may need to install setuptools_subversion when you use
  subversion 1.7.  If you suddenly start missing files in the sdists
  you upload to PyPI you definitely need it.  Alternatively: set up a
  proper MANIFEST.in as that method works with any version control
  system.
  [maurits]

- Made compatible with subversion 1.7 (the only relevant change is in
  the code that checks if a tags or tag directory already exists).
  Earlier versions of subversion are of course still supported.
  [maurits]

- Code repository moved to github:
  https://github.com/zestsoftware/zest.releaser
  [maurits]


3.23 (2011-09-28)
-----------------

- Fixed opening the html long description in ``longtest`` on Mac OS X
  Lion or python2.7 by using a ``file://`` url.
  Fixes https://bugs.launchpad.net/zest.releaser/+bug/858011
  [maurits]

.. # Note: for older changes see ``doc/sources/changelog.rst``.

.. _twine: https://pypi.python.org/pypi/twine


