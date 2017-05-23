import six


class ImageDetail(object):
    def __init__(self, id=None, name=None, type=None, distribution=None,
                 version=None, architecture=None):
        self.id = id
        self.name = name
        self.type = type
        self.distribution = distribution
        self.version = version
        self.architecture = architecture

        self._check_not_none_str_value('id', self.id)

    def _check_not_none_str_value(self, name, value):
        if value is None or not isinstance(value, six.string_types):
            raise ValueError('%s must be a string and have a value' % name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "architecture": self.architecture,
            "distribution": self.distribution,
            "type": self.type,
            "version": self.version,
        }


class ImageDetailMap(object):
    def __init__(self, mapping=None):
        self.mapping = mapping

    def get(self, id=None, name=None, version=None, type=None,
            architecture=None):
        mapped_image = self.mapping.get(id)
        if mapped_image is None:
            (mname, mtype, mdist, mversion, march) = tuple([None] * 5)
        else:
            (mname, mtype, mdist, mversion, march) = mapped_image

        mname = mname or name
        mtype = mtype or type
        mversion = mversion or version
        march = march or architecture

        return ImageDetail(
            id=id,
            name=mname,
            type=mtype,
            distribution=mdist,
            version=mversion,
            architecture=march,
        )
