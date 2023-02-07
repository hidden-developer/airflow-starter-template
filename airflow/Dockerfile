FROM apache/airflow:2.5.1-python3.8

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get install -y python3-dev libffi-dev openssl default-libmysqlclient-dev gcc git g++ \
  && apt-get -y install cmake \
  && apt-get install -y libgomp1

RUN usermod -g root airflow

ARG DIR_PATH=/opt/airflow
WORKDIR ${DIR_PATH}
USER airflow

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN $(which pip) install --user -r requirements.txt

COPY --chown=airflow:root libs ${DIR_PATH}/libs
COPY --chown=airflow:root dags ${DIR_PATH}/dags
COPY --chown=airflow:root logs ${DIR_PATH}/logs
COPY --chown=airflow:root plugins ${DIR_PATH}/plugins
COPY --chown=airflow:root configs ${DIR_PATH}/configs
COPY --chown=airflow:root airflow.cfg ${DIR_PATH}/airflow.cfg
COPY --chown=airflow:root webserver_config.py ${DIR_PATH}/webserver_config.py

ENV PYTHONPATH "${DIR_PATH}"

CMD ["airflow"]
