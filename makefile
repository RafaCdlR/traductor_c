
ifeq ($(OS),WINDOWS_NT)
	PY=python
endif

PY?=python3

MAIN=src/main.py
BUILD=build
ZIP=entrega.zip


.PHONY: all tests clean zip

all:
	 ${PY} src/main.py

tests:
	mkdir ${BUILD}
	 makefile src
zip:
	zip ${ZIP} makefile src

clean:
	${RM} ${BUILD}
