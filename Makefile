SHELL := /bin/sh
.PHONY: all demo reference record deck snapshot clean
all: deck

demo:
	python3 lab/run.py --mode isolated --output build/evidence

reference:
	python3 lab/run.py --mode reference --output build/reference

record: demo
	mkdir -p evidence
	cp build/evidence/results.json evidence/results.json
	cp build/evidence/transcript.txt evidence/transcript.txt

# Recorded evidence must match the exact lab source before any slide build.
deck:
	python3 tools/evidence.py
	python3 tools/notes.py
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex

snapshot: deck
	cp build/talk.pdf slides/talk.pdf

clean:
	rm -rf build
