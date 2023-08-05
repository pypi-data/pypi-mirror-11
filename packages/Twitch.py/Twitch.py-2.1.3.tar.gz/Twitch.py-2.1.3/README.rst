Twitch.py
=========
Twitch on the Shell

.. image:: https://travis-ci.org/leibrockoli/Twitch.py.svg?branch=master
    :target: https://travis-ci.org/leibrockoli/Twitch.py

About
-----

Twitch.py is a script to access Twitch.tv from the shell/terminal emulator.
Instead of having to open up your browser to check your favorite games, you 
can do so from the terminal.

Additionally if you have Livestreamer installed, you can also load a stream 
directly into Livestreamer.

Installation
------------

Twitch.py now uses Pip as it's central package distribution. To install 
Twitch.py you can run the following Pip command (may need sudo access)

.. sourcecode:: console
    $ pip install Twitch.py 


This will require administrator privileges (so it may require a sudo on Unix)

Usage
-----

Once installed you can call Twitch.py through it's main script

.. sourcecode:: console

    $ twitch

This will show you the top 20 games on Twitch right now. From here you will 
be asked to input a number to pick which game's directory you want to check out.

Once you pick a directory, you can select a stream to boot into Livestreamer 
(if you have Livestreamer installed that is)

If you want to show more games/streams, use the -l option to pick more

.. sourcecode:: console

    $ twitch -l 30

If you want a game's listing immediately, you can use this option

.. sourcecode:: console

    $ twitch -g <game>

Where 'game' is the game you want to check out, ie:

.. sourcecode:: console

    $ twitch -g Dota 2

No quotes required.

You can mix and match these options.

.. sourcecode:: console

    $ twitch -l 30 -g Dota 2

Uninstallation
--------------

Twitch.py should be uninstalled through your system's normal uninstallation 
methods.

* Windows: Control Panel > Add or Remove Software
* Linux: can be removed via Pip (pip uninstall Twitch.py) 
* OSX: Same as Linux (?)

Requirements
------------

Twitch.py uses Livestreamer and Requests (both obtained from Pip). It also 
requires Python 2.7.2 or higher. Due to the changes in Python 3, Python 3 is 
preferred.

* Python 2.7.2 or Python 3
* Requests 
* Livestreamer

Problems
--------

Report any issues to the Issue Tracker, or check the FAQ for anything else.
