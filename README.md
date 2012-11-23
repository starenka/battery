## battery

Battery is a simple sampler (or rompler if you wish) you can control only with keyboard. In fact only with couple keys. The goal was to have something to play samples I can control on a headless machine (I'm using [Rasberry Pi](http://www.raspberrypi.org/) and [MakeyMakey](http://www.makeymakey.com/) to control it right now). The philosophy is quite straightforward. Get some samples, copy them into samples directory and stick them into banks config file (see `banks` directory). You can specify as many banks as you want. Once you're ready, fire up battery with your custom bank file: `python battery.py -b my_bank.json` or just do `python battery.py` to use default one.

Once you've started the sampler use `a`, `s`, `d`, `f`, `g`, `h`, `j` and `arrow keys` to play the samples and `space` to rotate defined banks. Know what? Now you can record what you play by pressing `r`. Once you're finished, press `r` again to stop recording. You can do this multiple times and layer your loops on top of previous ones. To delete the last loop press `p`. Yes, so it almost works like Kaossilator's loops when using `FIX`. You can use `w` to toggle reverse mode on samples (not loops). To close the sampler press `q` or `ESC`.

I've bundled Kawai XD-5 drum samples from Hydrogen, you can get more free samples by runing `get_samples.sh` script. It expects you to have wget and rar binaries on your system.

More or less current screenshot:

 ![screenshot](http://junk.starenka.net/battery03.jpg)

This is how the drums would look like if use something you normally have at home: tinfoil and cardboard ;)

 ![drums](http://farm9.staticflickr.com/8470/8123065467_61eb2f3be3.jpg)

To check it in action (captured screen video, with bad sound and even worse music), click this [video](http://www.youtube.com/watch?v=Bm0dp61zsxE)....
