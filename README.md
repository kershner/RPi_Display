# Raspberry Pi GIF Display
<sub><sup>*This guide is mostly for my own memory when I need to nuke and re-deploy the device, but feel free to use the code for your own project!*</sup></sub>

#### This project uses a bunch of different technologies to run a constantly updating GIF Display powered by a Raspberry Pi.

# TL:DR...
1. Scripts run nightly on a server to update and maintain a repository of gif URLs
2. A website is established to continually rotate those gifs according to user settings
3. A Pi and a display are set up and configured to boot directly to the website

## Section 1 - Server Side Scripts
[scrape_reddit.py](https://github.com/kershner/RPi_Display/blob/master/rpi_display/scripts/scrape_reddit.py) uses the reddit API to grab gifs from a bunch of subreddits I've chosen (visible in the script).  

Gif URLs are collected and deposited into various text files according to the type of subreddit they were collected from.  

The 2nd script, [clean_up_urls.py](https://github.com/kershner/RPi_Display/blob/master/rpi_display/scripts/clean_up_urls.py), then parses each text file and tests every URL to make sure it still returns HTTP 200 and that it's not also in another text file called `bad_urls.txt` I've set up to weed out "problematic" gifs (mostly the odd 5 second porn loop that finds its way into the rotation from time to time).

I've chosen text files as my storage method vs. a database because they're simply a bit easier to interact with for the project's current size.  For example I can simply paste a URL into my `bad_urls.txt` file when I come across one as opposed to writing a SQL/ORM statement each time or creating a separate script/interface.  I might revisit this decision sometime in the future.

These scripts should just work (although I'm sure you'll want to heavily tweak them), but one required modification is to update the user agent string for PRAW (Python Reddit API Wrapper) located [here](https://github.com/kershner/RPi_Display/blob/master/rpi_display/scripts/scrape_reddit.py#L142).

## Section 2 - Website
The [website](kershner.org/pi_display) is a *very* simple bit of HTML and JavaScript designed specifically to be viewed on the display I've chosen.

The HTML is [here](https://github.com/kershner/RPi_Display/tree/master/rpi_display/app/templates) and the JavaScript is [here](https://github.com/kershner/RPi_Display/tree/master/rpi_display/app/static/js).

The site reads configuration settings from another file on the server, the **category** for the gifs and the **delay** (in seconds). The category determines which text file to pull URLs from, and the delay setting is used in the `setInterval()` function that drives the gif rotation.  

Each time a gif is played it is written to the config file so it can be viewed on the configuration website - mostly so I can save a particularly good gif that pops onto the display.  Some Python on the server will then remove that gif from the pool of gifs to be played so it won't come up again until the pool has been exhausted and re-created.

The loading animation is a fun bit of JavaScript I cooked up called [colorWave](http://codepen.io/kershner/pen/Yyyzjz) and the fade out/fade in for the gifs is handled by a [CSS transition](https://github.com/kershner/RPi_Display/blob/master/rpi_display/app/static/css/pi_display.css#L6) for better performance.

## Section 3 - Hardware
Here I'll detail the process of hooking up the RPi and display and also the configuration of the OS/software to boot directly to the website.
