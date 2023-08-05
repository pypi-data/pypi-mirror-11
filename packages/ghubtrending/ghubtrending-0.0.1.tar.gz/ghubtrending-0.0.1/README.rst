===============================
Github Trending twitter bot
===============================

Posts to twitter one-at-a-day trending github repositories.
That is achieved doing the following:

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

.. warning::

    This gets the trending repositories CREATED last week
    Currently this seems to be GH's way of showing trending.gh.com
    but it might change in the future on GH's side. Not here.
    This one will continue to show last week's =)

This requires you've got ~/.ghtrending directory created.
I'm using that to have a link to data/ in there and auto-commit
its content

.. warning::

    This works only on python3.

Oh! And remember that this has to be called everyday.
A simple cron line will do =)

.. image:: https://img.shields.io/travis/XayOn/ghubtrending.svg
        :target: https://travis-ci.org/XayOn/ghubtrending

.. image:: https://img.shields.io/pypi/v/ghubtrending.svg
        :target: https://pypi.python.org/pypi/ghubtrending

* Free software: BSD license
* More documentation: https://ghubtrending.readthedocs.org.

Features
--------

* Python 3
* Twitts one twitt-at-a-day so people won't get tired
* Does not twitt repeated twitts
