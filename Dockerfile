FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on
WORKDIR /app
RUN pip install --no-cache-dir poetry==2.1.3
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-root
COPY . .
RUN chmod +x /app/prestart.sh
ENTRYPOINT ["/app/prestart.sh"]
CMD ["python", "-m", "src.main"]