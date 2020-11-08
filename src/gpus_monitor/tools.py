import os
import ssl
import time
import config
import psutil
import smtplib
import netifaces as ni
from socket import gaierror
from pynvml.smi import nvidia_smi
from email.message import EmailMessage


def send_mail(subject, message, receiver):

    context = ssl.create_default_context()
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = config.USER
    msg["To"] = receiver

    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.PORT, context=context) as server:
        server.login(config.USER, config.PASSWORD)
        server.send_message(msg)


def get_machine_local_ip():
    interfaces = ni.interfaces()
    for inter in interfaces:
        if ni.ifaddresses(inter)[ni.AF_INET][0]["addr"][:7] == "194.167":
            return ni.ifaddresses(inter)[ni.AF_INET][0]["addr"]


def get_machine_infos():
    infos_uname = os.uname()

    return {
        "OS_TYPE": infos_uname[0],
        "MACHINE_NAME": infos_uname[1],
        "LOCAL_IP": get_machine_local_ip(),
    }


def gpus_snap_info():
    nvsmi = nvidia_smi.getInstance()
    return nvsmi.DeviceQuery(
        "memory.free,memory.total,memory.used,compute-apps,temperature.gpu,driver_version,timestamp,name"
    )


def process_info(pid):
    try:
        process = psutil.Process(pid)

        return {
            "pid": pid,
            "owner": process.username(),
            "executed_cmd": process.cmdline(),
            "from": process.cwd(),
            "since": process.create_time(),
            "is_running": process.is_running(),
            "cpu_core_required": f"{process.cpu_num()}/{os.cpu_count()} logic cores ({process.cpu_num()*100/os.cpu_count()}%)",
        }
    except psutil.NoSuchProcess:
        return None