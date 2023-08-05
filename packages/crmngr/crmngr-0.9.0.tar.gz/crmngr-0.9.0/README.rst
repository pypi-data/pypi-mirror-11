######
crmngr
######

.. contents:: Table of Contents

********
Overview
********

crmngr is a tool to aid with the management of a r10k-style control repository.

about r10k
==========

from `r10k's github page <https://github.com/puppetlabs/r10k>`_:
    R10k provides a general purpose toolset for deploying Puppet environments
    and modules. It implements the `Puppetfile`_ format and provides a native
    implementation of Puppet dynamic environments.
    
r10k is basically a git repository where each branch representes a dynamic
puppet environment. When working with more than a handful environments it is
hard to keep track of the modules spread over all these branches. Here is where
crmngr comes to the rescue.

crmngr
======

crmngr (Control Repository Manager) can generate reports and help with adding,
updating or removing modules over multiple branches.

See usage section of this document for details.

CAVEATS:
    Currently crmngr will not parse/validate metadata.json and thus will not
    check if all dependencies are satisfied between the modules in a certain
    environment.


************
Installation
************

crmngr can be installed using different methods, see below.

Additionally the git binary needs to be in the invoking users PATH, and the
access to the r10k control repository needs to be password-less. (f.e. using
SSH pubkey authentication). This also applies to git repositories used in
Puppetfiles.

pip (recommanded)
=================

.. code-block:: text

    pip install crmngr


setuptools
==========

.. code-block:: text

    python setup.py install


*************
Configuration
*************

crmngr is looking for its configuration in the file `~/.crmngr/config`.

The only mandatory setting is `repository` in the `crmngr` section defining the
git url of the r10k-style control repository.

.. code-block:: ini

    [crmngr]
    repository = git@git.example.org:user/control.git
    
If started without configuration file, crmngr will offer to create one.


Additionally the configuration can hold information to categorize modules, when
writing puppetfiles.

**NOTE**:
    These categories are not taken into account in reports.
    Also crmngr does not currently parse this information when loading
    Puppetfiles from the control repository.

.. code-block:: ini

    [crmngr]
    repository = git@git.example.org:user/control.git
    categories = base, lamp

    [base]
    apt
    concat
    inifile
    stdlib

    [lamp]
    apache
    mysql
    php

This will group the modules under the following headers in the resulting
Puppetfile:

.. code-block:: text

    # BASE modules ###

    # LAMP modules ###

    # UNCATEGORIZED modules ###

The order in categories option is respected, with uncategorized modules always
printed at the end of the file.


*****
Usage
*****

.. code-block:: text

    usage: crmngr [-h] [--debug] [--no-version-check]
              [--no-version-check-cache] {report,update,clean} ...

    manage a r10k-style control repository

    optional arguments:
      -h, --help            show this help message and exit
      --debug               enable debug output
      --no-version-check    do not check for latest versions. Default behaviour
                            is to fetch current version information for every
                            module found in every Puppetfile. This may take a
                            considerable amount of time, especially on first 
                            run
      --no-version-check-cache
                            Do not cache latest versions. Default behaviour is
                            to cache all version information for 24 hours

    commands:
      valid commands

      {report,update,clean}
        report              Puppetfile reporting (-h for usage details)
        update              Puppetfile manipulation (-h for usage details)
        clean               Clean cache



report
======

The report command is used to generate reports about module versions used in
the various branches of a control repository.

The report is aggregated by module, listing all module version, which branch
they use and what would be the latest installable version. (Version for
forge.puppetlabs.com modules, Tag for modules installed from git)

**NOTE**:
    The report command will output colorized text. When using a pager,
    make sure the pager understands this colors. For less use option -r:

    .. code-block:: text

        crmngr report | less -r

        # or if the output shall be preserved in a file
        crmngr report > report.out
        less -r report.out

        # or if you want to strip color codes all together
        crmngr report | perl -pe 's/\e\[?.*?[\@-~]//g'


.. code-block:: text

    usage: crmngr report [-h] [--report-unused]
                         [--branches [BRANCHES [BRANCHES ...]]]
                         [--modules [MODULES [MODULES ...]]]

    optional arguments:
      -h, --help            show this help message and exit
      --report-unused       additionally list branches that are not using a
                            certain module
      --branches [BRANCHES [BRANCHES ...]], -b [BRANCHES [BRANCHES ...]]
                            restrict output to specific branch(es). Supports
                            glob(7)-style wildcard patterns
      --modules [MODULES [MODULES ...]], -m [MODULES [MODULES ...]]
                            restrict output to specific module(s). Supports
                            glob(7)-style wildcard patterns


