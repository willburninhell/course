HOST=0.0.0.0
PORT=8000
-include Makefile.def
APPS=core

test:
		python manage.py test $(APPS)

cleanpyc:
		rm -f *.pyc */*.pyc

syncdb:
		python manage.py syncdb --noinput

run:
		python manage.py runserver $(HOST):$(PORT)