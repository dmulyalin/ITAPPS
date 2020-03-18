from py2neo import Graph, Node, Relationship, NodeMatcher
import pprint
import json
from ttp import ttp
import logging
from app import app
import os

logging.basicConfig(level="ERROR")
log = logging.getLogger(__name__)
TEMPLATES_FOLDER = os.path.join(app.config["BASEDIR"], 'app/upload_folder/ttp_templates/')
graph = Graph(host=app.config["NEO4J_SERVER_IP"], 
              password=app.config["NEO4J_SERVER_PASSWORD"], 
              username=app.config["NEO4J_SERVER_USER"])
matcher = NodeMatcher(graph)

# graph relationships
BELONGS_TO_VRF = Relationship.type("BELONGS_TO_VRF")
VRF_EXISTS_ON = Relationship.type("VRF_EXISTS_ON")
INTERFACE_BELONGS_TO = Relationship.type("INTERFACE_BELONGS_TO")
PARENT_INTERFACE = Relationship.type("PARENT_INTERFACE")
IP_ASSIGNED_TO = Relationship.type("IP_ASSIGNED_TO")
PARENT_SUBNET = Relationship.type("PARENT_SUBNET")
CDP_PEERING = Relationship.type("CDP_PEERING")
LLDP_PEERING = Relationship.type("LLDP_PEERING")
BELONGS_TO_BGP_AS = Relationship.type("BELONGS_TO_BGP_AS")
BGP_PEERING_STATE = Relationship.type("BGP_PEERING_STATE") # deprecated
BGP_PROCESS_DEVICE = Relationship.type("BGP_PROCESS_DEVICE")
BGP_CONFIG = Relationship.type("BGP_CONFIG")
BGP_PEERING_IP = Relationship.type("BGP_PEERING_IP")
BGP_PEERING_VRF = Relationship.type("BGP_PEERING_VRF")
VLAN_CONFIGURED_AS_TRUNK = Relationship.type("VLAN_CONFIGURED_AS_TRUNK")
VLAN_CONFIGURED_AS_ACCESS = Relationship.type("VLAN_CONFIGURED_AS_ACCESS")
VLAN_CONFIGURED_AS_VOICE = Relationship.type("VLAN_CONFIGURED_AS_VOICE")
VLAN_EXISTS_ON = Relationship.type("VLAN_EXISTS_ON")
HARDWARE = Relationship.type("HARDWARE")


# useful queries
queries = {
"delete_all": "MATCH (n) DETACH DELETE n",
"get_full_graph": "MATCH p=()-[]->() RETURN p LIMIT 250",
"get_subnet_between_devices": "MATCH p=(a:Device)-[:INTERFACE_BELONGS_TO]-(:Interface)-[:IP_ASSIGNED_TO]-(:IPv4_Address)-[:PARENT_SUBNET]-(s:IPv4_Subnet)-[:PARENT_SUBNET]-(:IPv4_Address)-[:IP_ASSIGNED_TO]-(:Interface)-[:INTERFACE_BELONGS_TO]-(b:Device) RETURN a.hostname, s.subnet, b.hostname",
"get_interface_by_uid_and_hostname": 'MATCH (i)-[:INTERFACE_BELONGS_TO]->(d:Device) WHERE d.hostname = "{hostname}" AND i.uid = "{int_uid}" RETURN i',
"get_cdp_peers": "MATCH p=()-[a:INTERFACE_BELONGS_TO]-()-[r:CDP_PEERING]-()-[b:INTERFACE_BELONGS_TO]-() RETURN p",
"get_ip_by_subnet_and_device": """
MATCH (s:IP_Subnet)-[:PARENT_SUBNET]-(ip:IP_Address)-[:IP_ASSIGNED_TO]-(:Interface)-[:INTERFACE_BELONGS_TO]-(d:Device) 
WHERE s.subnet = "{subnet}" AND d.hostname="{hostname}" RETURN ip.ip
""",
"get_ip_by_interface_and_device": """
MATCH (ip:IP_Address)-[:IP_ASSIGNED_TO]-(int:Interface)-[:INTERFACE_BELONGS_TO]-(d:Device)
WHERE int.uid = "{interface_uid}" AND d.hostname="{hostname}" RETURN ip.ip
""",
"get_bgp_peerings_config": """
MATCH (d1:Device)--(int1:Interface)--(ip1:IP_Address)--(p:BGP_Peering)--(ip2:IP_Address)--(int2:Interface)--(d2:Device)
WHERE id(ip1) > id(ip2)
MATCH (int1)--(v1:VRF)
MATCH (int2)--(v2:VRF)
MATCH (d1)--(:BGP_Process)-[cfg1:BGP_CONFIG]->(p)<-[cfg2:BGP_CONFIG]-(:BGP_Process)--(d2)
RETURN d1.hostname as Device_A, 
int1.name as Interface_A,
ip1.ip as IP_A,
v1.name as VRF_A,
d2.hostname as Device_B,
int2.name as Interface_B,
ip2.ip as IP_B,
v2.name as VRF_B,
cfg1.authentication_mode as auth_mode
""",
"get_devices_software_report": """
MATCH (d:Device)-[:HARDWARE]-(c:Chassis)
RETURN d.hostname as hostname, d.software_version as version, d.software_image as image, d.software_family as family, c.chassis as hardware
ORDER BY hostname
""",
"get_subnets_by_device": "MATCH (d:Device)-[:INTERFACE_BELONGS_TO]-(:Interface)-[:IP_ASSIGNED_TO]-(:IPv4_Address)--(s:IP_Subnet) WHERE d.hostname='{hostname}' RETURN s",
}

 

