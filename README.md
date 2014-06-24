Octopress2Ghost
===============
This is a script for covert octopress posts into a ghost posts import .sql file. 

## Usage

1. This script require python markdown extension module, there is the installation guide: [python-Markdown](http://pythonhosted.org//Markdown/install.html)

2. Copy `exportToGhost.py' into your octopress root folder and run the scprit in terminal:

		./exportToGhost.py
	
	> remember to add permission for .py script

3. Then a file called `import.sql` will generate in this folder, just import it to your ghost service database.