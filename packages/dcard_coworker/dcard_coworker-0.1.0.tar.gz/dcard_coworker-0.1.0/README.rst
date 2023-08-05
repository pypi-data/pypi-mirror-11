dcard_coworker
==============

Dcard crawler using asyncio(coroutine)


Feature
-------
| Get article list and content using coroutine


Dependencies
------------
* Python 3.3 and :mod:`asyncio` or Python 3.4+
* aiohttp


Installation
------------
::

	python setup.py install

or 

::

    pip install dcard_coworker


Example
-------

::

    import asyncio

    import aiohttp
    import dcard_coworker

    @asyncio.coroutine
    def get_funny_articles():
        session = aiohttp.ClientSession()
        forum_name = 'funny'
        page_index = 1
        result = yield from dcard_coworker.get_articles_of_page(session, forum_name, page_index)
        print(result)

    def main():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([get_funny_articles()]))

    if __name__ == '__main__':
        main()


Todo
----
* Add testings
* Add more examples
  

Authors and License
-------------------
The ``dcard_coworker`` package is written by Chien-Wei Huang. It’s MIT licensed and freely available.

Feel free to improve this package and send a pull request to GitHub.