# TTP vars shared with parsing templates
ttp_vars = {
    "IfsNormalize": {
        'Lo':   ['^Loopback'], 
        'Gi':   ['^GigabitEthernet'], 
        'Po':   ['^port-channel', '^Port-channel'], 
        'Te':   ['^TenGigabitEthernet', '^TenGe', '^TenGigE'], 
        'Fa':   ['^FastEthernet'], 
        'Eth':  ['^Ethernet'], 
        'Pt':   ['^Port[^-]']
        # 'Te':   ['^TenGigabitEthernet', '^TenGe', '^10GE', '^TenGigE', '^XGigabitEthernet'],
        # 'Vl':   ['^Vlanif', '^Vlan'], 
        # '100GE':['^HundredGigE']
    }
}                 

def add_devices_nodes(data):
    for device_results in data:
        device_info = {}
        # get hostname info
        device_hostname = device_results['global_configuration']['hostname']
        # add software version info
        device_info.update(device_results.get("software_version", {}))
        # add device
        device_node = Node('Device', hostname=device_hostname, **device_info)
        graph.merge(device_node, "Device", "hostname")
        
        
def add_vrfs_nodes(data):
    # add global vrf
    vrf_node = Node('VRF', name="global")
    graph.merge(vrf_node, "VRF", "name")    
    # add devices VRFs nodes to graph
    for device_results in data:
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        # add vrfs:
        for vrf in device_results.get('vrfs', []):
            # add vrf nodes
            vrf_node = Node('VRF', name=vrf['vrf_name'], **vrf)
            graph.merge(vrf_node, "VRF", "name")
            # add relationshoip to device
            graph.merge(VRF_EXISTS_ON(vrf_node, device_node))
            
def add_interfaces_nodes_to_device(data):            
    for device_results in data:   
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        # add interfaces, subinterfaces and IPs
        for interface in device_results.get("interfaces", []):
            interface = interface.copy()
            log.info("Adding interface: {}".format(str(interface)))
            # form interface node name
            interface_uid = "{}:{}".format(device_hostname, interface["name"])
            # delete ip information:
            if 'ipv4_ips' in interface:
                _ = interface.pop('ipv4_ips')
            if 'ipv6_ips' in interface:
                _ = interface.pop('ipv6_ips')
            # add interface and subinterface nodes
            if not interface['is_subinterface']:
                # add interface node
                interface_node = Node('Interface', uid=interface_uid, **interface)
                graph.merge(interface_node, "Interface", "uid")
                # add relationship back to device
                graph.merge(INTERFACE_BELONGS_TO(interface_node, device_node))
            elif interface['is_subinterface']:
                # add subinterface node
                interface_node = Node('Interface', 'Subinterface', uid=interface_uid, **interface)
                graph.merge(interface_node, "Interface", "uid")
                # add relationship back to device
                graph.merge(INTERFACE_BELONGS_TO(interface_node, device_node))
                # get parent interface node
                parent_int_uid = "{}:{}".format(device_hostname, interface["name"].split(".")[0])
                parent_interface_node = graph.run(queries["get_interface_by_uid_and_hostname"].format(hostname=device_hostname, int_uid=parent_int_uid))
                parent_interface_node.forward() # need to move forward 1, otherwise current will be none
                parent_interface_node = parent_interface_node.current.to_subgraph()
                # add relationship back to parent interface
                graph.merge(PARENT_INTERFACE(interface_node, parent_interface_node))
                
