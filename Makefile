setup:
	poetry install

gen_requirements:
	poetry export --without-hashes -f requirements.txt >requirements.txt

gen_requirements_dev:
	poetry export --without-hashes --dev -f requirements.txt >requirements-dev.txt

test:
	poetry run tox

run:
	docker build -t http_to_mqtt .
	docker run -e "BIND_PORT=3000" -p 3000:3000 http_to_mqtt
