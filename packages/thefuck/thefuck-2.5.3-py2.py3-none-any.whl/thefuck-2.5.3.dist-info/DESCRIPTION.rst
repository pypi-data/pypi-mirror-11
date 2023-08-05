The Fuck |Build Status|
=======================

| Magnificent app which corrects your previous console command,
| inspired by a `@liamosaur <https://twitter.com/liamosaur/>`_
| `tweet <https://twitter.com/liamosaur/status/506975850596536320>`_.

|gif with examples|

Few more examples:

.. code:: bash

    ➜ apt-get install vim
    E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
    E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

    ➜ fuck
    sudo apt-get install vim [enter/ctrl+c]
    [sudo] password for nvbn:
    Reading package lists... Done
    ...

.. code:: bash

    ➜ git push
    fatal: The current branch master has no upstream branch.
    To push the current branch and set the remote as upstream, use

        git push --set-upstream origin master


    ➜ fuck
    git push --set-upstream origin master [enter/ctrl+c]
    Counting objects: 9, done.
    ...

.. code:: bash

    ➜ puthon
    No command 'puthon' found, did you mean:
     Command 'python' from package 'python-minimal' (main)
     Command 'python' from package 'python3' (main)
    zsh: command not found: puthon

    ➜ fuck
    python [enter/ctrl+c]
    Python 3.4.2 (default, Oct  8 2014, 13:08:17)
    ...

.. code:: bash

    ➜ git brnch
    git: 'brnch' is not a git command. See 'git --help'.

    Did you mean this?
        branch

    ➜ fuck
    git branch [enter/ctrl+c]
    * master

.. code:: bash

    ➜ lein rpl
    'rpl' is not a task. See 'lein help'.

    Did you mean this?
             repl

    ➜ fuck
    lein repl [enter/ctrl+c]
    nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
    REPL-y 0.3.1
    ...

| If you are not scared to blindly run the changed command, there is a
``require_confirmation``
| `settings <https://pypi.python.org/pypi/thefuck#settings>`_ option:

.. code:: bash

    ➜ apt-get install vim
    E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
    E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

    ➜ fuck
    sudo apt-get install vim
    [sudo] password for nvbn:
    Reading package lists... Done
    ...

Requirements
------------

-  python (2.7+ or 3.3+)
-  pip
-  python-dev

Installation
------------

Install ``The Fuck`` with ``pip``:

.. code:: bash

    sudo pip install thefuck

`Or using an OS package manager (OS X, Ubuntu,
Arch). <https://github.com/nvbn/thefuck/wiki/Installation>`_

You should place this command in your ``.bash_profile``, ``.bashrc``,
``.zshrc`` or other startup script:

.. code:: bash

    eval "$(thefuck-alias)"
    # You can use whatever you want as an alias, like for Mondays:
    eval "$(thefuck-alias FUCK)"

`Or in your shell config (Bash, Zsh, Fish, Powershell,
tcsh). <https://github.com/nvbn/thefuck/wiki/Shell-aliases>`_

| Changes will be available only in a new shell session.
| To make them available immediately, run ``source ~/.bashrc`` (or your
shell config file like ``.zshrc``).

Update
------

.. code:: bash

    sudo pip install thefuck --upgrade

**Aliases changed in 1.34.**

How it works
------------

| The Fuck tries to match a rule for the previous command, creates a new
command
| using the matched rule and runs it. Rules enabled by default are as
follows:

-  ``cargo`` – runs ``cargo build`` instead of ``cargo``;
-  ``cargo_no_command`` – fixes wrongs commands like ``cargo buid``;
-  ``cd_correction`` – spellchecks and correct failed cd commands;
-  ``cd_mkdir`` – creates directories before cd'ing into them;
-  ``cd_parent`` – changes ``cd..`` to ``cd ..``;
-  ``composer_not_command`` – fixes composer command name;
-  ``cp_omitting_directory`` – adds ``-a`` when you ``cp`` directory;
-  ``cpp11`` – adds missing ``-std=c++11`` to ``g++`` or ``clang++``;
-  ``dirty_untar`` – fixes ``tar x`` command that untarred in the
   current directory;
-  ``dirty_unzip`` – fixes ``unzip`` command that unzipped in the
   current directory;
-  ``django_south_ghost`` – adds ``--delete-ghost-migrations`` to failed
   because ghosts django south migration;
