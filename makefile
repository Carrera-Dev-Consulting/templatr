unit-test:
	pytest tests/unit --cov=src --cov-report=term --cov-report=html --cov-report=xml
int-test:
	pytest tests/integration --cov=src --cov-report=term --cov-report=html --cov-report=xml
install:
	pip install .
install-dev:
	pip install -r tests/test-requirements.txt -r requirements-dev.txt .

