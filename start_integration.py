import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'python_dependencies.txt'])

import json
from jsonschema import validate
from sms_notifservice import SmsNotifService
from integration_error import IntegrationError

with open('settings.json', "rb") as SFile:
    pwd_data = json.loads(SFile.read().decode('utf-8'))

with open('settings_schema.json', "rb") as SFile:
    data_schema = json.loads(SFile.read().decode('utf-8'))

try:
    validate(instance=pwd_data, schema=data_schema)
except Exception as e:
    raise IntegrationError("Incorrect value in the settings file\n{}".format(str(e)))

ov_url = pwd_data["oneVizionUrl"]
ov_login = pwd_data["oneVizionLogin"]
ov_pwd = pwd_data["oneVizionPwd"]
service_id = pwd_data["serviceId"]
phone_number_field = pwd_data["phoneNumberField"]

awsAccessKeyId = pwd_data["awsAccessKeyId"]
awsSecretAccessKey = pwd_data["awsSecretAccessKey"]
awsRegion = pwd_data["awsRegion"]

max_attempts = pwd_data["maxAttempts"]
next_attempt_delay = pwd_data["nextAttemptDelay"]

with open('ihub_parameters.json', "rb") as PFile:
    ihub_data = json.loads(PFile.read().decode('utf-8'))

process_id = ihub_data['processId']
log_level = ihub_data['logLevel']

notification_service = SmsNotifService(service_id, ov_url, ov_login, ov_pwd, phone_number_field,
                                       awsAccessKeyId, awsSecretAccessKey, awsRegion, max_attempts,
                                       next_attempt_delay, process_id, log_level)
notification_service.start()
