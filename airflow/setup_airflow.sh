# copy .env.example
cp .env.example .env

# first line AIRLFOW_UID
sed -i "2s/.*/AIRFLOW_UID=$(id -u)/g" .env
