import sys
from collections import OrderedDict

import arduino_rpc.proxy as ap
from nadamq.NadaMq import cPacket, PACKET_TYPES


class ProxyBase(ap.ProxyBase):
    def __init__(self, serial, buffer_bounds_check=True):
        self._serial = serial
        self._buffer_bounds_check = buffer_bounds_check
        self._buffer_size = None

    def help(self):
        '''
        Open project webpage in new browser tab.
        '''
        import webbrowser

        url = self.properties().get('url')
        if url:
            webbrowser.open_new_tab(url)

    def properties(self):
        import pandas as pd

        return pd.Series(OrderedDict([(k, getattr(self, k)().tostring())
                                      for k in ['base_node_software_version',
                                                'name', 'manufacturer', 'url',
                                                'software_version']
                                      if hasattr(self, k)]))

    @property
    def buffer_size(self):
        if self._buffer_size is None:
            self._buffer_bounds_check = False
            payload_size_set = False
            try:
                max_i2c_payload_size = self.max_i2c_payload_size()
                payload_size_set = True
            except AttributeError:
                max_i2c_payload_size = sys.maxint
            try:
                max_serial_payload_size = self.max_serial_payload_size()
                payload_size_set = True
            except AttributeError:
                max_serial_payload_size = sys.maxint
            if not payload_size_set:
                raise IOError('Could not determine maximum packet payload '
                              'size. Make sure at least one of the following '
                              'methods is defined: `max_i2c_payload_size` '
                              'method or `max_serial_payload_size`.')
            self._buffer_size = min(max_serial_payload_size,
                                    max_i2c_payload_size)
            self._buffer_bounds_check = True
        return self._buffer_size

    def _send_command(self, packet):
        if self._buffer_bounds_check and len(packet.data()) > self.buffer_size:
            raise IOError('Packet size %s bytes too large.' %
                          (len(packet.data()) - self.buffer_size))
        return super(ProxyBase, self)._send_command(packet)


class I2cProxyMixin(object):
    def __init__(self, i2c_address, proxy):
        self.proxy = proxy
        self.address = i2c_address

    def _send_command(self, packet):
        response = self.proxy.i2c_request(self.address,
                                          map(ord, packet.data()))
        return cPacket(data=response.tostring(), type_=PACKET_TYPES.DATA)
