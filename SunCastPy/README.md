# SunCastPy
- This package reads data from NOAA and parses it to get the forecast by hour for the location selected.
- It has 2 modes cli and api/html.
## API/HTML
- Home page has a list of clickable buttons to select any of the 78 cities of Puerto Rico.
- /forecast/{city} has the forecast for the city
    - it has options to:
        - summarize the data. For example its going to rain from 3pm-6pm instead of seeing the duplicate forecast of rain 4 times (3,4,5,6)pm.
        - extend the number of days to see the forecast
- additional api's return a json response. More details can be seen by visiting the docs after launching the app.
## CLI
- Command line version of the api with the same functions as the html with the addition of being able to get other forecasts outside of Puerto Rico by specifying the latitude and longitude of the target location.
- For more information run `forecast --help` from command line