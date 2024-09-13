unit-test:
	pytest tests/unit --cov=src --cov-report=term --cov-report=html --cov-report=xml --html=htmlcov/report.html
int-test:
	pytest tests/integration --cov=src --cov-report=term --cov-report=html --cov-report=xml --html=htmlcov/report.html
test:
	pytest tests --cov=src --cov-report=term --cov-report=html --cov-report=xml --html=htmlcov/report.html
install:
	pip install .
install-dev:
	pip install -r tests/test-requirements.txt -r requirements-dev.txt .
start-cov-server:
	python -m http.server -d htmlcov 8080
docs:
	pdoc ./src
