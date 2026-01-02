from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import init_db, Device, Group
from .utils import scan_ipmi, scan_snmp, get_device_metrics
from .schemas import DeviceCreate, AlertResponse
import csv
import io
import os

app = FastAPI()

# CORS配置（前端跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
init_db()

@app.post("/devices/batch_add")
async def batch_add_devices(file: UploadFile = File(...)):
    """批量导入设备（CSV格式）"""
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    
    devices = []
    for row in reader:
        # 验证必填字段
        if not all(k in row for k in ["ip", "protocol", "username", "password"]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        devices.append(DeviceCreate(**row))
    
    # 保存到数据库（示例，实际需处理密码加密）
    for device in devices:
        Device.create(device.ip, device.protocol, device.username, device.password, device.group)
    
    return {"status": "success", "count": len(devices)}

@app.post("/devices/discover")
async def discover_network(network: str):
    """自动发现网段设备（如 192.168.1.0/24）"""
    # 调用扫描脚本（异步执行，避免阻塞）
    os.system(f"python3 app/discover.py {network}")
    return {"status": "scanning", "network": network}

@app.get("/alerts")
async def get_alerts():
    """获取当前告警（CPU > 80% 或 内存 > 90%）"""
    alerts = []
    for device in Device.select():
        metrics = get_device_metrics(device.ip, device.protocol, device.username, device.password)
        if metrics["cpu"] > 80 or metrics["memory"] > 90:
            alerts.append(AlertResponse(
                device_ip=device.ip,
                metric=metrics,
                severity="P1" if metrics["cpu"] > 85 else "P2"
            ))
    return alerts

# 启动命令: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
