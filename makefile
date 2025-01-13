
ifeq ($(OS),WINDOWS_NT)
	PY=python
endif

PY?=python3

MAIN=src/main.py
TESTSCR=src/tests.py
TEST_PATH=tests
BUILD_PATH=build
ZIP_PATH=entrega.zip

OPEN_PDF?=True

.PHONY: all tests clean zip clean-all latex probar ejecutar
.SILENT: all

all:
	 ${PY} ${MAIN}

tests:
	mkdir -p ${BUILD_PATH}
	${PY} ${TESTSCR} tests
	# ${PY} src/CParser.py
zip:
	zip ${ZIP_PATH} makefile src

clean:
	${RM} -rf ${BUILD_PATH} *.zip src/__pycache__/ *.pdf *.aux *.log
		find -type f -name '*~' -delete
	find -type f -name '#*#' -delete

ejecutar:
	${PY} src/CParser.py

probar:
	${PY} src/main.py tests/cosasc.c traducido.s

latex: traductor.pdf

traductor.pdf: documentacion/traductor.tex
	pdflatex $<
	evince $@ &

clean-all: clean
	${RM} *.txt *.out
	find -type f -name '*.out' -delete
