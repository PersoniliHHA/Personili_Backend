
# define an alias for the specfic python version used in this file.
FROM python:3.12-slim as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production
ARG REQUIREMENTS_FILE_NAME=requirements-local

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY requirements/${REQUIREMENTS_FILE_NAME}.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels  \
  -r ${REQUIREMENTS_FILE_NAME}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy the application code to the WORKDIR
COPY --chown=django:django . ${APP_HOME}


# copy application code to WORKDIR
#COPY --from=client-builder --chown=django:django ${APP_HOME} ${APP_HOME}


# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

#COPY --chown=django:django ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod u+x entrypoint.sh

USER django

 # COPY --chown=django:django ./start.sh .
 # RUN sed -i 's/\r$//g' ./start.sh
 # RUN chmod +x ./start.sh

ENTRYPOINT ["/app/entrypoint.sh"]
