import contextlib
import typing

from dask_kubernetes import InCluster, KubeCluster, make_pod_spec
from kubernetes.client import V1Pod

DEFAULT_IMAGE = "ghcr.io/dask/dask:latest"
DEFAULT_MEM_LIMIT_SCHEDULER = "4G"
DEFAULT_MEM_LIMIT_WORKER = "2G"
DEFAULT_CPU_REQUESTED = 1
DEFAULT_NODE_POOL = "default-node-pool"
DEFAULT_NODE_POOL_SCHEDULER = "highmem-node-pool"
DEFAULT_NODE_POOL_WORKER = "spot-compute-node-pool"
DEFAULT_SA_NAME = "dask-gcs"
DEFAULT_ENV = {
    "PREFECT_API_URL": "http://prefect.orchestration.svc.cluster.local:4200/api",
    "MLFLOW_TRACKING_URI": "http://mlflow.tracking.svc.cluster.local:5001",
}


class DefaultSpec:
    def __init__(
        self,
        image: str = DEFAULT_IMAGE,
        memory_limit: str = DEFAULT_MEM_LIMIT_WORKER,
        cpu_request: int = DEFAULT_CPU_REQUESTED,
        node_pool: str = DEFAULT_NODE_POOL,
        service_account_name: str = DEFAULT_SA_NAME,
        env: typing.Dict[str, typing.Any] = DEFAULT_ENV,
    ):
        self.image = image
        self.memory_limit = memory_limit
        self.cpu_request = cpu_request
        self.node_pool = node_pool
        self.service_account_name = service_account_name
        self.env = env

    def generate(self) -> V1Pod:
        return make_pod_spec(
            image=self.image,
            memory_limit=self.memory_limit,
            cpu_request=self.cpu_request,
            extra_pod_config={
                "nodeSelector": {"node_pool": self.node_pool},
                "serviceAccountName": self.service_account_name,
            },
            env=self.env,
        )


class SchedulerSpec(DefaultSpec):
    def __init__(
        self,
        image: str = DEFAULT_IMAGE,
        memory_limit: str = DEFAULT_MEM_LIMIT_SCHEDULER,
        cpu_request: int = DEFAULT_CPU_REQUESTED,
        node_pool: str = DEFAULT_NODE_POOL_SCHEDULER,
        service_account_name: str = DEFAULT_SA_NAME,
        env: typing.Dict[str, typing.Any] = DEFAULT_ENV,
    ):
        super().__init__(
            image, memory_limit, cpu_request, node_pool, service_account_name, env
        )


class WorkerSpec(DefaultSpec):
    def __init__(
        self,
        image: str = DEFAULT_IMAGE,
        memory_limit: str = DEFAULT_MEM_LIMIT_WORKER,
        cpu_request: int = DEFAULT_CPU_REQUESTED,
        node_pool: str = DEFAULT_NODE_POOL_WORKER,
        service_account_name: str = DEFAULT_SA_NAME,
        env: typing.Dict[str, typing.Any] = DEFAULT_ENV,
    ):
        super().__init__(
            image, memory_limit, cpu_request, node_pool, service_account_name, env
        )


@contextlib.contextmanager
def ephemeral_dask_cluster(
    scheduler_pod_spec: SchedulerSpec, worker_pod_spec: WorkerSpec
):

    cluster = KubeCluster(
        pod_template=worker_pod_spec,
        scheduler_pod_template=scheduler_pod_spec,
        auth=InCluster(),
        namespace="orchestration",
        n_workers=5,
    )

    try:
        yield cluster
    finally:
        cluster.close()