def add_interfaces_link_to_vrfs(data):
    for device_results in data:   
        device_hostname = device_results['global_configuration']['hostname']
        # add interfaces and IPs
        for interface in device_results.get("interfaces", []):
            # form interface node name
            interface_uid = "{}:{}".format(device_hostname, interface['name'])
            interface_node = matcher.match("Interface", uid=interface_uid).first()
            # add relationship BELONGS_TO_VRFs from interface to VRF
            if 'vrf' in interface:
                vrf_node = matcher.match("VRF", name=interface['vrf']).first()
                ## add relationship
                graph.merge(BELONGS_TO_VRF(interface_node, vrf_node))
            else:
                vrf_node = matcher.match("VRF", name="global").first()
                graph.merge(BELONGS_TO_VRF(interface_node, vrf_node))
                
def add_ip_and_subnet_nodes_and_links_to_interfaces(data):
    for device_results in data:   
        device_hostname = device_results['global_configuration']['hostname']
        # add IPs
        for interface in device_results.get("interfaces", []):
            interface = interface.copy()
            # form interface node name
            interface_uid = "{}:{}".format(device_hostname, interface['name'])
            interface_node = matcher.match("Interface", uid=interface_uid).first()
            # get ip information:
            ipv4_ips, ipv6_ips = {}, {}
            if 'ipv4_ips' in interface:
                ipv4_ips = interface.pop('ipv4_ips')
            if 'ipv6_ips' in interface:
                ipv6_ips = interface.pop('ipv6_ips')                
            # add ipv4 addresses and subnets nodes
            for ip_address, ip_properties in ipv4_ips.items():
                ip_node = Node('IP_Address', 'IPv4_Address', ip=ip_address, **ip_properties)
                graph.merge(ip_node, "IPv4_Address", "ip")
                graph.merge(IP_ASSIGNED_TO(ip_node, interface_node))
                # add ipv4 subnet:
                ip_subnet_node = Node('IP_Subnet', 'IPv4_Subnet', subnet=ip_properties["subnet"])
                graph.merge(ip_subnet_node, "IPv4_Subnet", "subnet")
                # add relationship between subnet and ip
                graph.merge(PARENT_SUBNET(ip_node, ip_subnet_node))     
            # add ipv6 addresses and subnets nodes            
            for ip_address, ip_properties in ipv6_ips.items():
                ip_node = Node('IP_Address', 'IPv6_Address', ip=ip_address, **ip_properties)
                graph.merge(ip_node, "IPv6_Address", "ip")
                graph.merge(IP_ASSIGNED_TO(ip_node, interface_node))
                # add ipv6 subnet:
                ip_subnet_node = Node('IP_Subnet', 'IPv6_Subnet', subnet=ip_properties["subnet"])
                graph.merge(ip_subnet_node, "IPv6_Subnet", "subnet")
                # add relationship between subnet and ip
                graph.merge(PARENT_SUBNET(ip_node, ip_subnet_node))
        
def add_cdp_peerings(data):
    for device_results in data:   
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        for peer in device_results.get("cdp_peers", []):
            peer = peer.copy()
            interface_uid = "{}:{}".format(device_hostname, peer.pop('interface'))
            interface_node = matcher.match("Interface", uid=interface_uid).first()
            if not interface_node:
                log.error("add_cdp_peerings: {} local interface node not found, interface name - {}".format(device_hostname, interface_uid))
                continue
            # get peer nodes details
            peer_device_hostname = peer["peer_hostname"].split(".")[0]
            peer_interface_uid = "{}:{}".format(peer_device_hostname, peer['peer_interface'])
            peer_device_node = matcher.match("Device", hostname=peer_device_hostname).first()
            peer_interface_node = matcher.match("Interface", uid=peer_interface_uid).first()
            # add peer device and interface nodes if not found in graph
            if not peer_device_node:
                peer_device_node = Node('Device', hostname=peer_device_hostname)
                peer_interface_node = Node('Interface', name=peer_interface_uid)
                graph.merge(peer_device_node, "Device", "hostname")
                graph.merge(peer_interface_node, 'Interface', 'name')
                graph.merge(INTERFACE_BELONGS_TO(peer_interface_node, peer_device_node))    
                # add CDP relationship
                graph.merge(CDP_PEERING(peer_interface_node, interface_node))    
            # add peer device interface node to graph if not found in graph
            elif not peer_interface_node:
                peer_interface_node = Node('Interface', name=peer_interface_uid)
                graph.merge(peer_interface_node, 'Interface', 'name')
                graph.merge(INTERFACE_BELONGS_TO(peer_interface_node, peer_device_node))                    
                # add CDP relationship
                graph.merge(CDP_PEERING(peer_interface_node, interface_node))    
            # add CDP relationship
            else:
                graph.merge(CDP_PEERING(peer_interface_node, interface_node))    

