.PHONY: help install migrate run test clean docker-build docker-up docker-down format lint

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make migrate       - Run database migrations"
	@echo "  make run           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean up temporary files"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Run linters"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

run:
	python manage.py runserver

test:
	pytest

test-coverage:
	pytest --cov=apps --cov=core --cov-report=html

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage

docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

docker-clean:
	docker-compose down -v

format:
	black apps/ core/ config/
	isort apps/ core/ config/

lint:
	flake8 apps/ core/ config/
	pylint apps/ core/ config/

superuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput
