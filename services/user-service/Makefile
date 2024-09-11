.PHONY: run
run:
	uvicorn src.main:app --reload

.PHONY: test
test:
	pytest -v

.PHONY: lint
lint:
	flake8 . && black .

.PHONY: build
build:
	docker build -t user-service .

.PHONY: run-docker
run-docker:
	docker run -p 8000:8000 user-service
