def get_sidelink_ip(cv2x_ip_base, ifname):
    import fcntl
    import ipaddress
    import socket
    import struct

    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def get_netmask(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x891b,
            struct.pack('256s', ifname)
        )[20:24])

    iface_ip = get_ip_address(ifname)
    netmask = get_netmask(ifname)

    cv2x_iface = ipaddress.ip_interface(f"{iface_ip}/{netmask}")
    base = int(cv2x_iface.ip) - int(cv2x_iface.network.network_address)

    sidelink_network = ipaddress.ip_network(f"{cv2x_ip_base}/{netmask}")
    sidelink_ip = ipaddress.ip_address(int(sidelink_network.network_address) + base)
    return str(sidelink_ip)
