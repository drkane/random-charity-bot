# Random Charity Bot

Twitter bot that tweets the name and website of a random charity. The data is based on the
register held by the Charity Commission for England and Wales, [released as open data](http://data.charitycommission.gov.uk/).

The bot randomly selects an active charity from the register, and tweets it. If the website
of the charity is known it tweets that too, otherwise it gives a link to the official register
entry for that charity.

This bot isn't affiliated with the Charity Commission, and gives no endorsement of the charities
tweeted.

Load data
---------

Fetches data from the Charity Commission open data page, and turns it into a JSON file with the
needed details in. The data file is then used by `random_charity_bot.py` to construct a tweet
about a charity.

    python fetch_charity_data.py
    
If the url of the Charity Commission data changes you can add the `--data-url` property to point
to the new address.

The data is updated monthly so running this command every month will ensure new charities are 
tweeted and removed ones aren't.

Add twitter authentication details
----------------------------------

You need to set up a twitter app, and get four keys to authorize your app:

- Consumer key
- Consumer secret
- Access token
- Access token secret
 
[Instructions are available here](https://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/)

These should be added to a config file, in the same style as `example.cfg`. Call this file
something like `config.cfg`.

Set tweets going
----------------

Use the following command:
  
    python random_charity_bot.py -c config.cfg

Where `config.cfg` is the path to your configuration file. You can also add individual configuration options directly to the command, like:

    python random_charity_bot.py -c config.cfg --sleep 3600
  
(This would set the time between tweets to one hour)

Possible future development
---------------------------

- include Scottish & Northern Irish charities
- regional/sector version
- boost larger charities in random search to show more household names
- lookup twitter account and use that handle (eg <opencharities.org> has data)

Credits
-------

- Fetch charity data script adapted from <https://github.com/OpenDataServices/grantnav/blob/master/dataload/fetch_charity_data.py>
- Twitter API use from <https://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/>
- Charity data from <http://data.charitycommission.gov.uk/> - used under [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
