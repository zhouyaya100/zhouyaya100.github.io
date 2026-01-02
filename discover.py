import sys
import ipaddress
from app.utils import scan_ipmi, scan_snmp

def main():
    network = sys.argv[1]  # 例如: 192.168.1.0/24
    for ip in ipaddress.IPv4Network(network):
        ip_str = str(ip)
        # 跳过网关/广播地址
        if ip_str in ["0.0.0.0", "255.255.255.255"]:
            continue
        
        # 尝试IPMI扫描
        ipmi_devices = scan_ipmi(ip_str)
        if ipmi_devices:
            print(f"Found IPMI device: {ip_str}")
            # 保存到数据库（简化，实际需用ORM）
            with open("discovered.csv", "a") as f:
                f.write(f"{ip_str},ipmi,admin,password,Default\n")
        
        # 尝试SNMP扫描
        snmp_devices = scan_snmp(ip_str)
        if snmp_devices:
            print(f"Found SNMP device: {ip_str}")
            with open("discovered.csv", "a") as f:
                f.write(f"{ip_str},snmp,public,public,Default\n")

if __name__ == "__main__":
    main()
