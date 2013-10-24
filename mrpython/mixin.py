# -*- coding: utf-8 -*-


from datetime import datetime


class DictInterface(object):

    _dict_attrs = ()

    @property
    def as_dict(self):
        return self.to_dict()

    def to_dict(self, only=[], recursion=0, date_format='%Y-%m-%d %H:%M:%S'):

        def _obj_to_dict(o, limit=[]):
            names = o._dict_attrs or filter(
                lambda x: not x.startswith('_'), vars(o))
            if limit:
                names = list(set(limit).intersection(set(names)))
            return {k: getattr(o, k) for k in names}

        def _walk(o, path=[], prev=None, limit=[], level=0):
            c = {}
            d = _obj_to_dict(o, limit)

            if prev:
                path.append(prev)

            for attr, value in d.iteritems():
                if isinstance(value, DictInterface):
                    if path and (value is path[0]):
                        continue
                    if value is prev:
                        continue
                    if not recursion:
                        continue
                    if level == recursion:
                        continue
                    c[attr] = _walk(value, path, o, level=level + 1)
                elif hasattr(value, '__iter__'):
                    c[attr] = [_walk(v, path, o, level=level + 1)
                               for v in value]
                elif isinstance(value, datetime):
                    c[attr] = value.strftime(date_format)
                else:
                    c[attr] = value
            return c

        return _walk(self, limit=only)
