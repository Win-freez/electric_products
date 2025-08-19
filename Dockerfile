FROM python:3.12-slim
ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on
WORKDIR app/
RUN pip install --no-cache-dir poetry==2.1.3
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main
COPY . /app
CMD ["python", "-m", "src.main"]
