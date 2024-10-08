
ifeq ($(OS),WINDOWS_NT)
	PY=python
endif

PY?=python3

.PHONY: all tests clean

all:
	 ${PY} src/main.py

clean:
	${RM} build
