Changelog
=========

2.3.0 (2015-09-25)
------------------

Fix
~~~

- Nasty hidden bug that would break python3 (fixes #27) [Valentin Lab]

  Actually this bug was revealed by python3 random hashes (thanks to
  @rschoon for the hint) and could be reproduced on python2.7 with ``-R``
  mode.

  The ``git show`` command actually will behave differently if given a tag
  reference and print random unexpected information before using the
  format string. This would prefix a lot of mess to the first field being
  asked in the format string.

  And this first field is dependent on the internal order of a dict, and
  this order is not important as such, and so nothing was done on this
  part.

  On python2.7, somehow, it would always be the same order that revealed
  to have no consequence (probably one of the rare field not used in
  current changelogs).

  Python3 or Python2.7 -R would shuffle this order and then trigger the
  error whenever this prefix would be appended to actually important
  fields that went into some further processing (as casted to int for
  the timestamp for instance).

2.2.1 (2015-06-09)
------------------

Fix
~~~

- Fix: doc: ``ìnclude_merge`` options was wrongly typed in sample config
  files (reported by @tuukkamustonen, fixed #29). [Valentin Lab]

- Updated doc to reflec that there are no support of windows for now.
  (fixes #28) [Valentin Lab]

  Actually windows will fail on ``subprocess`` call. (see #28)

- Remove commit's meta-information footer from changelog output. (fixes
  #25) [Valentin Lab]

  Some various tools (thinking of Gerrit) might leave some
  meta-information in the footer of your commit message's body that you do
  not want to be repeated in your changelog. So all values in the footer
  are removed (This concerns ``Change-Id``, ``Acked-by``, ``CC``,
  ``Signed-off-by``, ``Bug`` ... and any other value).

2.2.0 (2015-01-27)
------------------

New
~~~

- Provide support for older config file format. [Valentin Lab]

- Added 'octobercms-plugin' mako template. (fixes #16) [Valentin Lab]

- Added ``body_process`` and ``subject_process`` options. (fixes #22)
  [Valentin Lab]

  These options superseeds ``replace_regexps`` and ``body_split_regexp``
  as they provide a full control over text transformation of the subject
  or the body of the commit before they get included in the changelog.

- Added ``include_merge`` option to filter out merge commit. [Casey
  Duquette]

Changes
~~~~~~~

- Produce a more linear commit history (fixes #14) [Casey Duquette]

  Instead of retrieving the git log ordered by date, retrieve the log as
  a difference between tags to produce a more accurate view of changes
  between releases.

  For instance, imagine this git graph::

    * 6c0fd62 (HEAD, tag: sprint-6, origin/smoke, smoke, develop)
    *   5292a28 Merge back to develop
    |\
    | * 6612fce (tag: sprint-5.1, origin/master, origin/HEAD, master) super important hotfix
    * | 7d6286f more development work
    * | 8c1e3d6 continued development work
    * | fa3d4bd development work
    |/
    * ec1a19c (tag: sprint-5)

  Previously, commits ``fa3d4bd``, ``8c1e3d6``, ``7d6286f`` that
  occurred on the develop branch before the hotfix that led to tagging
  ``sprint-5.1``, were captured in the changelog under release
  ``sprint-5.1`` because of the order of the commits. But it is obvious
  that these commits were not included in a release until
  ``sprint-6``. The new method of calculating the changelog will capture
  this and reflect it properly, assigning those changes to ``sprint-6``.

Fix
~~~

- Last commit was omitted (fixes #23). [Valentin Lab]

- Bogus messages when template didn't exist. [Valentin Lab]

  Refactored out the common code and corrected the bad error message.

- Removed hypothetical memory exhaust while parsing ``git log``.
  [Valentin Lab]

  Parse stdout as it's produced by git log by chunks.

2.1.2 (2014-04-25)
------------------

Fix
~~~

- Fail with error message when config path exists but is not a file.
  (fixes #11) [Casey Duquette]

  For example, the config file could be a directory.

2.1.1 (2014-04-15)
------------------

Fix
~~~

- Removed exception if you had file which name that matched a tag's
  name. (fixes #9) [Valentin Lab]

2.1.0 (2014-03-25)
------------------

New
~~~

- Python3 compatibility. [Valentin Lab]

- Much greater performance on big repository by issuing only one shell
  command for all the commits. (fixes #7) [Valentin Lab]

- Add ``init`` argument to create a full ``.gitchangelog.rc`` in current
  git repository. [Valentin Lab]

- Remove optional first argument that could specify the target git
  repository to consider. [Valentin Lab]

  This is to remove duplicate way to do things. ``gitchangelog`` should be run
  from within a git repository.

  Any usage of ``gitchangelog MYREPO`` can be written ``(cd MYREPO;
  gitchangelog)``.

- Use a standard formatting configuration by default. [Valentin Lab]

  A default `standard` way of formatting is used if you don't provide
  any configuration file. Additionaly, any option you define in your
  configuration file will be added "on-top" of the default configuration
  values. This can reduce config file size or even remove the need of
  one if you follow the standard.

  And, thus, you can tweak the standard for your needs by providing only partial
  configuration file. See tests for examples.

- Remove user or system wide configuration file lookup. [Valentin Lab]

  This follows reflexion that you build a changelog for a repository and
  that the rules to make the changelog should definitively be explicit and
  thus belongs to the repository itself.

  Not a justification, but removing user and system wide configuration files
  also greatly simplifies testability.

Fix
~~~

- Encoding issues with non-ascii chars. [Valentin Lab]

- Avoid using pipes for windows compatibility and be more performant by
  avoiding to unroll full log to get the last commit. [Valentin Lab]

- Better support of exotic features of git config file format. (fixes
  #4) [Valentin Lab]

  git config file format allows ambiguous keys:

      [a "b.c"]
          d = foo
      [a.b "c"]
          e = foo
      [a.b.c]
          f = foo

  Are all valid. So code was simplified to use directly ``git config``.
  This simplification will deal also with cases where section could be
  attributed values:

      [a "b"]
          c = foo
      [a]
          b = foo

  By avoiding to parse the entire content of the file, and relying on
  ``git config`` implementation we ensure to remain compatible and not
  re-implement the parsing of this file format.

- Gitchangelog shouldn't fail if it fails to parse your git config.
  [Michael Hahn]

2.0.0 (2013-08-20)
------------------

New
~~~

- Added a ``mako`` output engine with standard ReSTructured text format
  for reference. [Valentin Lab]

- Added some information on path lookup scheme to find
  ``gitchangelog.rc`` configuration file. [Valentin Lab]

- Added templating system and examples with ``mustache`` template
  support for restructured text and markdown output format. [David
  Loureiro]

Changes
~~~~~~~

- Removed ``pkg`` and ``dev`` commits from default sample changelog
  output. [Valentin Lab]

Fix
~~~

- Some error message weren't written on stderr. [Valentin Lab]

1.1.0 (2012-05-03)
------------------

New
~~~

- New config file lookup scheme which adds a new possible default
  location ``.gitchangelog.rc`` in the root of the git repository.
  [Valentin Lab]

- Added a new section to get a direct visual of ``gitchangelog`` output.
  Reworded some sentences and did some other minor additions. [Valentin
  Lab]

Changes
~~~~~~~

- Removed old ``gitchangelog.rc.sample`` in favor of the new documented
  one. [Valentin Lab]

Fix
~~~

- The sample file was not coherent with the doc, and is now accepting
  'test' and 'doc' audience. [Valentin Lab]

1.0.2 (2012-05-02)
------------------

New
~~~

- Added a new sample file heavily documented. [Valentin Lab]

Fix
~~~

- ``ignore_regexps`` where bogus and would match only from the beginning
  of the line. [Valentin Lab]

- Display author date rather than commit date. [Valentin Lab]

0.1.2 (2011-05-17)
------------------

New
~~~

- Added ``body_split_regexp`` option to attempts to format correctly
  body of commit. [Valentin Lab]

- Use a list of tuple instead of a dict for ``section_regexps`` to be
  able to manage order between section on find match. [Valentin Lab]

Fix
~~~

- ``git`` in later versions seems to fail on ``git config <key>`` with
  errlvl 255, that was not supported. [Valentin Lab]

- Removed Traceback when there were no tags at all in the current git
  repository. [Valentin Lab]

0.1.1 (2011-04-07)
------------------

New
~~~

- Added section classifiers (ie: New, Change, Bugs) and updated the
  sample rc file. [Valentin Lab]

- Added a succint ``--help`` support. [Valentin Lab]


