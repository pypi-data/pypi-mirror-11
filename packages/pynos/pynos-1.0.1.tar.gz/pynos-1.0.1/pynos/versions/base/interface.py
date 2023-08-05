#!/usr/bin/env python
"""
Copyright 2015 Brocade Communications Systems, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import xml.etree.ElementTree as ET
import logging
import re

from ipaddress import ip_interface
from pynos.versions.base.yang.brocade_interface import brocade_interface
from pynos.versions.base.yang.brocade_rbridge import brocade_rbridge
import pynos.utilities


class Interface(object):
    """
    The Interface class holds all the actions assocaiated with the Interfaces
    of a NOS device.

    Attributes:
        None
    """
    def __init__(self, callback):
        """
        Interface init function.

        Args:
            callback: Callback function that will be called for each action.

        Returns:
            Interface Object

        Raises:
            None
        """
        self._callback = callback
        self._interface = brocade_interface(
            callback=pynos.utilities.return_xml
        )
        self._rbridge = brocade_rbridge(
            callback=pynos.utilities.return_xml
        )

    def add_vlan_int(self, vlan_id):
        """
        Add VLAN Interface. VLAN interfaces are required for VLANs even when
        not wanting to use the interface for any L3 features.

        Args:
            vlan_id: ID for the VLAN interface being created. Value of 2-4096.

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        vlinterface = ET.SubElement(config, 'interface-vlan',
                                    xmlns=("urn:brocade.com:mgmt:"
                                           "brocade-interface"))
        interface = ET.SubElement(vlinterface, 'interface')
        vlan = ET.SubElement(interface, 'vlan')
        name = ET.SubElement(vlan, 'name')
        name.text = vlan_id
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def del_vlan_int(self, vlan_id):
        """
        Delete VLAN Interface.

        Args:
            vlan_id: ID for the VLAN interface being created. Value of 2-4096.

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        vlinterface = ET.SubElement(config, 'interface-vlan',
                                    xmlns=("urn:brocade.com:mgmt:"
                                           "brocade-interface"))
        interface = ET.SubElement(vlinterface, 'interface')
        vlan = ET.SubElement(interface, 'vlan', operation='delete')
        name = ET.SubElement(vlan, 'name')
        name.text = vlan_id
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def enable_switchport(self, inter_type, inter):
        """
        Change an interface's operation to L2.

        Args:
            inter_type: The type of interface you want to configure. Ex.
                tengigabitethernet, gigabitethernet, fortygigabitethernet.
            inter: The ID for the interface you want to configure. Ex. 1/0/1

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        interface = ET.SubElement(config, 'interface',
                                  xmlns=("urn:brocade.com:mgmt:"
                                         "brocade-interface"))
        int_type = ET.SubElement(interface, inter_type)
        name = ET.SubElement(int_type, 'name')
        name.text = inter
        switchport_basic = ET.SubElement(int_type, 'switchport-basic')
        ET.SubElement(switchport_basic, 'basic')
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def disable_switchport(self, inter_type, inter):
        """
        Change an interface's operation to L3.

        Args:
            inter_type: The type of interface you want to configure. Ex.
                tengigabitethernet, gigabitethernet, fortygigabitethernet.
            inter: The ID for the interface you want to configure. Ex. 1/0/1

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        interface = ET.SubElement(config, 'interface',
                                  xmlns=("urn:brocade.com:mgmt:"
                                         "brocade-interface"))
        int_type = ET.SubElement(interface, inter_type)
        name = ET.SubElement(int_type, 'name')
        name.text = inter
        ET.SubElement(int_type, 'switchport-basic', operation='delete')
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def access_vlan(self, inter_type, inter, vlan_id):
        """
        Add a L2 Interface to a specific VLAN.

        Args:
            inter_type: The type of interface you want to configure. Ex.
                tengigabitethernet, gigabitethernet, fortygigabitethernet.
            inter: The ID for the interface you want to configure. Ex. 1/0/1
            vlan_id: ID for the VLAN interface being modified. Value of 2-4096.

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        interface = ET.SubElement(config, 'interface',
                                  xmlns=("urn:brocade.com:mgmt:"
                                         "brocade-interface"))
        int_type = ET.SubElement(interface, inter_type)
        name = ET.SubElement(int_type, 'name')
        name.text = inter
        switchport = ET.SubElement(int_type, 'switchport')
        access = ET.SubElement(switchport, 'access')
        accessvlan = ET.SubElement(access, 'accessvlan')
        accessvlan.text = vlan_id
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def del_access_vlan(self, inter_type, inter, vlan_id):
        """
        Remove a L2 Interface from a specific VLAN, placing it back into the
        default VLAN.

        Args:
            inter_type: The type of interface you want to configure. Ex.
                tengigabitethernet, gigabitethernet, fortygigabitethernet.
            inter: The ID for the interface you want to configure. Ex. 1/0/1
            vlan_id: ID for the VLAN interface being modified. Value of 2-4096.

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        interface = ET.SubElement(config, 'interface',
                                  xmlns=("urn:brocade.com:mgmt:"
                                         "brocade-interface"))
        int_type = ET.SubElement(interface, inter_type)
        name = ET.SubElement(int_type, 'name')
        name.text = inter
        switchport = ET.SubElement(int_type, 'switchport')
        access = ET.SubElement(switchport, 'access')
        accessvlan = ET.SubElement(access, 'accessvlan', operation='delete')
        accessvlan.text = vlan_id
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def set_ip(self, inter_type, inter, ip_addr):
        """
        Set IP address of a L3 interface.

        Args:
            inter_type: The type of interface you want to configure. Ex.
                tengigabitethernet, gigabitethernet, fortygigabitethernet.
            inter: The ID for the interface you want to configure. Ex. 1/0/1
            ip_addr: IP Address in <prefix>/<bits> format. Ex: 10.10.10.1/24

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        interface = ET.SubElement(config, 'interface',
                                  xmlns=("urn:brocade.com:mgmt:"
                                         "brocade-interface"))
        intert = ET.SubElement(interface, inter_type)
        name = ET.SubElement(intert, 'name')
        name.text = inter
        ipel = ET.SubElement(intert, 'ip')
        ip_config = ET.SubElement(
            ipel, 'ip-config',
            xmlns="urn:brocade.com:mgmt:brocade-ip-config"
        )
        address = ET.SubElement(ip_config, 'address')
        ipaddr = ET.SubElement(address, 'address')
        ipaddr.text = ip_addr
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def remove_port_channel(self, **kwargs):
        """
        Remove a port channel interface.

        Args:
            port_int (str): port-channel number (1, 2, 3, etc).
            callback (function): A function executed upon completion of the
                 method.  The only parameter passed to `callback` will be the
                 ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `port_int` is not passed.
            ValueError: if `port_int` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...    conn = (switch, '22')
            ...    with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...        output = dev.interface.remove_port_channel(port_int='1')
        """
        port_int = kwargs.pop('port_int')
        callback = kwargs.pop('callback', self._callback)

        if re.search('^[0-9]{1,3}$', port_int) is None:
            raise ValueError('%s must be in the format of x for port channel '
                             'interfaces.' % repr(port_int))

        port_channel = getattr(self._interface, 'interface_port_channel_name')
        port_channel_args = dict(name=port_int)

        config = port_channel(**port_channel_args)

        delete_channel = config.find('.//*port-channel')
        delete_channel.set('operation', 'delete')

        return callback(config)

    def ip_address(self, **kwargs):
        """
        Set IP Address on an Interface.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                 tengigabitethernet etc).
            name (str): Name of interface id.
                 (For interface: 1/0/5, 1/0/10 etc).
            ip_addr (str): IPv4/IPv6 Virtual IP Address..
                Ex: 10.10.10.1/24 or 2001:db8::/48
            delete (bool): True is the IP address is added and False if its to
                be deleted (True, False). Default value will be False if not
                specified.
            callback (function): A function executed upon completion of the
                 method.  The only parameter passed to `callback` will be the
                 ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `ip_addr` is not passed.
            ValueError: if `int_type`, `name`, or `ip_addr` are invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...    conn = (switch, '22')
            ...    with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...        int_type = 'tengigabitethernet'
            ...        name = '225/0/3'
            ...        ip_addr = '20.10.10.1/24'
            ...        output = dev.interface.disable_switchport(inter_type=
            ...        int_type, inter=name)
            ...        output = dev.interface.ip_address(int_type=int_type,
            ...        name=name, ip_addr=ip_addr)
            ...        output = dev.interface.ip_address(int_type=int_type,
            ...        name=name, ip_addr=ip_addr, delete=True)
            ...        ip_addr = 'fc00:1:3:1ad3:0:0:23:a/64'
            ...        output = dev.interface.ip_address(int_type=int_type,
            ...        name=name, ip_addr=ip_addr)
            ...        output = dev.interface.ip_address(int_type=int_type,
            ...        name=name, ip_addr=ip_addr, delete=True)
        """

        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        ip_addr = str(kwargs.pop('ip_addr'))
        delete = kwargs.pop('delete', False)
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['gigabitethernet', 'tengigabitethernet',
                           'fortygigabitethernet', 'hundredgigabitethernet']

        if int_type not in valid_int_types:
            raise ValueError('%s must be one of: %s' %
                             repr(int_type), repr(valid_int_types))

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces.' % repr(name))

        ipaddress = ip_interface(unicode(ip_addr))

        if ipaddress.version == 4:
            ip_args = dict(name=name, address=ip_addr)
            ip_address_attr = getattr(self._interface, 'interface_%s_ip_ip_'
                                      'config_address_address' % int_type)
        elif ipaddress.version == 6:
            ip_args = dict(name=name, address=ip_addr)
            ip_address_attr = getattr(
                self._interface, 'interface_%s_ipv6_ipv6_config_address_ipv6_'
                'address_address' % int_type)

        config = ip_address_attr(**ip_args)
        if delete:
            delete_ip = config.find('.//*address')
            delete_ip.set('operation', 'delete')
        try:
            return callback(config)
        # TODO Setting IP on port channel is not done yet.
        except AttributeError as (errno, errstr):
            return None

    def del_ip(self, inter_type, inter, ip_addr):
        """
        Delete IP address from a L3 interface.

        Args:
            inter_type: The type of interface you want to configure. Ex.
                tengigabitethernet, gigabitethernet, fortygigabitethernet.
            inter: The ID for the interface you want to configure. Ex. 1/0/1
            ip_addr: IP Address in <prefix>/<bits> format. Ex: 10.10.10.1/24

        Returns:
            True if command completes successfully or False if not.

        Raises:
            None
        """
        config = ET.Element('config')
        interface = ET.SubElement(config, 'interface',
                                  xmlns=("urn:brocade.com:mgmt:"
                                         "brocade-interface"))
        intert = ET.SubElement(interface, inter_type)
        name = ET.SubElement(intert, 'name')
        name.text = inter
        ipel = ET.SubElement(intert, 'ip')
        ip_config = ET.SubElement(
            ipel, 'ip-config',
            xmlns="urn:brocade.com:mgmt:brocade-ip-config"
        )
        address = ET.SubElement(ip_config, 'address', operation='delete')
        ipaddr = ET.SubElement(address, 'address')
        ipaddr.text = ip_addr
        try:
            self._callback(config)
            return True
        # TODO add logging and narrow exception window.
        except Exception as error:
            logging.error(error)
            return False

    def description(self, **kwargs):
        """Set interface description.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            desc (str): The description of the interface.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `desc` is not specified.
            ValueError: if `name`, `int_type`, or `desc` is not a valid
                value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.description(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/38',
            ...         desc='test')
            ...         dev.interface.description()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        desc = str(kwargs.pop('desc'))
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet',
            'port_channel',
            'vlan'
            ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))

        desc_args = dict(name=name, description=desc)

        if int_type == "vlan":
            if not pynos.utilities.valid_vlan_id(name):
                raise ValueError("`name` must be between `1` and `4096`")

            config = self._interface.interface_vlan_interface_vlan_description(
                **desc_args
                )
        else:
            if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None \
                    and re.search('^[0-9]{1,3}$', name) is None:
                raise ValueError('%s must be in the format of x/y/z for '
                                 'physical interfaces or x for port channel.'
                                 % repr(name))

            config = getattr(
                self._interface,
                'interface_%s_description' % int_type
                )(**desc_args)
        return callback(config)

    def private_vlan_type(self, **kwargs):
        """Set the PVLAN type (primary, isolated, community).

        Args:
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            pvlan_type (str): PVLAN type (primary, isolated, community)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `name` or `pvlan_type` is not specified.
            ValueError: if `name` or `pvlan_type` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> name = '90'
            >>> pvlan_type = 'isolated'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.private_vlan_type(name=name,
            ...         pvlan_type=pvlan_type)
            ...         dev.interface.private_vlan_type()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        name = kwargs.pop('name')
        pvlan_type = kwargs.pop('pvlan_type')
        callback = kwargs.pop('callback', self._callback)
        allowed_pvlan_types = ['isolated', 'primary', 'community']

        if not pynos.utilities.valid_vlan_id(name):
            raise ValueError("Incorrect name value.")

        if pvlan_type not in allowed_pvlan_types:
            raise ValueError("Incorrect pvlan_type")

        pvlan_args = dict(name=name, pvlan_type_leaf=pvlan_type)
        pvlan_type = getattr(self._interface,
                             'interface_vlan_interface_vlan_'
                             'private_vlan_pvlan_type_leaf')
        config = pvlan_type(**pvlan_args)
        return callback(config)

    def vlan_pvlan_association_add(self, **kwargs):
        """Add a secondary PVLAN to a primary PVLAN.

        Args:
            name (str): VLAN number (1-4094).
            sec_vlan (str): The secondary PVLAN.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `name` or `sec_vlan` is not specified.
            ValueError: if `name` or `sec_vlan` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '20'
            >>> sec_vlan = '30'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.private_vlan_type(name=name,
            ...         pvlan_type='primary')
            ...         output = dev.interface.private_vlan_type(name=sec_vlan,
            ...         pvlan_type='isolated')
            ...         output = dev.interface.vlan_pvlan_association_add(
            ...         name=name, sec_vlan=sec_vlan)
            ...         dev.interface.vlan_pvlan_association_add()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        name = kwargs.pop('name')
        sec_vlan = kwargs.pop('sec_vlan')
        callback = kwargs.pop('callback', self._callback)

        if not pynos.utilities.valid_vlan_id(name):
            raise ValueError("Incorrect name value.")
        if not pynos.utilities.valid_vlan_id(sec_vlan):
            raise ValueError("`sec_vlan` must be between `1` and `4095`.")

        pvlan_args = dict(name=name, sec_assoc_add=sec_vlan)
        pvlan_assoc = getattr(self._interface,
                              'interface_vlan_interface_vlan_'
                              'private_vlan_association_sec_assoc_add')
        config = pvlan_assoc(**pvlan_args)
        return callback(config)

    def pvlan_host_association(self, **kwargs):
        """Set interface PVLAN association.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            pri_vlan (str): The primary PVLAN.
            sec_vlan (str): The secondary PVLAN.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, `pri_vlan`, or `sec_vlan` is not
                specified.
            ValueError: if `int_type`, `name`, `pri_vlan`, or `sec_vlan`
                is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '225/0/38'
            >>> pri_vlan = '75'
            >>> sec_vlan = '100'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.private_vlan_type(name=pri_vlan,
            ...         pvlan_type='primary')
            ...         output = dev.interface.private_vlan_type(name=sec_vlan,
            ...         pvlan_type='isolated')
            ...         output = dev.interface.vlan_pvlan_association_add(
            ...         name=pri_vlan, sec_vlan=sec_vlan)
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.private_vlan_mode(
            ...         int_type=int_type, name=name, mode='host')
            ...         output = dev.interface.pvlan_host_association(
            ...         int_type=int_type, name=name, pri_vlan=pri_vlan,
            ...         sec_vlan=sec_vlan)
            ...         dev.interface.pvlan_host_association()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        pri_vlan = kwargs.pop('pri_vlan')
        sec_vlan = kwargs.pop('sec_vlan')
        callback = kwargs.pop('callback', self._callback)

        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel']

        if int_type not in int_types:
            raise ValueError("Incorrect int_type value.")

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        if not pynos.utilities.valid_vlan_id(pri_vlan):
            raise ValueError("`sec_vlan` must be between `1` and `4095`.")
        if not pynos.utilities.valid_vlan_id(sec_vlan):
            raise ValueError("`sec_vlan` must be between `1` and `4095`.")

        pvlan_args = dict(name=name, host_pri_pvlan=pri_vlan)

        associate_pvlan = getattr(self._interface,
                                  'interface_%s_switchport_private_vlan_'
                                  'host_association_host_pri_pvlan' %
                                  int_type)
        config = associate_pvlan(**pvlan_args)
        sec_assoc = config.find('.//*host-association')
        sec_assoc = ET.SubElement(sec_assoc, 'host-sec-pvlan')
        sec_assoc.text = sec_vlan
        return callback(config)

    def admin_state(self, **kwargs):
        """Set interface administrative state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc).
            name (str): Name of interface. (1/0/5, 1/0/10, etc).
            enabled (bool): Is the interface enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `enabled` is not passed.
            ValueError: if `int_type`, `name`, or `enabled` are invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         dev.interface.admin_state(
            ...         int_type='tengigabitethernet', name='225/0/38',
            ...         enabled=False)
            ...         dev.interface.admin_state(
            ...         int_type='tengigabitethernet', name='225/0/38',
            ...         enabled=True)
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        enabled = kwargs.pop('enabled')
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['gigabitethernet', 'tengigabitethernet',
                           'fortygigabitethernet', 'hundredgigabitethernet',
                           'port_channel']

        if int_type not in valid_int_types:
            raise ValueError('`int_type` must be one of: %s' %
                             repr(valid_int_types))

        if not isinstance(enabled, bool):
            raise ValueError('`enabled` must be `True` or `False`.')

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        state_args = dict(name=name)
        admin_state = getattr(self._interface,
                              'interface_%s_shutdown' % int_type)
        config = admin_state(**state_args)
        if enabled:
            shutdown = config.find('.//*shutdown')
            shutdown.set('operation', 'delete')
        try:
            return callback(config)
        # TODO: Catch existing 'no shut'
        # This is in place because if the interface is already admin up,
        # `ncclient` will raise an error if you try to admin up the interface
        # again.
        except AttributeError:
            return None

    def pvlan_trunk_association(self, **kwargs):
        """Set switchport private vlan host association.

        Args:

        Returns:

        Raises:

        Examples:
        """
        pass

    def trunk_allowed_vlan(self, **kwargs):
        """Modify allowed VLANs on Trunk (add, remove, none, all).

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            action (str): Action to take on trunk. (add, remove, none, all)
            vlan (str): vlan id for action. Only valid for add and remove.
            ctag (str): ctag range. Only valid for add and remove.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `mode` is not specified.
            ValueError: if `int_type`, `name`, or `mode` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.226', '10.24.52.10']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '226/0/4'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.trunk_mode(int_type=int_type,
            ...         name=name, mode='trunk')
            ...         output = dev.interface.trunk_allowed_vlan(
            ...         int_type=int_type, name=name, action='add', ctag='25',
            ...         vlan='8000')
            ...         dev.interface.private_vlan_mode()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        action = kwargs.pop('action')
        ctag = kwargs.pop('ctag', None)
        vlan = kwargs.pop('vlan', None)
        callback = kwargs.pop('callback', self._callback)

        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel']
        valid_actions = ['add', 'remove', 'none', 'all']

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" %
                             repr(int_types))

        if action not in valid_actions:
            raise ValueError('%s must be one of: %s' % (action, valid_actions))

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        allowed_vlan_args = dict(name=name,
                                 add=vlan,
                                 remove=vlan,
                                 trunk_vlan_id=vlan,
                                 trunk_ctag_range=ctag
                                 )

        ctag_actions = ['add', 'remove']

        if ctag and not vlan:
            raise ValueError('vlan must be set when ctag is set ')

        if ctag and action not in ctag_actions:
            raise ValueError('%s must be in %s when %s is set '
                             % (repr(action),
                                repr(ctag_actions),
                                repr(ctag)
                                )
                             )

        if not ctag:
            allowed_vlan = getattr(self._interface,
                                   'interface_%s_switchport_trunk_'
                                   'allowed_vlan_%s' %
                                   (int_type, action))
        else:
            allowed_vlan = getattr(self._interface,
                                   'interface_%s_switchport_trunk_trunk_vlan_'
                                   'classification_allowed_vlan_%s_trunk_'
                                   'ctag_range'
                                   % ((int_type, action))
                                   )
        config = allowed_vlan(**allowed_vlan_args)
        return callback(config)

    def private_vlan_mode(self, **kwargs):
        """Set PVLAN mode (promiscuous, host, trunk).

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            mode (str): The switchport PVLAN mode.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `mode` is not specified.
            ValueError: if `int_type`, `name`, or `mode` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '225/0/38'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.private_vlan_mode(
            ...         int_type=int_type, name=name, mode='trunk_host')
            ...         dev.interface.private_vlan_mode()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        mode = kwargs.pop('mode').lower()
        callback = kwargs.pop('callback', self._callback)

        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel']
        valid_modes = ['host', 'promiscuous', 'trunk_host',
                       'trunk_basic', 'trunk_promiscuous']

        if int_type not in int_types:
            raise ValueError("Incorrect int_type value.")

        if mode not in valid_modes:
            raise ValueError('%s must be one of: %s' % (mode, valid_modes))

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        pvlan_args = dict(name=name)

        if 'trunk' in mode:
            pvlan_mode = getattr(self._interface,
                                 'interface_%s_switchport_mode_'
                                 'private_vlan_private_vlan_trunk_%s' %
                                 (int_type, mode))
        else:
            pvlan_mode = getattr(self._interface,
                                 'interface_%s_switchport_mode_'
                                 'private_vlan_%s' % (int_type, mode))
        config = pvlan_mode(**pvlan_args)
        return callback(config)

    def spanning_tree_state(self, **kwargs):
        """Set Spanning Tree state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc).
            name (str): Name of interface or VLAN id.
                (For interface: 1/0/5, 1/0/10 etc).
                (For VLANs 0, 1, 100 etc).
            enabled (bool): Is the interface enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `enabled` is not passed.
            ValueError: if `int_type`, `name`, or `enabled` are invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         enabled = True
            ...         int_type = 'tengigabitethernet'
            ...         name = '225/0/37'
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         enabled = False
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         int_type = 'vlan'
            ...         name = '102'
            ...         enabled = False
            ...         output = dev.interface.add_vlan_int(name)
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         enabled = False
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        enabled = kwargs.pop('enabled')
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['gigabitethernet', 'tengigabitethernet',
                           'fortygigabitethernet', 'hundredgigabitethernet',
                           'port_channel',  'vlan']

        if int_type not in valid_int_types:
            raise ValueError('%s must be one of: %s' %
                             repr(int_type), repr(valid_int_types))

        if not isinstance(enabled, bool):
            raise ValueError('%s must be `True` or `False`.' % repr(enabled))

        if int_type == 'vlan':
            if not pynos.utilities.valid_vlan_id(name):
                raise ValueError('%s must be between 0 to 4095.' % int_type)

            state_args = dict(name=name)
            spanning_tree_state = getattr(self._interface,
                                          'interface_%s_interface_%s_spanning_'
                                          'tree_stp_shutdown' % (int_type,
                                                                 int_type))

        else:
            if re.search(r'^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
                raise ValueError('%s must be in the format of x/y/z.'
                                 % int_type)

            state_args = dict(name=name)
            spanning_tree_state = getattr(self._interface,
                                          'interface_%s_spanning_tree_'
                                          'shutdown' % int_type)

        config = spanning_tree_state(**state_args)

        if enabled:
            if int_type == 'vlan':
                shutdown = config.find('.//*stp-shutdown')
            else:
                shutdown = config.find('.//*shutdown')
            shutdown.set('operation', 'delete')
        try:
            return callback(config)
        # TODO: Catch existing 'no shut'
        # This is in place because if the interface spanning tree is already
        # up,`ncclient` will raise an error if you try to admin up the
        # interface again.
        # TODO: add logic to shutdown STP at protocol level too.
        except AttributeError:
            return None

    def tag_native_vlan(self, **kwargs):
        """Set tagging of native VLAN on trunk.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            mode (str): Trunk port mode (trunk, trunk-no-default-native).
            enabled (bool): Is tagging of the VLAN enabled on trunks?
                (True, False)
            callback (function): A function executed upon completion oj the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `state` is not specified.
            ValueError: if `int_type`, `name`, or `state` is not valid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.trunk_mode(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/38', mode='trunk')
            ...         output = dev.interface.tag_native_vlan(name='225/0/38',
            ...         int_type='tengigabitethernet')
            ...         output = dev.interface.tag_native_vlan(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/38', enabled=False)
            ...         dev.interface.tag_native_vlan()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)

        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel']

        if int_type not in int_types:
            raise ValueError("Incorrect int_type value.")

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        if not isinstance(enabled, bool):
            raise ValueError("Invalid state.")

        tag_args = dict(name=name)
        tag_native_vlan = getattr(self._interface, 'interface_%s_switchport_'
                                  'trunk_tag_native_vlan' % int_type)
        config = tag_native_vlan(**tag_args)
        if not enabled:
            untag = config.find('.//*native-vlan')
            untag.set('operation', 'delete')

        try:
            return callback(config)
        # TODO: Catch existing 'no switchport tag native-vlan'
        except AttributeError:
            return None

    def switchport_pvlan_mapping(self, **kwargs):
        """Switchport private VLAN mapping.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            pri_vlan (str): The primary PVLAN.
            sec_vlan (str): The secondary PVLAN.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `mode` is not specified.
            ValueError: if `int_type`, `name`, or `mode` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '225/0/37'
            >>> pri_vlan = '3000'
            >>> sec_vlan = ['3001', '3002']
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.private_vlan_type(name=pri_vlan,
            ...         pvlan_type='primary')
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.private_vlan_mode(
            ...         int_type=int_type, name=name, mode='trunk_promiscuous')
            ...         for spvlan in sec_vlan:
            ...             output = dev.interface.private_vlan_type(
            ...             name=spvlan, pvlan_type='isolated')
            ...             output = dev.interface.vlan_pvlan_association_add(
            ...             name=pri_vlan, sec_vlan=spvlan)
            ...             output = dev.interface.switchport_pvlan_mapping(
            ...             int_type=int_type, name=name, pri_vlan=pri_vlan,
            ...             sec_vlan=spvlan)
            ...         dev.interface.switchport_pvlan_mapping()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        pri_vlan = kwargs.pop('pri_vlan')
        sec_vlan = kwargs.pop('sec_vlan')
        callback = kwargs.pop('callback', self._callback)
        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel']

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))

        if not re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) \
                and not re.search('^[0-9]{1,3}$', name):
            raise ValueError("`name` must be in the format of x/y/x for "
                             "physical interfaces or x for port channel.")

        if not pynos.utilities.valid_vlan_id(pri_vlan, extended=True):
                raise ValueError("`pri_vlan` must be between `1` and `4096`")

        if not pynos.utilities.valid_vlan_id(sec_vlan, extended=True):
                raise ValueError("`sec_vlan` must be between `1` and `4096`")

        pvlan_args = dict(name=name,
                          promis_pri_pvlan=pri_vlan,
                          promis_sec_pvlan_range=sec_vlan)
        pvlan_mapping = getattr(self._interface,
                                'interface_gigabitethernet_switchport_'
                                'private_vlan_mapping_promis_sec_pvlan_range')
        config = pvlan_mapping(**pvlan_args)
        return callback(config)

    def mtu(self, **kwargs):
        """Set interface mtu.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            mtu (str): Value between 1522 and 9216
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `mtu` is not specified.
            ValueError: if `int_type`, `name`, or `mtu` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.mtu(mtu='1666',
            ...         int_type='tengigabitethernet', name='225/0/38')
            ...         dev.interface.mtu() # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        mtu = kwargs.pop('mtu')
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet',
            'port_channel'
            ]

        if int_type not in int_types:
            raise ValueError("Incorrect int_type value.")

        valid_mtu = range(1522, 9216)
        if int(mtu) not in valid_mtu:
            raise ValueError("Incorrect mtu value 1522-9216")

        mtu_args = dict(name=name, mtu=mtu)

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        config = getattr(
            self._interface,
            'interface_%s_mtu' % int_type
            )(**mtu_args)
        return callback(config)

    def fabric_isl(self, **kwargs):
        """Set fabric ISL state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            enabled (bool): Is fabric ISL state enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `state` is not specified.
            ValueError: if `int_type`, `name`, or `state` is not a valid value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.fabric_isl(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/40',
            ...         enabled=False)
            ...         dev.interface.fabric_isl()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet'
            ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" %
                             repr(int_types))

        if not isinstance(enabled, bool):
            raise ValueError('`enabled` must be `True` or `False`.')

        fabric_isl_args = dict(name=name)

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
            raise ValueError("`name` must match `^[0-9]{1,3}/[0-9]{1,3}/[0-9]"
                             "{1,3}$`")

        config = getattr(
            self._interface,
            'interface_%s_fabric_fabric_isl_fabric_isl_enable' % int_type
            )(**fabric_isl_args)

        if not enabled:
            fabric_isl = config.find('.//*fabric-isl')
            fabric_isl.set('operation', 'delete')

        return callback(config)

    def fabric_trunk(self, **kwargs):
        """Set fabric trunk state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            enabled (bool): Is Fabric trunk enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `state` is not specified.
            ValueError: if `int_type`, `name`, or `state` is not a valid value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.fabric_trunk(name='225/0/40',
            ...         int_type='tengigabitethernet', enabled=False)
            ...         dev.interface.fabric_trunk()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet'
            ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))

        if not isinstance(enabled, bool):
            raise ValueError('`enabled` must be `True` or `False`.')

        fabric_trunk_args = dict(name=name)

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
            raise ValueError("`name` must match `^[0-9]{1,3}/[0-9]{1,3}/[0-9]"
                             "{1,3}$`")

        config = getattr(
            self._interface,
            'interface_%s_fabric_fabric_trunk_fabric_trunk_enable' % int_type
            )(**fabric_trunk_args)

        if not enabled:
            fabric_trunk = config.find('.//*fabric-trunk')
            fabric_trunk.set('operation', 'delete')

        return callback(config)

    def v6_nd_suppress_ra(self, **kwargs):
        """Set interface description.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            rbridge_id (str): rbridge-id for device. Only required when type is
                `ve`.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `rbridge_id` is not specified.
            ValueError: if `int_type`, `name`, or `rbridge_id` is not a valid
                value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.v6_nd_suppress_ra(name='10',
            ...         int_type='ve', rbridge_id='225')
            ...         dev.interface.v6_nd_suppress_ra()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet',
            've'
            ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))

        if int_type == "ve":
            if re.search('^[0-9]{1,4}$', name) is None:
                raise ValueError("`name` must be between `1` and `8191`")

            rbridge_id = kwargs.pop('rbridge_id', "1")

            nd_suppress_args = dict(name=name, rbridge_id=rbridge_id)
            nd_suppress = getattr(self._rbridge,
                                  'rbridge_id_interface_ve_ipv6_'
                                  'ipv6_nd_ra_ipv6_intf_cmds_'
                                  'nd_suppress_ra_suppress_ra_all')
            config = nd_suppress(**nd_suppress_args)
        else:
            if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
                raise ValueError("`name` must match "
                                 "`^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$`")

            nd_suppress_args = dict(name=name)
            nd_suppress = getattr(self._interface,
                                  'interface_%s_ipv6_ipv6_nd_ra_'
                                  'ipv6_intf_cmds_nd_suppress_ra_'
                                  'suppress_ra_all' % int_type)
            config = nd_suppress(**nd_suppress_args)
        return callback(config)

    def vrrp_vip(self, **kwargs):
        """Set VRRP VIP.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc).
            name (str): Name of interface. (1/0/5, 1/0/10, etc).
            vrid (str): VRRPv3 ID.
            vip (str): IPv4/IPv6 Virtual IP Address.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, `vrid`, or `vip` is not passed.
            ValueError: if `int_type`, `name`, `vrid`, or `vip` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.set_ip('tengigabitethernet',
            ...         '225/0/18', '10.1.1.2/24')
            ...         output = dev.interface.ip_address(name='225/0/18',
            ...         int_type='tengigabitethernet',
            ...         ip_addr='2001:4818:f000:1ab:cafe:beef:1000:2/64')
            ...         dev.interface.vrrp_vip(int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1', vip='10.1.1.1/24')
            ...         dev.interface.vrrp_vip(int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1',
            ...         vip='fe80::cafe:beef:1000:1/64')
            ...         dev.interface.vrrp_vip(int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1',
            ...         vip='2001:4818:f000:1ab:cafe:beef:1000:1/64')
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        vrid = kwargs.pop('vrid')
        vip = kwargs.pop('vip')
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['gigabitethernet', 'tengigabitethernet',
                           'fortygigabitethernet', 'hundredgigabitethernet',
                           'port_channel']

        if int_type not in valid_int_types:
            raise ValueError('`int_type` must be one of: %s' %
                             repr(valid_int_types))

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        ipaddress = ip_interface(unicode(vip))

        vrrp_args = dict(name=name,
                         vrid=vrid,
                         virtual_ipaddr=str(ipaddress.ip))
        vrrp_vip = None
        if ipaddress.version == 4:
            vrrp_args['version'] = '3'
            vrrp_vip = getattr(self._interface,
                               'interface_%s_vrrp_virtual_ip_'
                               'virtual_ipaddr' % int_type)
        elif ipaddress.version == 6:
            vrrp_vip = getattr(self._interface,
                               'interface_%s_ipv6_vrrpv3_group_virtual_ip_'
                               'virtual_ipaddr' % int_type)
        config = vrrp_vip(**vrrp_args)
        return callback(config)

    def vrrp_state(self, **kwargs):
        """Set VRRP state (enabled, disabled).

        Args:

        Returns:

        Raises:

        Examples:
        """
        pass

    def vrrp_preempt(self, **kwargs):
        """Set VRRP preempt mode (enabled, disabled).

        Args:

        Returns:

        Raises:

        Examples:
        """
        pass

    def vrrp_priority(self, **kwargs):
        """Set VRRP priority.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc).
            name (str): Name of interface. (1/0/5, 1/0/10, etc).
            vrid (str): VRRPv3 ID.
            priority (str): VRRP Priority.
            ip_version (str): Version of IP (4, 6).
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, `vrid`, `priority`, or
                `ip_version` is not passed.
            ValueError: if `int_type`, `name`, `vrid`, `priority`, or
                `ip_version` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.set_ip('tengigabitethernet',
            ...         '225/0/18', '10.1.1.2/24')
            ...         output = dev.interface.ip_address(name='225/0/18',
            ...         int_type='tengigabitethernet',
            ...         ip_addr='2001:4818:f000:1ab:cafe:beef:1000:2/64')
            ...         dev.interface.vrrp_vip(int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1', vip='10.1.1.1/24')
            ...         dev.interface.vrrp_vip(int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1',
            ...         vip='fe80::cafe:beef:1000:1/64')
            ...         dev.interface.vrrp_vip(int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1',
            ...         vip='2001:4818:f000:1ab:cafe:beef:1000:1/64')
            ...         dev.interface.vrrp_priority(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1', ip_version='4',
            ...         priority='66')
            ...         dev.interface.vrrp_priority(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/18', vrid='1', ip_version='6',
            ...         priority='77')
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        vrid = kwargs.pop('vrid')
        priority = kwargs.pop('priority')
        ip_version = int(kwargs.pop('ip_version'))
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['gigabitethernet', 'tengigabitethernet',
                           'fortygigabitethernet', 'hundredgigabitethernet',
                           'port_channel']

        if int_type not in valid_int_types:
            raise ValueError('`int_type` must be one of: %s' %
                             repr(valid_int_types))

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        vrrp_args = dict(name=name,
                         vrid=vrid,
                         priority=priority)
        vrrp_priority = None
        if ip_version == 4:
            vrrp_args['version'] = '3'
            vrrp_priority = getattr(self._interface,
                                    'interface_%s_vrrp_priority' % int_type)
        elif ip_version == 6:
            vrrp_priority = getattr(self._interface,
                                    'interface_%s_ipv6_vrrpv3_group_priority' %
                                    int_type)
        config = vrrp_priority(**vrrp_args)
        return callback(config)

    def vrrp_advertisement_interval(self, **kwargs):
        """Set VRRP advertisement interval.

        Args:

        Returns:

        Raises:

        Examples:
        """
        pass

    def proxy_arp(self, **kwargs):
        """Set interface administrative state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc).
            name (str): Name of interface. (1/0/5, 1/0/10, etc).
            enabled (bool): Is proxy-arp enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `state` is not passed.
            ValueError: if `int_type`, `name`, or `state` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         dev.interface.proxy_arp(int_type='tengigabitethernet',
            ...         name='225/0/12', enabled=True)
            ...         dev.interface.proxy_arp(int_type='tengigabitethernet',
            ...         name='225/0/12', enabled=False)
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['gigabitethernet', 'tengigabitethernet',
                           'fortygigabitethernet', 'hundredgigabitethernet',
                           'port_channel']

        if int_type not in valid_int_types:
            raise ValueError('`int_type` must be one of: %s' %
                             repr(valid_int_types))

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        if not isinstance(enabled, bool):
            raise ValueError('`enabled` must be `True` or `False`.')

        state_args = dict(name=name)
        proxy_arp = getattr(self._interface,
                            'interface_%s_ip_ip_config_proxy_arp' % int_type)
        config = proxy_arp(**state_args)
        if not enabled:
            proxy_arp = config.find('.//*proxy-arp')
            proxy_arp.set('operation', 'delete')
        try:
            return callback(config)
        # TODO: Catch existing 'no shut'
        # This is in place because if the interface is already admin up,
        # `ncclient` will raise an error if you try to admin up the interface
        # again.
        except AttributeError:
            return None

    def port_channel_minimum_links(self, **kwargs):
        """Set minimum number of links in a port channel.

        Args:
            name (str): Port-channel number. (1, 5, etc)
            minimum_links (str): Minimum number of links in channel group.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `name` or `minimum_links` is not specified.
            ValueError: if `name` is not a valid value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.port_channel_minimum_links(
            ...         name='1', minimum_links='2')
            ...         dev.interface.port_channel_minimum_links()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        name = str(kwargs.pop('name'))
        minimum_links = str(kwargs.pop('minimum_links'))
        callback = kwargs.pop('callback', self._callback)

        min_links_args = dict(name=name, minimum_links=minimum_links)

        if re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError("`name` must match `^[0-9]{1,3}${1,3}$`")

        config = getattr(
            self._interface,
            'interface_port_channel_minimum_links'
            )(**min_links_args)

        return callback(config)

    def channel_group(self, **kwargs):
        """set channel group mode.

        args:
            int_type (str): type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): name of interface. (1/0/5, 1/0/10, etc)
            port_int (str): port-channel number (1, 2, 3, etc).
            channel_type (str): tiype of port-channel (standard, brocade)
            mode (str): mode of channel group (active, on, passive).
            delete (bool): Deletes the neighbor if `delete` is ``True``.
            callback (function): a function executed upon completion of the
                method.  the only parameter passed to `callback` will be the
                ``elementtree`` `config`.

        returns:
            return value of `callback`.

        raises:
            keyerror: if `int_type`, `name`, or `description` is not specified.
            valueerror: if `name` or `int_type` are not valid values.

        examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.channel_group(name='225/0/20',
            ...         int_type='tengigabitethernet',
            ...         port_int='1', channel_type='standard', mode='active')
            ...         dev.interface.channel_group()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        channel_type = kwargs.pop('channel_type')
        port_int = kwargs.pop('port_int')
        mode = kwargs.pop('mode')
        delete = kwargs.pop('delete', False)
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet'
            ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))

        valid_modes = ['active', 'on', 'passive']

        if mode not in valid_modes:
            raise ValueError("`mode` must be one of: %s" % repr(valid_modes))

        valid_types = ['brocade', 'standard']

        if channel_type not in valid_types:
            raise ValueError("`channel_type` must be one of: %s" %
                             repr(valid_types))

        if re.search('^[0-9]{1,3}$', port_int) is None:
                raise ValueError("incorrect port_int value.")

        channel_group_args = dict(name=name, mode=mode)

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
                raise ValueError("incorrect name value.")

        config = getattr(
            self._interface,
            'interface_%s_channel_group_mode' % int_type
            )(**channel_group_args)

        channel_group = config.find('.//*channel-group')
        if delete is True:
            channel_group.set('operation', 'delete')
        else:
            port_int_el = ET.SubElement(channel_group, 'port-int')
            port_int_el.text = port_int
            port_type_el = ET.SubElement(channel_group, 'type')
            port_type_el.text = channel_type

        return callback(config)

    def port_channel_vlag_ignore_split(self, **kwargs):
        """Ignore VLAG Split.

        Args:
            name (str): Port-channel number. (1, 5, etc)
            enabled (bool): Is ignore split enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `name` or `enable` is not specified.
            ValueError: if `name` is not a valid value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.port_channel_vlag_ignore_split(
            ...         name='1', enabled=True)
            ...         dev.interface.port_channel_vlag_ignore_split()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        name = str(kwargs.pop('name'))
        enabled = bool(kwargs.pop('enabled'))
        callback = kwargs.pop('callback', self._callback)

        vlag_ignore_args = dict(name=name)

        if re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError("`name` must match x")

        config = getattr(
            self._interface,
            'interface_port_channel_vlag_ignore_split'
            )(**vlag_ignore_args)

        if not enabled:
            ignore_split = config.find('.//*ignore-split')
            ignore_split.set('operation', 'delete')

        return callback(config)

    def trunk_mode(self, **kwargs):
        """Set trunk mode (trunk, trunk-no-default-vlan).

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            mode (str): Trunk port mode (trunk, trunk-no-default-native).
            callback (function): A function executed upon completion oj the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `mode` is not specified.
            ValueError: if `int_type`, `name`, or `mode` is not valid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.trunk_mode(name='225/0/38',
            ...         int_type='tengigabitethernet', mode='trunk')
            ...         dev.interface.trunk_mode()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        mode = kwargs.pop('mode').lower()
        callback = kwargs.pop('callback', self._callback)

        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel']

        if int_type not in int_types:
            raise ValueError("Incorrect int_type value.")

        valid_modes = ['trunk', 'trunk-no-default-native']
        if mode not in valid_modes:
            raise ValueError("Incorrect mode value")

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None and \
                re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for physical '
                             'interfaces or x for port channel.' % repr(name))

        mode_args = dict(name=name, vlan_mode=mode)
        switchport_mode = getattr(self._interface, 'interface_%s_switchport_'
                                  'mode_vlan_mode' % int_type)
        config = switchport_mode(**mode_args)
        return callback(config)

    def transport_service(self, **kwargs):
        """Configure VLAN Transport Service.

        Args:
            vlan (str): The VLAN ID.
            service_id (str): The transport-service ID.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `vlan` or `service_id` is not specified.
            ValueError: if `vlan` is invalid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.226', '10.24.52.10']
            >>> auth = ('admin', 'password')
            >>> vlan = '6666'
            >>> service_id = '1'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type='vlan', name=vlan, enabled=False)
            ...         output = dev.interface.transport_service(vlan=vlan,
            ...         service_id=service_id)
            ...         dev.interface.transport_service()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        vlan = kwargs.pop('vlan')
        service_id = kwargs.pop('service_id')
        callback = kwargs.pop('callback', self._callback)

        if not pynos.utilities.valid_vlan_id(vlan, extended=True):
            raise ValueError("%s must be between `1` and `8191`" %
                             repr(vlan))

        service_args = dict(name=vlan, transport_service=service_id)
        transport_service = getattr(self._interface,
                                    'interface_vlan_interface_vlan_'
                                    'transport_service')
        config = transport_service(**service_args)
        return callback(config)

    def lacp_timeout(self, **kwargs):
        """Set lacp timeout.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            timeout (str):  Timeout length.  (short, long)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `timeout` is not specified.
            ValueError: if `int_type`, `name`, or `timeout is not valid.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '225/0/39'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.channel_group(name=name,
            ...         int_type=int_type, port_int='1',
            ...         channel_type='standard', mode='active')
            ...         output = dev.interface.lacp_timeout(name=name,
            ...         int_type=int_type, timeout='long')
            ...         dev.interface.lacp_timeout()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        timeout = kwargs.pop('timeout')
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet'
            ]

        if int_type not in int_types:
            raise ValueError("Incorrect int_type value.")

        valid_timeouts = ['long', 'short']
        if timeout not in valid_timeouts:
            raise ValueError("Incorrect timeout value")

        timeout_args = dict(name=name, timeout=timeout)

        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None:
                raise ValueError("Incorrect name value.")

        config = getattr(
            self._interface,
            'interface_%s_lacp_timeout' % int_type
            )(**timeout_args)
        return callback(config)

    def switchport(self, **kwargs):
        """Set interface switchport status.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            enabled (bool): Is the interface enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type` or `name` is not specified.
            ValueError: if `name` or `int_type` is not a valid
                value.

        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.switchport(name='225/0/19',
            ...         int_type='tengigabitethernet')
            ...         output = dev.interface.switchport(name='225/0/19',
            ...         int_type='tengigabitethernet', enabled=False)
            ...         dev.interface.switchport()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)
        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel', 'vlan']

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))
        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None \
                and re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for '
                             'physical interfaces or x for port channel.'
                             % repr(name))

        switchport_args = dict(name=name)
        switchport = getattr(self._interface,
                             'interface_%s_switchport_basic_basic' % int_type)

        config = switchport(**switchport_args)
        if not enabled:
            config.find('.//*switchport-basic').set('operation', 'delete')
        return callback(config)

    def acc_vlan(self, **kwargs):
        """Set access VLAN on a port.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            vlan (str): VLAN ID to set as the access VLAN.
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `vlan` is not specified.
            ValueError: if `int_type`, `name`, or `vlan` is not valid.
        Examples:
            >>> import pynos.device
            >>> switches = ['10.24.48.225', '10.24.52.9']
            >>> auth = ('admin', 'password')
            >>> int_type = 'tengigabitethernet'
            >>> name = '225/0/31'
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pynos.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.add_vlan_int('736')
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.acc_vlan(int_type=int_type,
            ...         name=name, vlan='736')
            ...         dev.interface.acc_vlan()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = kwargs.pop('int_type')
        name = kwargs.pop('name')
        vlan = kwargs.pop('vlan')
        callback = kwargs.pop('callback', self._callback)
        int_types = ['gigabitethernet', 'tengigabitethernet',
                     'fortygigabitethernet', 'hundredgigabitethernet',
                     'port_channel', 'vlan']

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))
        if not pynos.utilities.valid_vlan_id(vlan):
            raise ValueError("`name` must be between `1` and `4096`")
        if re.search('^[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}$', name) is None \
                and re.search('^[0-9]{1,3}$', name) is None:
            raise ValueError('%s must be in the format of x/y/z for '
                             'physical interfaces or x for port channel.'
                             % repr(name))

        vlan_args = dict(name=name, accessvlan=vlan)
        access_vlan = getattr(self._interface,
                              'interface_%s_switchport_access_accessvlan' %
                              int_type)
        config = access_vlan(**vlan_args)
        return callback(config)
