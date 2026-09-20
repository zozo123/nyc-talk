SHELL := /bin/sh
.PHONY: all demo reference factory factory-boat test verify record record-factory deck snapshot clean
all: snapshot

demo:
	python3 lab/run.py --mode isolated --output build/evidence

reference:
	python3 lab/run.py --mode reference --output build/reference

factory:
	python3 -m factory.run --output build/factory

factory-boat:
	python3 -m factory.run --boat --output build/factory

test:
	python3 -m unittest discover -s tests -v

verify: test
	python3 tools/evidence.py

record: demo
	mkdir -p evidence
	cp build/evidence/results.json evidence/results.json
	cp build/evidence/transcript.txt evidence/transcript.txt

record-factory: factory
	mkdir -p evidence
	cp build/factory/results.json evidence/factory-results.json
	python3 -c "import json,pathlib; d=json.loads(pathlib.Path('build/factory/local.json').read_text()); t=['MODE local / STATUS '+d['status']]+[c['status']+' '+c['check']+': '+c['detail'] for c in d['checks']]; pathlib.Path('evidence/factory-transcript.txt').write_text('\n'.join(t)+'\n')"

deck:
	python3 tools/evidence.py
	node tools/build_deck.js
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex

snapshot: deck
	cp build/talk.pdf slides/talk.pdf
	cp build/talk.pptx slides/talk.pptx
	python3 tools/replay.py verifier --html demo/replay.html

clean:
	rm -rf build factory/store
