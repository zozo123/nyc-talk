SHELL := /bin/sh
.PHONY: all demo reference factory factory-boat record record-factory deck snapshot clean
all: deck

demo:
	python3 lab/run.py --mode isolated --output build/evidence

reference:
	python3 lab/run.py --mode reference --output build/reference

# Local logic only. Does not provision machines.
factory:
	python3 -m factory.run --output build/factory

# Credentialed Boat accept-VM. Requires BOAT_API_KEY. Bounded TTL.
factory-boat:
	python3 -m factory.run --boat --output build/factory

record: demo
	mkdir -p evidence
	cp build/evidence/results.json evidence/results.json
	cp build/evidence/transcript.txt evidence/transcript.txt

record-factory: factory
	mkdir -p evidence
	cp build/factory/results.json evidence/factory-results.json
	python3 -c "import json,pathlib; p=pathlib.Path('build/factory/local.json'); d=json.loads(p.read_text()); t=['MODE local / STATUS '+d['status']]+[c['status']+' '+c['check']+': '+c['detail'] for c in d['checks']]; pathlib.Path('evidence/factory-transcript.txt').write_text('\n'.join(t)+'\n')"

# Recorded evidence must match lab and factory source before any slide build.
deck:
	python3 tools/evidence.py
	python3 tools/notes.py
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex

snapshot: deck
	cp build/talk.pdf slides/talk.pdf

clean:
	rm -rf build factory/store
