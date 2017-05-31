import six


class ImageDetail(object):
    """
        A representation of server image details. This is typically the build image or template used to deploy a server. It contains information about the OS, architecture etc.

        Args:
            id (str): id, e.g. "ami-abcdef"
            name (str): name, e.g. "Ubuntu Linux 16.04 LTS 64 bit"
            type (str): ``Windows`` or ``Linux``
            distribution (str): distribution or subtype, e.g. ``Server 2012`` or ``CentOS``
            version (str): version e.g. ``V2`` or ``16.04.1``
            architecture (str): architecture e.g ``i386``, ``x86_64``

    """  # noqa

    def __init__(self, id=None, name=None, type=None, distribution=None,
                 version=None, architecture=None):
        self._id = id
        self._name = name
        self._type = type
        self._distribution = distribution
        self._version = version
        self._architecture = architecture

        self._check_not_none_str_value('id', self._id)

    def _check_not_none_str_value(self, name, value):
        if value is None or not isinstance(value, six.string_types):
            raise ValueError('%s must be a string and have a value' % name)

    def serialize(self):
        """Serialize the contents"""

        return {
            "id": self._id,
            "name": self._name,
            "architecture": self._architecture,
            "distribution": self._distribution,
            "type": self._type,
            "version": self._version,
        }


class ImageDetailMap(object):
    """
        A utility class that is able to look up common server images used for several servers using a dict mapping ids to the details.

        Args:
            mapping (dict): A dict with str keys and tuple values

        Example:
            This shows initializing a mapping and looking up images::

                m = ImageDetailMap([
                    'ubuntu16': ('Ubuntu Linux 16.04 LTS 64 bit', 'Linux', 'Ubuntu', '16.04', 'x64'),
                    'w2012R2': ('Windows Server 2012R2 Standard', 'Windows', 'Server 2012', 'R2', 'x64'),
                ])

                m.get('no-match')                       # Returns an Image with None
                m.get('ubuntu16')                       # Matches the image with "ubuntu16"
                m.get('ubuntu16', architecture='i386')  # Matches the image with "ubuntu16" and overrides the architecture
    """  # noqa

    def __init__(self, mapping=None):
        self._mapping = mapping

    def get(self, id=None, name=None, version=None, type=None,
            architecture=None, distribution=None):
        """
            Lookup an image. If none is found, an image is returned with no data in it.
            Use the arguments to override individual details.

            Args:
                name (str): optional name
                type (str): optional type
                distribution (str): optional distribution
                version (str): optional version
                architecture (str): optional architecture

            Returns: :py:class:`nflex_connector_utils.image_detail.ImageDetail`
        """  # noqa

        mapped_image = self._mapping.get(id)
        if mapped_image is None:
            (mname, mtype, mdist, mversion, march) = tuple([None] * 5)
        else:
            (mname, mtype, mdist, mversion, march) = mapped_image

        mname = mname or name
        mtype = mtype or type
        mversion = mversion or version
        march = march or architecture
        mdist = mdist or distribution

        return ImageDetail(
            id=id,
            name=mname,
            type=mtype,
            distribution=mdist,
            version=mversion,
            architecture=march,
        )
