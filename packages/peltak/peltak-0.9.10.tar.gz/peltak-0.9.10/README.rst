###############################
peltak - Improve your workflow
###############################

**peltak** is a command line utility to improve your daily workflow. The main
focus so far was making managing a gitlab merge request easier.

Installation
=============

::

    $ pip install peltak

Basic usage
===========

**peltak** is built around the concept of actions. The app itself is just a
runtime for executing actions. All the functionality is implemented through
actions, and the app can be easily extended by creating new actions. The
set of actions available to the use is a combination of built-ins and actions
defined for the project. The project specific actions have to be stored
in ``.peltak/actions/`` directory under poject root directory.


The app has a built-in help system. By executing **peltak** without arguments
you will get the help screen. You can also get the list of available commands
and their description::

    $ peltak list-actions

To get help about a particular command, just execute it with ``-h`` or
``--help``::

    $ peltak list-actions -h

This will give you the command description along with the list of possible
arguments and their description.


Gitlab authentication
---------------------

The first time a command that connects to gitlb instance is used you will be
asked to login. Those are used to authenticate against the remote gitlab
instance and won't be saved. If you choose the option to stay logged in
the app will save your private token in the configuration and use it for
future sessions.

Configuration
=============

Right now the configuration is stored only on a per-project basis. To edit
the configuraiton use the ``config`` action. You can get the current
configuration using::

    $ peltak config

Managing merge request
=======================

First thing to do would be to fetch the mr template if it's defined for the
project (using gitlab issues)::

    $ peltak fetch-template

You can still edit merge request without the template, but you will have to 
enter the whole description manually.


There is one action designed for merge request creation and updates::

    $ peltak mr

It is a command line form for filling in the MR details. With each consecutive
run it will only aks for things only for thinkgs that weren't provided
before. If you wan't to change a field that was already field in the previous
runs, you can use the ``-u/--update`` option. So if you have already set the
title and problem and want to change it, you will need to execute:

    $ peltak mr -u title,problem

Releasing the MR
----------------

By default the title will be prepended with the **[WIP]** tag. To indicate that
you have finished working on the MR and it's ready, pass the ``--ready`` flag::

    $ peltak mr --ready

Pushing branch
==============

There is also a **push** action that will ask you all the questions before
pushing the branch. It will always push the branch you are currently on so
you won't need to manually specify it either. As with **mr** action, the
questions you answer *yes* to won't be asked again in the future. The downside
is that right now there is no way to update the answer, so once you say yes
it will stay that way. I plan to add an option to update the answers as well,
but it wasn't crucial so far so it got postponed.

