
import nmap

last_results = []

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 3389: "RDP"
}

def scan_network(ip_range):
    scanner = nmap.PortScanner()
    try:
        scanner.scan(hosts=ip_range, arguments='-p ' + ','.join(map(str, COMMON_PORTS.keys())))
    except Exception as e:
    
        return {'error': str(e)}

    result = []
    for host in scanner.all_hosts():
        if 'tcp' in scanner[host]:
            for port in scanner[host]['tcp']:
                protocol = COMMON_PORTS.get(port, 'Unknown')
                result.append({
                    'ip': host,
                    'state': scanner[host].state(),
                    'port': port,
                    'protocol': protocol
                })
    global last_results
    last_results = result
    return result
