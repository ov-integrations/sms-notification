import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "python_dependencies.txt"])

import json
from sms_notifservice import SmsNotifService

with open("settings.json", "rb") as settings_file:
    settings_json = json.loads(settings_file.read().decode("utf-8"))

phone_number_field = settings_json["phoneNumberField"] if "phoneNumberField" in settings_json else ""

with open("ihub_parameters.json", "rb") as ihub_params_file:
    ihub_params_json = json.loads(ihub_params_file.read().decode("utf-8"))

notification_service = SmsNotifService(settings_json["serviceId"],
                                       settings_json["oneVizionUrl"], 
                                       settings_json["oneVizionLogin"],
                                       settings_json["oneVizionPwd"],
                                       phone_number_field,
                                       settings_json["awsAccessKeyId"],
                                       settings_json["awsSecretAccessKey"],
                                       settings_json["awsRegion"], 
                                       settings_json["maxAttempts"],
                                       settings_json["nextAttemptDelay"], 
                                       ihub_params_json["processId"],
                                       ihub_params_json["logLevel"])
notification_service.start()
