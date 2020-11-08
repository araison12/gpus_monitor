import os
import yaml

# SMTP SERVER CONFIG


USER = os.environ.get(
    "GPUSMONITOR_MAIL_USER"
)  # for the moment, only accessible from SIC08005 (all users)
PASSWORD = os.environ.get(
    "GPUSMONITOR_MAIL_PASSWORD"
)  # for the moment, only accessible from SIC08005 (all users)
PORT = 465
SMTP_SERVER = "smtp.gmail.com"

# SCANNING RATE

WAITING_TIME = 0.5  # min
PROCESS_AGE = 2  # min

# PERSONS TO INFORM
def persons_to_inform():
    with open("../../persons_to_inform.yaml", "r") as yaml_file:
        PERSON_TO_INFORM_LIST = yaml.load(yaml_file, Loader=yaml.FullLoader)["list"]
    return PERSON_TO_INFORM_LIST
