# Artemis

Artemis is an OIC social media network forked from Reddit R2. We plan to switch the backend over to Lemmy soon.

# Installation

You will need Ubuntu 14.04 Trusty Tahr (nothing older, nothing newer). We recommend you use a Docker image of Trusty Tahr running on a modern system to avoid any security vulnerabilities that might stem from running such an old system in production. Download the source, make the /home/src folder, dump all the stuff from this repo in that folder, run artemis/install-artemis.sh as superuser, and then change the artemis/r2/run.ini symlink to point at development.ini instead of production.ini (if you're only devving). After that set up your hosts to make artemis.local point to your running server, and navigate to that URL in your browser, congrats, you have Artemis up and working.

To make changes not in the /r2/r2/public/static folder, you will need to rebuild. Run `sudo make` in /r2/ after you've made your modifications, and then run `sudo artemis-restart`.

# Disclaimer

We do not make any claims about the security or reliability of this software and we are not liable if you get hacked. Portions of this code and assets are (C) 2005-2015 reddit Inc. If you find a vulnerability or you have something else to tell us, please contact artemis@cocaine.ninja for assistance or ethical disclosure.
