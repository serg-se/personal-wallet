# Generate workable requirements.txt from Poetry dependencies
FROM python:3.10-slim-bullseye AS requirements

RUN pip install --no-cache-dir --upgrade poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without dev --without-hashes -o /requirements.txt

# Final app image
FROM python:3.10-alpine AS runtime

WORKDIR /app

# Install requirements
COPY --from=requirements /requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY src/ ./

ENTRYPOINT ["python", "-m", "personal_wallet"]