Examples
--------

Gather a report of all module versions, in all branches:

.. code-block:: text

    crmngr report


Gather a report of all modules in branches ending with Production:

.. code-block:: text

    crmngr report --branches "*Production"


Gather a report of all modules that contain profile in their name:

.. code-block:: text

    crmngr report --modules "*profile*"


Gather a report of modules apache, php and mysql in branches starting with Cust:

.. code-block:: text

    crmngr report --branches "Cust*" --modules apache php mysql

Gather a report of all modules in branches CustProd, CustStage and CustDev.
Additionally list which branches do not use a specific module.

.. code-block:: text

    crmngr report --branches CustProd CustStage CustDev --report-unused

update
======

The update command updates, adds or removes modules from Puppetfiles.

If you execute crmngr update with neither --git nor --module, it will write
a sanitized version of the Puppetfile, using the current module versions.

The update command will display a diff for every affected branch and will
ask you to confirm the changes.

**NOTE**:
    The author part of a module name is *only* used to find the correct module
    on forge. If you run update on --module puppetlabs/stdlib, this will also
    affect all other stdlib modules that might be in a Puppetfile (i.e.
    otherauthor/stdlib or stdlib installed from git will be replaced by
    puppetlabs/stdlib).


.. code-block:: text

    usage: crmngr update [-h] [--add | --remove]
                         [--branches [BRANCHES [BRANCHES ...]]] 
                         [--module MODULE]
                         [--git URL | --version [VERSION]] 
                         [--tag [TAG] | --commit COMMIT | --branch BRANCH]

    optional arguments:
      -h, --help            show this help message and exit
      --diff-only           only show changes
      --non-interactive, -n
                            In non-interactive mode, crmngr will neither ask for
                            confirmation before commit or push, nor will it show
                            diffs of what will be changed. Use with care!
      --add                 add module if not already in Puppetfile. Default
                            behaviour is to only update module in branches it
                            is already defined.
      --remove              remove module from Puppetfile. Version identifying
                            parameters (--version, --tag, --commit, --branch)
                            are NOT taken into account. All module versions are
                            removed!
      --branches [BRANCHES [BRANCHES ...]], -b [BRANCHES [BRANCHES ...]]
                            update only specific branch(es). Default: All 
                            branches.
      --module MODULE       module to update/add/remove, for modules fetched
                            from forge.puppetlabs.com the format needs to be
                            author/modulename
      --git URL             git URL of module's repository. If not specified,
                            the module is fetched from forge.puppetlabs.com
      --version [VERSION]   version of forge.puppetlabs.com module. If
                            parameter is specified without VERSION, latest
                            available version from forge.puppetlabs.com will
                            be used instead
      --tag [TAG]           tag of git module. If parameter is specified without
                            TAG, latest tag from repository is used instead
      --commit COMMIT       commit of git module
      --branch BRANCH       branch of git module


Examples
--------

Sanitize Puppetfiles of all branches:

.. code-block:: text

    crmngr update


Update stdlib module in all branches to latest forge version.


.. code-block:: text

    crmngr update --module puppetlabs/stdlib --version


Update stdlib module in all branches to latest forge version. Additionally add
the module to branches that currently lack the stdlib module

.. code-block:: text

    crmngr update --add --module puppetlabs/stdlib --version


Remove icinga modules from control repository branches that end with Vagrant.

.. code-block:: text

    crmngr update --remove --module icinga --branches "*Vagrant"


Update apache module to git branch 2.0.x in control repository branch Devel

.. code-block:: text

    crmngr update --branches Devel \
                  --module apache \
                  --git git@github.com:puppetlabs/puppetlabs-apache.git \
                  --branch 2.0.x


clean
=====

The clean command clears the cache used by crmngr.

.. code-block:: bash

    usage: crmngr clean
    
    
.. _github-r10k: https://github.com/puppetlabs/r10k

.. _Puppetfile: 
  https://github.com/puppetlabs/r10k/blob/master/doc/puppetfile.mkd