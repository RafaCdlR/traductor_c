
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
	mkdir -p ${BUILD_PATH}
	# ${PY} ${TESTSCR} tests ${BUILD_PATH}
	${PY} src/Cparser.py
zip:
	zip ${ZIP} makefile src

clean:
	${RM} -rf ${BUILD_PATH} ${ZIP} *~
	find -type f -name '*~' -delete
	find -type f -name '#*#' -delete
