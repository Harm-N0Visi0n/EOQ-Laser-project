FROM python:3.14-slim
WORKDIR /app
RUN pip install poetry --quiet
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "fastapi", "run", "main.py", "--port", "8000"]