-  ``django_south_merge`` – adds ``--merge`` to inconsistent django
   south migration;
-  ``docker_not_command`` – fixes wrong docker commands like
   ``docker tags``;
-  ``dry`` – fixes repetitions like ``git git push``;
-  ``fix_alt_space`` – replaces Alt+Space with Space character;
-  ``git_add`` – fixes *"Did you forget to 'git add'?"*;
-  ``git_branch_delete`` – changes ``git branch -d`` to
   ``git branch -D``;
-  ``git_branch_list`` – catches ``git branch list`` in place of
   ``git branch`` and removes created branch;
-  ``git_checkout`` – fixes branch name or creates new branch;
-  ``git_diff_staged`` – adds ``--staged`` to previous ``git diff`` with
   unexpected output;
-  ``git_fix_stash`` – fixes ``git stash`` commands (misspelled
   subcommand and missing ``save``);
-  ``git_not_command`` – fixes wrong git commands like ``git brnch``;
-  ``git_pull`` – sets upstream before executing previous ``git pull``;
-  ``git_pull_clone`` – clones instead of pulling when the repo does not
   exist;
-  ``git_push`` – adds ``--set-upstream origin $branch`` to previous
   failed ``git push``;
-  ``git_push_pull`` – runs ``git pull`` when ``push`` was rejected;
-  ``git_stash`` – stashes you local modifications before rebasing or
   switching branch;
-  ``go_run`` – appends ``.go`` extension when compiling/running Go
   programs
-  ``grep_recursive`` – adds ``-r`` when you trying to ``grep``
   directory;
-  ``gulp_not_task`` – fixes misspelled gulp tasks;
-  ``has_exists_script`` – prepends ``./`` when script/binary exists;
-  ``heroku_no_command`` – fixes wrong ``heroku`` commands like
   ``heroku log``;
-  ``history`` – tries to replace command with most similar command from
   history;
-  ``java`` – removes ``.java`` extension when running Java programs;
-  ``javac`` – appends missing ``.java`` when compiling Java files;
-  ``lein_not_task`` – fixes wrong ``lein`` tasks like ``lein rpl``;
-  ``ls_lah`` – adds ``-lah`` to ``ls``;
-  ``man`` – changes manual section;
-  ``man_no_space`` – fixes man commands without spaces, for example
   ``mandiff``;
-  ``mercurial`` – fixes wrong ``hg`` commands;
-  ``mkdir_p`` – adds ``-p`` when you trying to create directory without
   parent;
-  ``no_command`` – fixes wrong console commands, for example
   ``vom/vim``;
-  ``no_such_file`` – creates missing directories with ``mv`` and ``cp``
   commands;
-  ``open`` – prepends ``http`` to address passed to ``open``;
-  ``pip_unknown_command`` – fixes wrong ``pip`` commands, for example
   ``pip instatl/pip install``;
-  ``python_command`` – prepends ``python`` when you trying to run not
   executable/without ``./`` python script;
-  ``python_execute`` – appends missing ``.py`` when executing Python
   files;
-  ``quotation_marks`` – fixes uneven usage of ``'`` and ``"`` when
   containing args'
-  ``rm_dir`` – adds ``-rf`` when you trying to remove directory;
-  ``sed_unterminated_s`` – adds missing '/' to ``sed``'s ``s``
   commands;
-  ``sl_ls`` – changes ``sl`` to ``ls``;
-  ``ssh_known_hosts`` – removes host from ``known_hosts`` on warning;
-  ``sudo`` – prepends ``sudo`` to previous command if it failed because
   of permissions;
-  ``switch_layout`` – switches command from your local layout to en;
-  ``systemctl`` – correctly orders parameters of confusing
   ``systemctl``;
-  ``test.py`` – runs ``py.test`` instead of ``test.py``;
-  ``tsuru_login`` – runs ``tsuru login`` if not authenticated or
   session expired;
-  ``tmux`` – fixes ``tmux`` commands;
-  ``whois`` – fixes ``whois`` command.

Enabled by default only on specific platforms:

-  ``apt_get`` – installs app from apt if it not installed;
-  ``brew_install`` – fixes formula name for ``brew install``;
-  ``brew_unknown_command`` – fixes wrong brew commands, for example
   ``brew docto/brew doctor``;
-  ``brew_upgrade`` – appends ``--all`` to ``brew upgrade`` as per
   Homebrew's new behaviour;