def add_lldp_peerings(data):
    for device_results in data:   
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        for peer in device_results.get('lldp_peers', []):
            peer = peer.copy()
            interface_uid = "{}:{}".format(device_hostname, peer.pop('interface'))
            interface_node = matcher.match("Interface", uid=interface_uid).first()
            if not interface_node:
                log.error("add_lldp_peerings: {} local interface node not found, interface name - {}".format(device_hostname, interface_uid))
                continue
            # get peer nodes details
            peer_device_hostname = peer["peer_hostname"].split(".")[0]
            peer_interface_uid = "{}:{}".format(peer_device_hostname, peer['peer_interface'])
            peer_device_node = matcher.match("Device", hostname=peer_device_hostname).first()
            peer_interface_node = matcher.match("Interface", uid=peer_interface_uid).first()
            # add peer device and interface nodes if not found in graph
            if not peer_device_node:
                peer_device_node = Node('Device', hostname=peer_device_hostname)
                peer_interface_node = Node('Interface', name=peer_interface_uid)
                graph.merge(peer_device_node, "Device", "hostname")
                graph.merge(peer_interface_node, 'Interface', 'name')
                graph.merge(INTERFACE_BELONGS_TO(peer_interface_node, peer_device_node))    
                # add LLDP relationship
                graph.merge(LLDP_PEERING(peer_interface_node, interface_node))    
            # add peer device interface node to graph if not found in graph
            elif not peer_interface_node:
                peer_interface_node = Node('Interface', name=peer_interface_uid)
                graph.merge(peer_interface_node, 'Interface', 'name')
                graph.merge(INTERFACE_BELONGS_TO(peer_interface_node, peer_device_node))                    
                # add LLDP relationship
                graph.merge(LLDP_PEERING(peer_interface_node, interface_node))    
            # add LLDP relationship
            else:
                graph.merge(LLDP_PEERING(peer_interface_node, interface_node))   
                

def find_ip_subnet_node(ip, hostname=None):
    """
    find longest match subnet for IP address, 
    return py2neo Node object on success, None on failure
    
    Args:
        ip - IP address to find subnet for
        hostname - hostname of device where subnets should be connected too 
    """
    import ipaddress
    matched_subnets = {} # dictionary of {prefix_len: subnet} items
    ip_node = None
    # restrict to only subnets connected to particular hostname
    if hostname:
        ip_subnets = queries["get_subnets_by_device"].format(hostname=hostname)
    # get all subnets
    else:
        ip_subnets = matcher.match("IP_Subnet")
    # find subnets that contains given IP address
    if "." in ip: # IPv4 IP
        ip = ipaddress.IPv4Address(ip)
        for subnet in ip_subnets:
            if not "." in subnet["subnet"]:
                continue
            subnet_obj = ipaddress.IPv4Network(subnet["subnet"])
            if ip in subnet_obj:
                matched_subnets[subnet_obj.prefixlen] = subnet                    
    elif ":" in ip: # IPv6 IP
        ip = ipaddress.IPv6Address(ip)
        for subnet in ip_subnets:
            if not ":" in subnet["subnet"]:
                continue
            subnet_obj = ipaddress.IPv6Network(subnet["subnet"])
            if ip in subnet_obj:
                matched_subnets[subnet_obj.prefixlen] = subnet 
    else:
        log.error("find_ip_subnet_node: not an ip - '{}'".format(ip))
    # get longest mask prefixlen subnet
    if matched_subnets:
        longes_prefix_len = sorted(list(matched_subnets.keys()))[-1]
        # return longest prefixlen subnet
        return matched_subnets[longes_prefix_len]       

