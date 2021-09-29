# Use to build modules

.PHONY: test clean doc

all:
	@echo Targets: run git doc clean md5

doc:
	pdoc --logo /home/peterglen/pgpygtk/webserver/drawing.png -o doc `find . -name \*.py`

git:
	git add .
	git commit -m auto
	git push
	#git push local

run:
	./wsgi_server.py

test:
	@make -C client test

hello:
	@make -C client hello

deb:  build build3
	./build-deb.sh

clean:

md5:
	echo duoing md5













