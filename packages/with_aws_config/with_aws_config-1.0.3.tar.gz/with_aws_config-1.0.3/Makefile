.PHONY: build clean publish lint preview

build:
	python setup.py sdist

clean:
	rm -rf MANIFEST dist *.pyc

publish: clean build
	twine upload dist/with_aws_config-*.tar.gz

lint:
	pylint *.py

dist/README.html: README.rst
	# requires pip install docutils
	mkdir -p dist
	python setup.py --long-description | rst2html.py > dist/README.html

preview: dist/README.html
	open dist/README.html
