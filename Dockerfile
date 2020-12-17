FROM python:3
COPY . /tests/
WORKDIR /tests
RUN pip install -r requirements.txt
ENTRYPOINT python -m pytest --verbose vacancies_tests.py