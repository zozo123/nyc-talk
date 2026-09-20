SHELL := /bin/sh
.PHONY: all test demo reference factory factory-isolated factory-boat record record-factory record-isolated record-all evidence deck snapshot pptx replay replay-html verify clean
all: deck

test:
	python3 -m unittest discover -s tests -v

demo:
	python3 lab/run.py --mode isolated --output build/evidence

reference:
	python3 lab/run.py --mode reference --output build/reference

# These local fixture subprocesses provide no OS isolation.
factory:
	python3 -m factory.run --output build/factory

factory-isolated:
	python3 -m factory.isolated --output build/isolated-factory

# Optional; never used by the deck build. A non-PASS result exits nonzero.
factory-boat:
	python3 -m factory.run --boat --output build/factory

record: demo
	mkdir -p evidence
	cp build/evidence/results.json evidence/results.json
	cp build/evidence/transcript.txt evidence/transcript.txt

record-factory: factory
	cp build/factory/results.json evidence/factory-results.json
	python3 -c "import json,pathlib; d=json.loads(pathlib.Path('build/factory/local.json').read_text()); t=['MODE local / STATUS '+d['status']]+[c['status']+' '+c['check']+': '+c['detail'] for c in d['checks']]; pathlib.Path('evidence/factory-transcript.txt').write_text('\n'.join(t)+'\n')"

record-isolated: factory-isolated
	cp build/isolated-factory/results.json evidence/isolated-factory.json
	cp build/isolated-factory/transcript.txt evidence/isolated-factory-transcript.txt

record-all: record record-factory record-isolated
	python3 tools/audit_baseline.py
	python3 tools/evidence.py

evidence:
	python3 tools/evidence.py

# No cloud access or experiment execution. Record first after any factory edit.
deck: evidence
	python3 tools/build_deck.py
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build slides/talk.tex
	! grep -q 'Overfull' build/talk.log

snapshot: deck pptx replay-html
	cp build/talk.pdf slides/talk.pdf
	cp build/nyc-talk.pptx slides/talk.pptx

pptx: evidence
	node slides/build_pptx.js

verify: test evidence

replay-html: evidence
	python3 tools/replay.py --html demo/replay.html

replay: evidence
	python3 tools/replay.py

clean:
	rm -rf build factory/store
