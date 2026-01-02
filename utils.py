import subprocess
from .models import Device, Group

def scan_ipmi(network: str) -> list:
    """扫描IPMI设备（需ipmitool已安装）"""
    cmd = f"ipmitool -I lanplus -H {network} -U admin -P password mc info 2>/dev/null"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if "IPMI" in output.stdout:
        return [{"ip": network, "protocol": "ipmi", "username": "admin", "password": "password"}]
    return []

def scan_snmp(network: str) -> list:
    """扫描SNMP设备（需snmpwalk已安装）"""
    cmd = f"snmpwalk -v2c -c public {network} 1.3.6.1.2.1.1.5.0 2>/dev/null"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if "sysName" in output.stdout:
        return [{"ip": network, "protocol": "snmp", "username": "public", "password": "public"}]
    return []

def get_device_metrics(ip: str, protocol: str, username: str, password: str) -> dict:
    """获取设备实时指标（简化版）"""
    if protocol == "ipmi":
        # 实际用ipmitool获取
        cpu = 75  # 示例值
        memory = 65
    else:  # snmp
        # 实际用snmpget获取
        cpu = 82
        memory = 88
    return {"cpu": cpu, "memory": memory}
