# Raspberry Pi GIF Display
<sub><sup>*This guide is mostly for my own memory when I need to nuke and re-deploy the device, but feel free to use the code for your own project!*</sup></sub>

**This project uses a few different technologies to run a constantly updating GIF Display powered by a Raspberry Pi.**

![RPi Gif Display Build Process](http://www.kershner.org/static/images/pi-display.gif "RPi Gif Display Build Process")

# [Video](https://www.youtube.com/watch?v=PFvCgDggzr4)

# TL:DR...
**[1.](#scripts)**  Scripts run nightly on a server to update and maintain a repository of gif URLs

**[2.](#website)**  A website is established to continually rotate those gifs according to user settings

**[3.](#hardware)**  A Pi and a display are set up and configured to boot directly to the website




**Parts List (Amazon Links for Convenience)**
* [Raspberry Pi 2 Model B](http://www.amazon.com/Raspberry-Pi-Model-Project-Board/dp/B00T2U7R7I/ref=sr_1_1?s=pc&ie=UTF8&qid=1443628402&sr=1-1&keywords=raspberry+pi+2)
* [Official 7'' Touchscreen Display](http://www.amazon.com/OFFICIAL-RASPBERRY-FOUNDATION-TOUCHSCREEN-DISPLAY/dp/B0153R2A9I/ref=sr_1_1?s=pc&ie=UTF8&qid=1443628430&sr=1-1&keywords=raspberry+pi+official+7%27%27+touchscreen)
* [Pimoroni Display Frame](https://shop.pimoroni.com/collections/new-products/products/raspberry-pi-7-touchscreen-display-frame)
* [Cheap WiFi Dongle](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_sim_147_3?ie=UTF8&refRID=03W9TVY2JZE865P2HR92&dpID=31ChKj3dl7L&dpSrc=sims&preST=_AC_UL160_SR160%2C160_)
* [Cheap USB Patch Cable](http://www.amazon.com/StarTech-com-Inch-Micro-USB-Cable/dp/B003YKX6WM/ref=sr_1_2?s=pc&ie=UTF8&qid=1443628618&sr=1-2&keywords=usb+patch+cable)
* 2A USB Power Supply (most cell phone chargers)
* MicroSD Card


<a name="scripts">

# Server Side Scripts
[scrape_reddit.py](https://github.com/kershner/RPi_Display/blob/master/rpi_display/scripts/scrape_reddit.py) uses the reddit API to grab gifs from a bunch of subreddits I've chosen (visible in the script).  

Gif URLs are collected and deposited into various [text files](https://github.com/kershner/RPi_Display/tree/master/rpi_display/urls) according to the type of subreddit they were collected from.  

A second script ([clean_up_urls.py](https://github.com/kershner/RPi_Display/blob/master/rpi_display/scripts/clean_up_urls.py)) then parses each text file and tests every URL for HTTP 200 and that it's not also in another text file called `bad_urls.txt` I've set up to weed out "problematic" gifs (the ocasional 5 second porn loop or what have you).

I've chosen text files as my storage method vs. a database because they're simply a bit easier to interact with for the project's current size.  For example I can quickly paste a URL into my `bad_urls.txt` file as I come across them instead of having to write a SQL/ORM statement each time or creating a separate script/interface.  I'll probably revisit this decision as my gif repository grows.

These scripts should just work wherever you choose to run them (although I'm sure you'll want to heavily tweak them), but one required modification is to update the user agent string for PRAW (Python Reddit API Wrapper) located [here](https://github.com/kershner/RPi_Display/blob/master/rpi_display/scripts/scrape_reddit.py#L142).

<a name="website">

# Website
The [website](http://www.kershner.org/pi_display) is a *very* simple bit of HTML and JavaScript designed specifically to be viewed on the display I've chosen.  The site is built with [Flask](http://flask.pocoo.org/) and utilizes [jQuery](https://jquery.com/).  You can find the HTML [here](https://github.com/kershner/RPi_Display/tree/master/rpi_display/app/templates) and the JavaScript [here](https://github.com/kershner/RPi_Display/tree/master/rpi_display/app/static/js).

The site reads configuration settings from another file on the server, the **category** for the gifs and the **delay** (in seconds). The category determines which text file to pull URLs from, and the delay setting is used in the `setInterval()` function that drives the gif rotation.  

Each time a gif is played it is written to the config file so it can be viewed on the configuration website - mostly so I can save a particularly good gif that pops onto the display.  Some Python on the server will then remove that gif from the pool of gifs to be played so it won't come up again until the pool has been exhausted and re-created.

The loading animation is a fun bit of JavaScript I cooked up called [colorWave](http://codepen.io/kershner/pen/Yyyzjz) and the fade out/fade in for the gifs is handled by a [CSS transition](https://github.com/kershner/RPi_Display/blob/master/rpi_display/app/static/css/pi_display.css#L6) for better performance.

<a name="hardware">

# Hardware / Configuration
First things first, you'll need to get a suitable OS installed onto an SD card (for the RPi 1) or a MicroSD card (for the RPi 2).  [This official guide](https://www.raspberrypi.org/help/noobs-setup/) should get you started.  Once the SD card is ready to go, you'll need to hook up a working display and mouse/keyboard to the Pi, insert the SD card, and boot her up.

The first thing I always do on my Pi's first boot is set up [RDP](https://en.wikipedia.org/wiki/Remote_Desktop_Protocol) so I can SSH to the Pi from my desktop PC and not have to worry about hooking up an external display.  To do this you need to set up your Pi's WiFi connection (I usually just do this through the X desktop), install **xrdp** - `sudo apt-get install xrdp`, find your Pi's IP address on your local network (I do this through my router's admin panel, though IPConfig would work too), and then use Windows 7+'s native Remote Desktop application to SSH in.  Now you've got a nice headless RPi!

Next you'll want to update the repositories on your Raspbian install by running `sudo apt-get update` followed by `sudo apt-get upgrade`.  At this stage you'll want to download the web browser we'll be using, **Chromium** by executing `sudo apt-get install chromium`.

Now, if you're using the same parts as me, you'll be ablle to hook up your display.  I followed [this video](https://www.youtube.com/watch?v=tK-w-wDvRTg) and the install was generally smooth (note I used USB power instead of the jumper cables).

*Now to configure the OS for the very important purpose of displaying Gifs 24/7.*

First you'll want to run `sudo raspi-config` to set a few options there.  You'll want to overclock your Pi as high as possible.  If you've got a Pi2 the choice is easy (the Pi2 setting).  For previous Pis you'll generally be safe with overclocking but it'll require some trial and error to dial in the exact right settings for your purposes.  In the `raspi-config` application you'll also want to make sure you **boot to desktop**.

Next, we're going to edit the LX Desktop Autostart file. `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`.  This file runs each time the x server is started.

You'll want to comment out everything that is already in the file and add these lines to the top:
```
@xset s noblank
@xset s off
@xset -dpms
```
These lines should ensure that 'screen blanking' does not occur.  You might need to also install **xset**, a utility to control some settings of x `sudo apt-get install x11-xserver-utils`.

Next you'll be adding a line to start the Chromium browser in kiosk (fullscreen) mode, pointed to the website you've set up.  Mine looks like this:
`@chromium --kiosk www.kershner.org/pi_display`

The final step will be to set your resolution and tweak your overscan settings.  These can be located in the **boot.txt** file, so open it up with `sudo nano /boot/config.txt`.  Here you'll want to play with the `FRAMEBUFFER_HEIGHT` and `FRAMEBUFER_WIDTH` settings to set a comfortable resolution.  Mine is currently set to **240x400** which is insanely small, but allows for very smooth gif playback.  If the picture doesn't take up your whole screen (black bars) or if it bleeds off the edge of the screen you'll need to tweak the overscan settings in a very tedious trial and error way.

That's about all there is to it.  One extra step I might recommend is to set up a [cron](https://en.wikipedia.org/wiki/Cron) job to periodically reboot the device or at the very least refresh the Chromium session in case of some error preventing the gif feed from continuing.