def add_bgp_process_node(data):
    for device_results in data:   
        # check if BGP config exists, continue if not
        bgp_config = device_results.get("bgp_config", {})
        bgp_asn = bgp_config.get("bgp_asn", None)
        if not bgp_asn:
            continue
        # find device hostname and node
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()   
        # add BGP ASN to graph
        bgp_asn_node = Node('BGP_ASN', asn=bgp_asn)
        graph.merge(bgp_asn_node, 'BGP_ASN', 'asn')
        graph.merge(BELONGS_TO_BGP_AS(device_node, bgp_asn_node))        
        # add BGP process node and link back to device
        bgp_process_uid = "{}.{}".format(device_hostname, bgp_asn)
        bgp_process_node = Node('BGP_Process', uid=bgp_process_uid, **bgp_config.get("global_config", {}))
        graph.merge(bgp_process_node, 'BGP_Process', 'uid')
        graph.merge(BGP_PROCESS_DEVICE(bgp_process_node, device_node))
        
        # add links between VRF nodes and BGP process
        for vrf_name, vrf_config in bgp_config.get("vrf_config", {}).items():
            vrf_node = matcher.match("VRF", name=vrf_name).first() 
            graph.merge(BGP_CONFIG(bgp_process_node, vrf_node, **vrf_config))
            
        # add BGP_Peering nodes for global peerings
        for neighbor_ip, config in bgp_config.get("neighbors", {}).items():
            # check if this neighbor is actually a peer group
            if config.get("is_peer_group", False):
                continue
            # check if this neighbor has peer-group attached
            if "peer_group" in config:
                peer_group_name = config["peer_group"]
                peer_group_config =  bgp_config["neighbors"][peer_group_name].copy()
                peer_group_config.update(config)
                config = peer_group_config
            # get vrf node:
            local_vrf_name = config["vrf"]
            local_vrf_node = matcher.match("VRF", name=local_vrf_name).first() 
            # find BGP peering source IP
            if "session_source_interface" in config:
                source_ip = config["session_source_interface"]
                source_ip_query = graph.run(queries["get_ip_by_interface_and_device"].format(interface_uid="{}:{}".format(
                    device_hostname, source_ip), hostname=device_hostname))
                # check IP type matches neighbor_ip - v4 or v6
                for item in source_ip_query.data():
                    ip_val = item["ip.ip"]
                    if "." in ip_val and "." in neighbor_ip:
                        source_ip = ip_val
                        break
                    elif ":" in ip_val and ":" in neighbor_ip:
                        source_ip = ip_val
                        break
                # get source ip node
                try:
                    source_ip_node = matcher.match("IP_Address", ip=source_ip).first()
                except TypeError:
                    log.error("add_bgp_process_node: Failed to obtain BGP peering source_ip for device - {}, source interface - {}\nPeer configuration:\n{}\nCypher query:{} ".format(
                            device_hostname, config["session_source_interface"], str(config), 
                            queries["get_ip_by_interface_and_device"].format(interface_uid="{}:{}".format(device_hostname, source_ip), hostname=device_hostname)
                        )
                    )    
                    continue                     
            else:
                # find parent subnet that connected to this device and link neighbor IP to it
                parent_subnet_node = find_ip_subnet_node(ip=neighbor_ip, hostname=device_hostname)
                # find local ip in same subnet as peer IP
                source_ip = graph.run(queries["get_ip_by_subnet_and_device"].format(subnet=parent_subnet_node["subnet"], hostname=device_hostname))
                try:
                    source_ip = source_ip.data()[0]["ip.ip"]
                except IndexError:
                    log.error("add_bgp_process_node: Failed to obtain BGP peering source_ip for device - {}, subnet - {}\nPeer configuration:\n{}\nCypher query:{} ".format(
                        device_hostname, parent_subnet_node["subnet"], str(config), queries["get_ip_by_subnet_and_device"].format(subnet=parent_subnet_node["subnet"], hostname=device_hostname)))    
                    continue                        
                # get source ip node
                source_ip_node = matcher.match("IP_Address", ip=source_ip).first()
            # try to find neighbor IP node
            neighbor_ip_node = matcher.match("IP_Address", ip=neighbor_ip).first()
            # create neighbor IP node if not exists
            if not neighbor_ip_node:
                if "." in neighbor_ip:
                    neighbor_ip_node = Node('IP_Address', 'IPv4_Address', ip=neighbor_ip, **{"sourced_from": "bgp_config"})
                    graph.merge(neighbor_ip_node, "IPv4_Address", "ip")
                elif ":" in neighbor_ip:
                    neighbor_ip_node = Node('IP_Address', 'IPv6_Address', ip=neighbor_ip, **{"sourced_from": "bgp_config"})
                    graph.merge(neighbor_ip_node, "IPv6_Address", "ip")
                # find parent subnet that connected to this device and link neighbor IP to it
                parent_subnet_node = find_ip_subnet_node(ip=neighbor_ip, hostname=device_hostname)
                if parent_subnet_node:
                    graph.merge(PARENT_SUBNET(neighbor_ip_node, parent_subnet_node))  
            # do some checks
            if not source_ip_node:
                log.error("add_bgp_process_node: Device - {}, Failed to find source IP for neighbor: {}".format(device_hostname, neighbor_ip))
                continue
            # add bgp peering node and links to it:
            bgp_peering_uid = "-".join(sorted([source_ip, neighbor_ip]))
            bgp_peering_node = Node('BGP_Peering', uid=bgp_peering_uid)
            graph.merge(bgp_peering_node, "BGP_Peering", "uid")
            # add links to peering IP nodes:
            graph.merge(BGP_PEERING_IP(bgp_peering_node, source_ip_node))
            graph.merge(BGP_PEERING_IP(bgp_peering_node, neighbor_ip_node)) 
            # add link to local bgp process
            graph.merge(BGP_CONFIG(bgp_process_node, bgp_peering_node, **config))            
            # add links to VRF
            graph.merge(BGP_PEERING_VRF(bgp_peering_node, local_vrf_node))
                
    
