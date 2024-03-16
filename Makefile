# Use to build modules

.PHONY: test clean doc doc3

all:
	@echo Targets: run git doc clean md5

doc:
	#echo `find .  -maxdepth 2 -name  \*.py`
	#echo `find . -type d -maxdepth 2 `
	@#pdoc  --html --force -o doc3 `find . -maxdepth 2 -name  \*.py`
	./gendocs.py

# Auto Checkin
ifeq ("$(AUTOCHECK)","")
AUTOCHECK=autocheck
endif

git:
	rm -f test/*
	make clean
	git add .
	git commit -m "$(AUTOCHECK)"
	git push
	#git push local

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

# EOF
