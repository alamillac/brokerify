export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_DEBUG=1
export FLASK_ENV=development
export FLASK_APP=web/api/__init__.py
flask run
