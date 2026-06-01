import os

from dotenv import load_dotenv
from mlflow.exceptions import RestException, MlflowException
from mlflow.server import get_app_client
from mlflow.server.auth.client import AuthServiceClient

# Authenticate as admin with default password defined in auth_config.ini
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "password1234"
load_dotenv()

tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
auth_client: AuthServiceClient = get_app_client("basic-auth", tracking_uri=tracking_uri)

# Update admin password
admin_password = os.getenv("MLFLOW_ADMIN_PASSWORD")
if not admin_password:
    raise RuntimeError(f"MLFLOW_ADMIN_PASSWORD env variable is missing")
try:
    auth_client.update_user_password("admin", admin_password)
except MlflowException as e:
    print(f"Authentication failed, maybe the admin password was updated already?")
    raise e
os.environ["MLFLOW_TRACKING_PASSWORD"] = admin_password

# Create user
username = os.getenv("MLFLOW_USERNAME")
password = os.getenv("MLFLOW_PASSWORD")
try:
    user = auth_client.get_user(username)
    auth_client.update_user_password(username, password)
except RestException:
    user = auth_client.create_user(username, password)
    print(f"Created user: {user.username} (ID: {user.id})")

auth_client.update_user_admin(username, True)
