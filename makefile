
ifeq ($(OS),WINDOWS_NT)
	PY=python
endif

PY?=python3

MAIN=src/main.py
TESTSCR=src/tests.py
TEST_PATH=tests
BUILD_PATH=build
ZIP_PATH=entrega.zip


.PHONY: all tests clean zip
.SILENT: all

all:
	 ${PY} ${MAIN}

tests:
	mkdir ${BUILD}
	${PY} ${TESTSCR} ${TEST_PATH}
zip:
	zip ${ZIP} makefile src

clean:
	${RM} ${BUILD} ${ZIP} *~