def add_bgp_peering_relationships_state(data):
    for device_results in data:        
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        for bgp_neighbor in device_results.get("bgp_neighbors_state", []):
            bgp_neighbor = bgp_neighbor.copy()
            try:
                peer_ip = bgp_neighbor.pop("neighbor")
            except KeyError: # if no bp state in source data, bgp_neighbors_state will add empty group due to start regexes has default values
                continue
            try:
                source_ip = bgp_neighbor.pop("session_source_ip")
            except KeyError:
                import pprint
                log.info("add_bgp_peers: failed to get session IPs from bgp peer results:\n{}".format(pprint.pformat(bgp_neighbor)))
                continue
            if "v4" in bgp_neighbor["afi"].lower():
                source_ip_node = matcher.match("IPv4_Address", ip=source_ip).first()        
                neighbor_ip_node = matcher.match("IPv4_Address", ip=peer_ip).first()
                # add peer IPv4 node to graph if not exists
                if not neighbor_ip_node:
                    neighbor_ip_node = Node('IP_Address', 'IPv4_Address', ip=peer_ip, **{"sourced_from": "bgp_peering"})
                    graph.merge(neighbor_ip_node, "IPv4_Address", "ip")
                    # add link to parent subnet
                    parent_subnet_node = find_ip_subnet_node(ip=peer_ip)
                    if parent_subnet_node:
                        graph.merge(PARENT_SUBNET(neighbor_ip_node, parent_subnet_node))
            elif "v6" in bgp_neighbor["afi"].lower():
                source_ip_node = matcher.match("IPv6_Address", ip=source_ip).first()    
                neighbor_ip_node = matcher.match("IPv6_Address", ip=peer_ip).first()
                # add peer IPv6 node to graph if not exists
                if not neighbor_ip_node:
                    neighbor_ip_node = Node('IP_Address', 'IPv6_Address', ip=peer_ip, **{"sourced_from": "bgp_peering"})
                    graph.merge(neighbor_ip_node, "IPv6_Address", "ip")
                    # add link to parent subnet
                    parent_subnet_node = find_ip_subnet_node(ip=peer_ip)
                    if parent_subnet_node:
                        graph.merge(PARENT_SUBNET(neighbor_ip_node, parent_subnet_node))
            # add peer BGP ASN to graph
            peer_asn = bgp_neighbor["remote_asn"]
            bgp_asn_node = Node('BGP_ASN', asn=peer_asn)
            graph.merge(bgp_asn_node, 'BGP_ASN', 'asn')
            # skip bgp session if no source ip node found found           
            if not source_ip_node:
                log.error("add_bgp_peers: no source ip node found - '{}', for device '{}'".format(source_ip, device_hostname))
                continue            
            # add bgp peering relationship
            graph.merge(BGP_PEERING_STATE(source_ip_node, neighbor_ip_node, **bgp_neighbor))
                
                
