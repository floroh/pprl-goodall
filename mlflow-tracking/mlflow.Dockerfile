FROM python:3.12-trixie
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install mlflow[auth]==3.12.0 psycopg2-binary boto3
COPY user_setup.py /opt/user_setup.py