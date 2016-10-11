# Random Charity Bot

Twitter bot that tweets the name and website of a random charity

Load data
---------


Add twitter authentication details
----------------------------------

These should be added to a config file, in the same style as `example.cfg`. 

Set tweets going
----------------

Use the following command:
  
  python random_charity_bot.py -c config.cfg

Where `config.cfg` is the path to your configuration file. You can also add individual configuration options directly to the command, like:

  python random_charity_bot.py -c config.cfg --sleep 3600
  
(This would set the time between tweets to one hour)
