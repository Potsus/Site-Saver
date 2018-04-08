# Site-Saver
A project to make wget's site downloading feature accessable to non tech-savy users. With a focus on downloading sites made with a site-builder like wordpress or squarespace

### the top 1m sites on the web according to alexa
we'll be using this lits to avoid trying to download what is obviously not a personal site
http://s3.amazonaws.com/alexa-static/top-1m.csv.zip

credentials should be stored in the `aws` folder
python requirements are in the `requirements.txt` file

install everything you need with `./install.sh install`
set up a blacklist with `./install.sh data`
run everything with `./install.sh run`