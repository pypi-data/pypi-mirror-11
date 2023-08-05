Github Trending twitter bot
===============================

Posts to twitter one-at-a-day trending github repositories.

.. image:: https://img.shields.io/travis/XayOn/GHubtrending.svg
        :target: https://travis-ci.org/XayOn/GHubtrending

.. image:: https://img.shields.io/pypi/v/ghubtrending.svg
        :target: https://pypi.python.org/pypi/ghubtrending

* Free software: BSD license
* More documentation: https://ghubtrending.readthedocs.org.


Workflow
========

* Check if if this week we've got a json file, if not
    * Get the week's twitter repositories
    * Store them in a json file
    * Publish the json file to github (just for coolness)
* If we've got it.
    * Get current day's twitter trending.

This means that we're not actually posting today's trending
but one specific day's Nth trending being N the day of week.

But that's ok, as I'm doing this to have one specific
repository each week.

Also, we mantain a list of already-posted repos and get the
next one if we've already posted that.

Features
--------

* Python 3
* Twitts one twitt-at-a-day so people won't get tired
* Does not twitt repeated twitts

Usage
-----

Install it by executing:

::

    python setup.py install

I recommend the usage of a virtualenv.

This will create an entry_point, called ghubtrending, that will update the
twitter status with the repository of the week.

This works only on python3.
Configuration file should be, located at ~/.ghtrend_bot.cfg as follows:


::

    [github]
    login=
    password=

    [twitter]
    CONSUMER_KEY=
    CONSUMER_SECRET=
    ACCESS_TOKEN=
    ACCESS_TOKEN_SECRET=


.. warning::

    This gets the trending repositories CREATED last week
    Currently this seems to be GH's way of showing trending.gh.com
    but it might change in the future on GH's side. Not here.
    This one will continue to show last week's =)

This requires you've got ~/.ghtrending directory created.
I'm using that to have a link to data/ in there and auto-commit
its content
