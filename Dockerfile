FROM apache/airflow
FROM python:3.7-bullseye

ADD requirements.txt .
USER root
ADD requirements.txt .
USER root
RUN /bin/bash -o pipefail -o errexit -o nounset -o nolog -c \
  "apt-get update \
  && apt-get install -y --no-install-recommends \
     gcc \
     heimdal-dev \
     procps \
     openjdk-11-jdk \
     ant \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*"


ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64
RUN export JAVA_HOME

RUN pip install --no-cache-dir -r requirements.txt

CMD ["webserver"]