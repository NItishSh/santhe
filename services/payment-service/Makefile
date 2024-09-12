.PHONY: all clean test lint run build docker

all: clean test lint run

clean:
	rm -rf .mypy_cache .pytest_cache dist build *.egg-info
	find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf

test:
	pytest tests/

lint:
	mypy src/
	black src/ tests/
	isort src/ tests/

run:
	uvicorn main:app --reload

build:
	python setup.py sdist bdist_wheel

docker:
	docker build -t payment-service .
	docker run -p 8000:8000 payment-service

format:
	black src/ tests/
	isort src/ tests/

check-format:
	black --check src/ tests/
	isort --check-only src/ tests/
