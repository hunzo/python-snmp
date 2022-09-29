from pysnmp import hlapi


class SNMP:
    def construct_object_types(self, list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types

    def cast(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    def fetch(self, handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(
                    handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = self.cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError(
                        'Got SNMP error: {0}'.format(error_indication))
            except StopIteration:
                break
        return result

    def get(self, target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *self.construct_object_types(oids)
        )
        return self.fetch(handler, 1)[0]

    def get_bulk(self, target, oids, credentials, count, start_from=0, port=161,
                 engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.bulkCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            start_from, count,
            *self.construct_object_types(oids)
        )
        return self.fetch(handler, count)

    def get_bulk_auto(self, target, oids, credentials, count_oid, start_from=0, port=161,
                      engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        count = self.get(target, [count_oid], credentials,
                         port, engine, context)[count_oid]
        return self.get_bulk(target, oids, credentials, count, start_from, port, engine, context)
