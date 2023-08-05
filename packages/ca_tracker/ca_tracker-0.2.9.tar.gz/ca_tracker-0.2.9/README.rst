Installation instructions for dzne compute server.
--tested on python version 2.7.7--
Christoph Moehl, christoph.moehl@dzne.de


1. Install x forwarding software on you client computer, e.g. http://xquartz.macosforge.org/landing/ (if not installed yet)

2. log in to one of the dzne compute servers e.g.
ssh -Y compute-04.dzne.de

3. load the python module
module load python

4. install virtualenv in your home directory (if not installed yet)
easy_install -d /home/[username]/.python27 --user virtualenv

5. cerate a project directory and a new virtual environment (here with name venv - other names are possible)
mkdir my_project
cd my_project
/home/[username]/.local/bin/virtualenv venv 

6. activate the virtual environment and install python packages numpy, six, pandas ans scipy
source venv/bin/activate
pip install numpy==1.8.1
pip install six
pip install pandas
pip install scipy

7. finally install ca_tracker
pip install ca_tracker

8. edit the file config.json to set the analysis parameters

9. now you can run ca_tracker_1 and ca_tracker_2



you can check what modules are already installed with the command
pip freeze


