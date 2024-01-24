FROM python:3.11-slim


RUN apt update && apt install -y \
  build-essential \
  curl \
  locales \
  wget


RUN addgroup --system app && adduser --system --group app --home /app

# Some programs don't like the default C.UTF-8 locale, make sure we'en en_US UTF-8
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:UTF-8
ENV LC_ALL=en_US.UTF-8

USER app

WORKDIR /app
RUN chown app:app .
USER app

RUN pip install poetry

COPY --chown=app:app . /app


RUN python -m poetry install --only main --no-root

ENV DJANGO_SECRET_KEY=s3cr3t
ENV PYTHONUNBUFFERED=true

EXPOSE 8000
CMD ["python", "-m", "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
