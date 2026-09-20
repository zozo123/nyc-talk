SHELL := /bin/sh
.PHONY: all test verify demo reference factory http factory-boat record record-factory record-http deck pptx snapshot clean
all: deck

test:
	python3 -m unittest discover -s tests -v

# Fixtures only. No cloud or model calls. Not an arbitrary-code sandbox.
verify: test factory http
	python3 tools/evidence.py

demo:
	python3 lab/run.py --mode isolated --output build/evidence

reference:
	python3 lab/run.py --mode reference --output build/reference

factory:
	python3 -m factory.run --output build/factory

http:
	python3 -m factory.http_demo --output build/http

factory-boat:
	python3 -m factory.run --boat --output build/factory

record: demo
	mkdir -p evidence
	cp build/evidence/results.json evidence/results.json
	cp build/evidence/transcript.txt evidence/transcript.txt

record-factory: factory
	mkdir -p evidence
	cp build/factory/results.json evidence/factory-results.json
	python3 -c "import json,pathlib; d=json.loads(pathlib.Path('build/factory/local.json').read_text()); t=['MODE local / STATUS '+d['status']]+[c['status']+' '+c['check']+': '+c['detail'] for c in d['checks']]; pathlib.Path('evidence/factory-transcript.txt').write_text('\n'.join(t)+'\n')"

record-http: http
	mkdir -p evidence
	cp build/http/results.json evidence/http-results.json
	cp build/http/transcript.txt evidence/http-transcript.txt

deck:
	python3 tools/evidence.py
	python3 tools/build_deck.py
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex

pptx:
	python3 tools/evidence.py
	node tools/build_deck.js

snapshot: deck pptx
	cp build/talk.pdf slides/talk.pdf
	cp build/talk.pptx slides/talk.pptx

clean:
	rm -rf build factory/store
