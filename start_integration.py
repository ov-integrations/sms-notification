import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'python_dependencies.txt'])

import json
from sms_notifservice import SmsNotifService

with open('settings.json', "rb") as SFile:
    settings_data = json.loads(SFile.read().decode('utf-8'))

with open('ihub_parameters.json', "rb") as PFile:
    ihub_data = json.loads(PFile.read().decode('utf-8'))

notification_service = SmsNotifService(settings_data["serviceId"], settings_data["oneVizionUrl"], 
                                       settings_data["oneVizionLogin"], settings_data["oneVizionPwd"], settings_data["phoneNumberField"],
                                       settings_data["awsAccessKeyId"], settings_data["awsSecretAccessKey"], settings_data["awsRegion"], 
                                       settings_data["maxAttempts"], settings_data["nextAttemptDelay"], 
                                       ihub_data['processId'], ihub_data['logLevel'])
notification_service.start()
