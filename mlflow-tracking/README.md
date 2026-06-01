# MLflow Tracking setup

```sh
cd mlflow-tracking
cp default.env .env
# Set passwords in .env
docker compose -f docker-compose.yml -f docker-compose-local.yml up -d
```

Update default admin password ([docs](https://www.mlflow.org/docs/latest/ml/auth/) and create new user
```sh
docker exec -t mlflow-server bash -c "cd /opt && python user_setup.py
```

Visit UI at [http://127.0.0.1:5000](http://127.0.0.1:5000)