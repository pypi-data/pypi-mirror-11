Boomerang.io Python API client
==============

Installing
______________

.. code:: python

  pip install boomerang-client

Example usage
--------------

.. code:: python

  import calendar
  import datetime
  from boomerang.client import BoomerangClient
  
  bc = BoomerangClient(<projectid>, <apikey>)
  
  future = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
  date = calendar.timegm(future.timetuple())
  params = { "url": "http://theurl.com", "msg": "the message", "run_at": date }
  
  print bc.create_boomerang(params).text
  print bc.get_all_boomerangs().text
