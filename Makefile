SHELL := /bin/sh
.PHONY: all test factory demo isolated record record-factory author deck pptx snapshot clean
all: deck

test:
	python3 -m unittest discover -s tests -v
factory:
	python3 -m factory.run --output build/factory-local
demo:
	python3 lab/run.py --mode isolated --output build/evidence
isolated: demo
	python3 -m factory.run --isolated --output build/factory
record: isolated
	mkdir -p evidence
	cp build/evidence/results.json evidence/results.json
	cp build/evidence/transcript.txt evidence/transcript.txt
	cp build/factory/results.json evidence/factory-results.json
	cp build/factory/transcript.txt evidence/factory-transcript.txt
record-factory:
	python3 -m factory.run --isolated --output build/factory
	cp build/factory/results.json evidence/factory-results.json
	cp build/factory/transcript.txt evidence/factory-transcript.txt
# Authoring changes the shared geometry/content and requires npm install.
# Recompiling the checked-in Beamer source requires only TeX + Python.
author:
	node slides/build.js
	python3 tools/author.py
deck:
	python3 tools/evidence.py
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
pptx:
	node slides/build.js
snapshot: deck
	cp build/talk.pdf slides/talk.pdf
clean:
	rm -rf build factory/store
