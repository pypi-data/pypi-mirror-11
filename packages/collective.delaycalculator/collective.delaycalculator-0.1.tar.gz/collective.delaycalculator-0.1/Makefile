#!/usr/bin/make
#
all: run

bootstrap.py:
	wget http://downloads.buildout.org/2/bootstrap.py

.PHONY: bootstrap buildout run test cleanall
bootstrap: bootstrap.py
	virtualenv-2.7 .
	./bin/python bootstrap.py

buildout:
	if ! test -f bin/buildout;then make bootstrap;fi
	bin/buildout

run:
	if ! test -f bin/instance;then make buildout;fi
	bin/instance fg

test:
	if ! test -f bin/test;then make buildout;fi
	bin/test

cleanall:
	rm -fr bin develop-eggs htmlcov include .installed.cfg lib .mr.developer.cfg parts downloads eggs
