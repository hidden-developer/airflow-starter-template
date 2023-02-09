# Airflow starter template

## Prerequisition

- Apache Airflow
- Docker
- docker-compose

## How to start

1. Run shell scripts for installing docker.
   support only linux version

   another OS, Follow [Docker Installation](https://docs.docker.com/engine/install/)

   ```bash

   bash install_docker.sh
   ```

2. Enter airflow directory

   ```bash
   cd airflow
   ```

3. Setup environment

   ```bash
   bash setup_airflow.sh
   ```

4. Fill in `.env`

5. Run docker-compose

   ```bash
   # initialize DB
   docker-compose -p project_name up airflow-init
   # Run Airflow
   docker-compose -p project_name up -d
   ```

6. Check your Airflow GUI

   [http://localhost:8080](http://localhost:8080)

7. Setup Airflow Settings

   - `[Admin] - [Connection]`: connect for Airflow and provider
     - Bigquery: Google Cloud(KeyFileJSON: service_account.json)
     - AWS: Amazon Web Services(AccessKeyId, SecretAccessKey, Extra: `{"region_name": "ap-northeast-2"}`)
     - MySQL: MySQL(Host, Schema, Login, Password, Port)

8. Write First DAG
   in `dags/` directory

## Q & A

1. How to add pip packages?
   add package name in `airflow/requirements.txt`

2. How to install OS level programs?
   modify `airflow/Dockerfile`
