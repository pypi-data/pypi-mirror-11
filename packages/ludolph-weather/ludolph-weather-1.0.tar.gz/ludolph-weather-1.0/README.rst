ludolph-weather
###############

`Ludolph <https://github.com/erigones/Ludolph>`_: Weather plugin

Simple plugin that displays current weather information or weather forecast.
Although it currently uses the `OpenWeatherMap <http://openweathermap.org>`_ service it can be easily extended to support other weather forecast providers.

.. image:: https://badge.fury.io/py/ludolph-weather.png
    :target: http://badge.fury.io/py/ludolph-weather


Installation
------------

- Install the latest released version using pip::

    pip install ludolph-weather

- Add new plugin section into Ludolph configuration file::

    [ludolph_weather.open_weather_map]
    api_key = xxxxxxxxxxxxxxxxxxxxxxxxx
    default_location = Bratislava,SK
    timezone = Europe/Bratislava

- Reload Ludolph::

    service ludolph reload


**Dependencies:**

- `Ludolph <https://github.com/erigones/Ludolph>`_ (0.6.0+)
- `requests <http://docs.python-requests.org/>`_
- `pytz <http://pytz.sourceforge.net/>`_


Links
-----

- Wiki: https://github.com/erigones/Ludolph/wiki/How-to-create-a-plugin#create-3rd-party-plugin
- Bug Tracker: https://github.com/erigones/ludolph-weather/issues
- Google+ Community: https://plus.google.com/u/0/communities/112192048027134229675
- Twitter: https://twitter.com/erigones


License
-------

For more information see the `LICENSE <https://github.com/erigones/ludolph-weather/blob/master/LICENSE>`_ file.
