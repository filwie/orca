from orca.topology.probes.k8s import probe
from orca.k8s import client as k8s_client
from orca.topology.probes.k8s import linker
from orca.common import logger

log = logger.get_logger(__name__)


class ReplicaSetProbe(probe.K8SProbe):

    def run(self):
        log.info("Starting K8S watch on resource: replica_set")
        watch = k8s_client.ResourceWatch(self._client.ExtensionsV1beta1Api(), 'replica_set')
        watch.add_handler(ReplicaSetHandler(self._graph))
        watch.run()


class ReplicaSetHandler(probe.K8SHandler):

    def _extract_properties(self, obj):
        id = obj.metadata.uid
        properties = {}
        properties['name'] = obj.metadata.name
        properties['namespace'] = obj.metadata.namespace
        properties['replicas'] = obj.spec.replicas
        return (id, 'replica_set', properties)


class ReplicaSetToDeploymentLinker(linker.K8SLinker):

    def _are_linked(self, replica_set, deployment):
        match_namespace = self._match_namespace(replica_set, deployment)
        match_selector = self._match_selector(replica_set, deployment.spec.selector.match_labels)
        return match_namespace and match_selector

    @staticmethod
    def create(graph, client):
        return ReplicaSetToDeploymentLinker(
            graph,
            'replica_set', k8s_client.ResourceAPI(client.ExtensionsV1beta1Api(), 'replica_set'),
            'deployment', k8s_client.ResourceAPI(client.AppsV1Api(), 'deployment'))