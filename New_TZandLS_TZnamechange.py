#!/usr/bin/env python

import pprint
import requests

from com.vmware.nsx_client import TransportZones
from com.vmware.nsx_client import LogicalSwitches
from com.vmware.nsx.model_client import TransportZone
from com.vmware.nsx.model_client import LogicalSwitch
from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.lib import connect
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory


def main():
    session = requests.session()
    session.verify = False
    nsx_url = 'https://%s:%s' % ("10.29.12.211", 443)
    connector = connect.get_requests_connector(
        session=session, msg_protocol='rest', url=nsx_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)
    security_context = create_user_password_security_context("admin", "VMware1!")
    connector.set_security_context(security_context)

    # Create the services we'll need.
    transportzones_svc = TransportZones(stub_config)
    logicalswitches_svc = LogicalSwitches(stub_config)

    # Create a transport zone.
    new_tz = TransportZone(
	transport_type=TransportZone.TRANSPORT_TYPE_OVERLAY,
	display_name="My New Transport Zone",
	description="Transport zone created by Python",
	host_switch_name="nsxtvds1"
    )
    tz = transportzones_svc.create(new_tz)
    print("Transport zone created. id is %s" % tz.id)

    # Create a Logical Switch based on this TZ
    ls = LogicalSwitch(
	transport_zone_id=tz.id,
	admin_state=LogicalSwitch.ADMIN_STATE_UP,
	replication_mode=LogicalSwitch.REPLICATION_MODE_MTEP,
	display_name="ls-demo",
    )
    ls = logicalswitches_svc.create(ls)
    print("Logical switch created. id is %s" % ls.id)
    print("Review the newly created Transport Zone and Logical Switch in NSX GUI")
    print("When you hit Enter the name of Transport Zone will be changed!!!")
    raw_input("Press Enter to continue...")
    # Read that transport zone.
    read_tz = transportzones_svc.get(tz.id)
    read_tz.display_name = "Updated TZ"
    updated_tz = transportzones_svc.update(tz.id, read_tz)

    print("Review the updated Transport Zone name in NSX GUI")
    print("When you hit Enter both the Logical Switch and the transport Zone will be deleted")
    raw_input("Press Enter to continue...")
    logicalswitches_svc.delete(ls.id)
    transportzones_svc.delete(tz.id)
    print("TZ and LS are deleted !!!")

if __name__ == "__main__":
    main()
