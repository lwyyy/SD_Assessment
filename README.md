# SD_Assessment
Software Development Assessment Part 3
This application is a squad roster builder for a tabletop miniatures skirmish game, a type of war game.
This code is a new version of the application.

# Running notes
We run this code on MacOS environment.
This code requires Python and Flask, so users needs to install them before running it.
MacOS has python 2.7 originally, so users needn't to install python.
Flask and other packages can be installed using a package manager such as pip.

The steps to install virtualenv tool and flask:
1. open a terminal
2. input: sudo easy_install pip
3. input: sudo pip install virtualenv
4. input: mkdir FGWarband
5. input: cd FGWarband
6. input: virtualenv venv
7. activate virtualenv, input: source venv/bin/activate 
8. input: pip install flask

Then clone this repository into the virtual environment (FGWarband folder) using command: 
git clone https://github.com/lwyyy/SD_Assessment.git

Next, go into SD_Assessment folder under the FGWarband folder and run the code using command: 
python framewrok.py

This should result in the following line being displayed:
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

After that, using a browser navigate to http://localhost:5000/ to see the application interface.

Notes: 
 * Stop running the website using "CTRL+C" in the terminal
 * Deactivate virtualenv using command: deactivate
