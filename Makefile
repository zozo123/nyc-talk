SHELL := /bin/sh
.PHONY: all clean
all:
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
clean:
	rm -rf build
