# Use to build modules

.PHONY: test clean doc doc3

all:
	@echo Targets: run git doc clean md5

#doc:
#	pdoc --logo /home/peterglen/pgpygtk/webserver/drawing.png \
#                -o doc `find . -maxdepth 2 -name  \*.py`

doc3:
	@pdoc3  --html --force -o doc3 `find . -maxdepth 2 -name  \*.py`

# Auto Checkin
ifeq ("$(AUTOCHECK)","")
AUTOCHECK=autocheck
endif

git:
	rm -f test/*
	git add .
	git commit -m "$(AUTOCHECK)"
	git push
	git push local

run:
	./mock_server.py

test:
	@make -C client test

hello:
	@make -C client hello

deb:  build build3
	./build-deb.sh

clean:
	./clean.sh

md5:
	echo doing md5













