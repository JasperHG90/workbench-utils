import typing

from google.cloud import secretmanager


class SecretAccessor:
    def __init__(self, project_id: str):
        self._project_id = project_id

    def get_secret(
        self, secret_id: str, version_id: typing.Union[str, int] = "latest"
    ) -> str:
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the secret version.
        name = f"projects/{self._project_id}/secrets/{secret_id}/versions/{version_id}"
        # Access the secret version.
        response = client.access_secret_version(name=name)
        # Return the decoded payload.
        return response.payload.data.decode("UTF-8")
