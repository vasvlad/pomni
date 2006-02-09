PYTHON=python

clean:
	find -name *.pyc -exec rm {} \;
	rm -rf build dist gtktest.tar.gz MANIFEST

dist: clean
	./setup.py sdist

test:
	PYTHONPATH=. ${PYTHON} examples/tests.py
	for f in `ls gtktest/tests/test_*.py`; do \
		PYTHONPATH=. ${PYTHON} $$f; \
	done

.PHONY: clean dist test
