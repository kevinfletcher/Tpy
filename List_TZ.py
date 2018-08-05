#!/usr/bin/env python

import pprint
import requests

from com.vmware.nsx_client import TransportZones
from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.lib import connect
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory


def main():
    # Create a session using the requests library. For more information on
    # requests, see http://docs.python-requests.org/en/master/
    session = requests.session()

    # If your NSX API server is using its default self-signed certificate,
    # you will need the following line, otherwise the python ssl layer
    # will reject the server certificate. THIS IS UNSAFE and you should
    # normally verify the server certificate.
    session.verify = False

    # Set up the API connector and security context
    # Don't forget to put your own NSX Manager IP Address
    nsx_url = 'https://%s:%s' % ("10.29.12.211", 443)
    connector = connect.get_requests_connector(
        session=session, msg_protocol='rest', url=nsx_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)

    # Don't forget to put your own username and password for NSX
    security_context = create_user_password_security_context(
        "admin", "VMware1!")
    connector.set_security_context(security_context)

    # Now any API calls we make should authenticate to NSX using
    # HTTP Basic Authentication. Let's get a list of all Transport Zones.
    transportzones_svc = TransportZones(stub_config)
    tzs = transportzones_svc.list()
    # Create a pretty printer to make the output look nice.
    pp = PrettyPrinter()
    pp.pprint(tzs)


if __name__ == "__main__":
    main()