def add_vlan_nodes_and_link_with_interfaces(data):
    for device_results in data:        
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        # add vlan nodes out of configuration
        for vlan in device_results.get("vlans_config", []):      
            vlan_id = vlan.pop("vid")
            vlan_node = Node('VLAN', vid=vlan_id, **{"L2_DOMAIN": "Default"})
            graph.merge(vlan_node, "VLAN", "vid")
            graph.merge(VLAN_EXISTS_ON(vlan_node, device_node, **{"vlan_name": vlan.get("name", "")}))
        # add vlan nodes and relationships out of interfaces configuration
        for interface in device_results.get("interfaces", []):
            interface = interface.copy()
            # form interface node name
            interface_uid = "{}:{}".format(device_hostname, interface['name'])
            interface_node = matcher.match("Interface", uid=interface_uid).first()
            if not interface_node:
                log.error("add_vlan_nodes_and_link_with_interfaces: failed to find interface node, name - '{}'".format(interface_node))
                continue
            # add access vlan relationship
            if "access_vlan" in interface:
                vlan_id = interface["access_vlan"]
                vlan_node = matcher.match("VLAN", vid=vlan_id).first()
                if not vlan_node:
                    vlan_node = Node('VLAN', vid=vlan_id, **{"L2_DOMAIN": "Default"})
                    graph.merge(vlan_node, "VLAN", "vid")
                graph.merge(VLAN_CONFIGURED_AS_ACCESS(vlan_node, interface_node))
            # add voice vlan relationship
            if "voice_vlan" in interface:
                vlan_id = interface["voice_vlan"]
                vlan_node = matcher.match("VLAN", vid=vlan_id).first()
                if not vlan_node:
                    vlan_node = Node('VLAN', vid=vlan_id, **{"L2_DOMAIN": "Default"})
                    graph.merge(vlan_node, "VLAN", "vid")
                graph.merge(VLAN_CONFIGURED_AS_VOICE(vlan_node, interface_node))
            # add trunk vlans relationships
            if "trunked_vlans" in interface:
                for vlan_id in interface["trunked_vlans"]:
                    vlan_node = matcher.match("VLAN", vid=vlan_id).first()
                    if not vlan_node:
                        vlan_node = Node('VLAN', vid=vlan_id, **{"L2_DOMAIN": "Default"})
                        graph.merge(vlan_node, "VLAN", "vid")
                    graph.merge(VLAN_CONFIGURED_AS_TRUNK(vlan_node, interface_node))                    
            
def add_hardware_data(data):
    for device_results in data:        
        device_hostname = device_results['global_configuration']['hostname']
        device_node = matcher.match("Device", hostname=device_hostname).first()
        hardware_data = device_results.get("hardware", {})
        if not "hardware_chassis" in hardware_data:
            log.warning("add_hardware_data: no chassis information found for device - {}".format(device_hostname))
            continue
        # add chassis node:
        parameters = {
            "chassis"         : hardware_data["hardware_chassis"],
            "inventory_items" : json.dumps(hardware_data["inventory_items"], sort_keys=True, indent=4)
        }
        shassis_node = Node('Chassis', uid="{}:Chassis".format(device_hostname), **parameters)
        graph.merge(shassis_node, "Chassis", "uid")
        # add link between device and chassis nodes
        graph.merge(HARDWARE(device_node, shassis_node))   
        
                
# run functions
def run():
    pass

# add_devices_nodes(result)    
# add_vrfs_nodes(result)    
# add_interfaces_nodes_to_device(result)    
# add_interfaces_link_to_vrfs(result)    
# add_ip_and_subnet_nodes_and_links_to_interfaces(result)    
# add_cdp_peerings(result)
# add_lldp_peerings(result)
# add_bgp_process_node(result)
# add_bgp_peering_relationships_state(result)
# add_vlan_nodes_and_link_with_interfaces(result)
# add_hardware_data(result)