-  ``pacman`` – installs app with ``pacman`` or ``yaourt`` if it is not
   installed.

Bundled, but not enabled by default:

-  ``git_push_force`` – adds ``--force`` to a ``git push`` (may conflict
   with ``git_push_pull``);
-  ``rm_root`` – adds ``--no-preserve-root`` to ``rm -rf /`` command.

Creating your own rules
-----------------------

| For adding your own rule you should create ``your-rule-name.py``
| in ``~/.thefuck/rules``. The rule should contain two functions:

.. code:: python

    match(command: Command, settings: Settings) -> bool
    get_new_command(command: Command, settings: Settings) -> str

| Also the rule can contain an optional function
| ``side_effect(command: Command, settings: Settings) -> None`` and
| optional ``enabled_by_default``, ``requires_output`` and ``priority``
variables.

``Command`` has three attributes: ``script``, ``stdout`` and ``stderr``.

``Settings`` is a special object filled with ``~/.thefuck/settings.py``
and values from env (`see more below <https://pypi.python.org/pypi/thefuck#settings>`_).

Simple example of the rule for running script with ``sudo``:

.. code:: python

    def match(command, settings):
        return ('permission denied' in command.stderr.lower()
                or 'EACCES' in command.stderr)


    def get_new_command(command, settings):
        return 'sudo {}'.format(command.script)

    # Optional:
    enabled_by_default = True

    def side_effect(command, settings):
        subprocess.call('chmod 777 .', shell=True)

    priority = 1000  # Lower first, default is 1000

    requires_output = True

| `More examples of
rules <https://github.com/nvbn/thefuck/tree/master/thefuck/rules>`_,
| `utility functions for
rules <https://github.com/nvbn/thefuck/tree/master/thefuck/utils.py>`_.

Settings
--------

The Fuck has a few settings parameters which can be changed in
``~/.thefuck/settings.py``:

-  ``rules`` – list of enabled rules, by default
   ``thefuck.conf.DEFAULT_RULES``;
-  ``require_confirmation`` – requires confirmation before running new
   command, by default ``True``;
-  ``wait_command`` – max amount of time in seconds for getting previous
   command output;
-  ``no_colors`` – disable colored output;
-  ``priority`` – dict with rules priorities, rule with lower
   ``priority`` will be matched first;
-  ``debug`` – enables debug output, by default ``False``.

Example of ``settings.py``:

.. code:: python

    rules = ['sudo', 'no_command']
    require_confirmation = True
    wait_command = 10
    no_colors = False
    priority = {'sudo': 100, 'no_command': 9999}
    debug = False

Or via environment variables:

-  ``THEFUCK_RULES`` – list of enabled rules, like
   ``DEFAULT_RULES:rm_root`` or ``sudo:no_command``;
-  ``THEFUCK_REQUIRE_CONFIRMATION`` – require confirmation before
   running new command, ``true/false``;
-  ``THEFUCK_WAIT_COMMAND`` – max amount of time in seconds for getting
   previous command output;
-  ``THEFUCK_NO_COLORS`` – disable colored output, ``true/false``;
-  ``THEFUCK_PRIORITY`` – priority of the rules, like
   ``no_command=9999:apt_get=100``,
   rule with lower ``priority`` will be matched first;
-  ``THEFUCK_DEBUG`` – enables debug output, ``true/false``.

For example:

.. code:: bash

    export THEFUCK_RULES='sudo:no_command'
    export THEFUCK_REQUIRE_CONFIRMATION='true'
    export THEFUCK_WAIT_COMMAND=10
    export THEFUCK_NO_COLORS='false'
    export THEFUCK_PRIORITY='no_command=9999:apt_get=100'

Developing
----------

Install ``The Fuck`` for development:

.. code:: bash

    pip install -r requirements.txt
    python setup.py develop

Run unit tests:

.. code:: bash

    py.test

Run unit and functional tests (requires docker):

.. code:: bash

    FUNCTIONAL=true py.test

For sending package to pypi:

.. code:: bash

    sudo apt-get install pandoc
    ./release.py

License MIT
-----------

Project License can be found `here <https://github.com/nvbn/thefuck/blob/master/LICENSE.md>`_.

.. |Build Status| image:: https://travis-ci.org/nvbn/thefuck.svg
   :target: https://travis-ci.org/nvbn/thefuck
.. |gif with examples| image:: https://raw.githubusercontent.com/nvbn/thefuck/master/example.gif


