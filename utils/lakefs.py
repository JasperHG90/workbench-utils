import lakefs_client


def get_lakefs_configuration(
    lakectl_access_key: str, lakectl_secret_key: str, lakectl_host: str
) -> lakefs_client.configuration.Configuration:
    configuration = lakefs_client.Configuration()
    configuration.username = lakectl_access_key
    configuration.password = lakectl_secret_key
    configuration.host = lakectl_host
    return configuration


def get_storage_options(
    lakefs_configuration: lakefs_client.configuration.Configuration,
):
    return {
        "key": lakefs_configuration.username,
        "secret": lakefs_configuration.password,
        "client_kwargs": {
            "endpoint_url": lakefs_configuration.host,
        },
        "config_kwargs": {"s3": {"addressing_style": "path"}},
    }
