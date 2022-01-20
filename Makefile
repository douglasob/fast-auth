RUN = poetry run

.PHONY: tests pep8 publish all

tests:
	${RUN} pytest -vs

pep8:
	${RUN} isort .
	${RUN} blue .

publish:
	poetry publish --build


all: pep8 tests publish