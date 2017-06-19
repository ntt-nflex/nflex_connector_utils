from . import Resource


class ComputePool(Resource):
    """
        A representation of a compute pool.

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            cpu_hz (int): cpu in Hz (optional)
            memory_b (int): memory in bytes (optional)
            storage_b (int): storage in bytes (optional)
            billing_tag (str): billing tag for the compute pool (optional)
    """  # noqa

    def __init__(self, cpu_hz=None, memory_b=None, storage_b=None,
                 billing_tag=None, **kwargs):
        super(ComputePool, self).__init__(type='compute_pool', **kwargs)
        self._cpu_hz = cpu_hz
        self._memory_b = memory_b
        self._storage_b = storage_b
        self._billing_tag = billing_tag

    def serialize(self):
        """Serialize the contents"""

        data = super(ComputePool, self).serialize()
        data['details'] = {
            self.type: {
                "cpu_hz": self._cpu_hz,
                "memory_b": self._memory_b,
                "storage_b": self._storage_b,
                "billing_tag": self._billing_tag
            }
        }
        return data
