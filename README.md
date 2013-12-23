This will export temperature and humidity readouts from tellstick net into a google drive spreadsheet.
I didnt want to use my own database to store values so google drive should have todo. And it can export it into a nice HTML for viewing automagically which will refetch the data on reload.

Put your keys in config.json and your gmail login info and the spreadsheet key as well. The key is what you see in the url for the spreadsheet after "ccc?key=" until the "&".

Using oauth for authentication and gdata for google integration.
