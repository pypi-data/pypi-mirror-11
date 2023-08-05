> This fork contains one script, at /notebook/static/notebook/js/dsten.js. With this script, Simple Mode is the default; click on the "Simple Mode" button to toggle this mode on/off. The following describes special features, in Simple Mode.
- By default, shift-enter runs all cells.
- Only one mode -- edit mode -- exists, for simplicity.
- "Scratch cell" available as a sandbox environment to-go.

# Jupyter Notebook

The Jupyter HTML notebook is a web-based notebook environment for interactive computing.

Dev quickstart:

* Create a virtual env (ie jupyter-dev)
* ensure that you have node/npm installed (ie brew install node on OS X)
* Clone this repo and cd into it
* pip install -r requirements.txt -e .

_NOTE_: For Debian/Ubuntu systems, if you're installing the system node you need
to use the 'nodejs-legacy' package and not the 'node' package.

Launch with:

    jupyter notebook

For Ubuntu Trusty:
```
sudo apt-get install nodejs-legacy npm python-virtualenv python-dev
python2 -m virtualenv ~/.virtualenvs/notebook
source ~/.virtualenvs/notebook/bin/activate
pip install --upgrade setuptools pip
git clone https://github.com/jupyter/notebook.git
cd notebook
pip install -r requirements.txt -e .
jupyter notebook
```

