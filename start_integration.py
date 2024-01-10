import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "python_dependencies.txt"])

import json
from jsonschema import validate
from sms_notifservice import SmsNotifService
from module_error import ModuleError

with open("settings.json", "rb") as settings_file:
    settings_json = json.loads(settings_file.read().decode("utf-8"))

with open("settings_schema.json", "rb") as settings_schema_file:
    settings_schema_json = json.loads(settings_schema_file.read().decode("utf-8"))

try:
    validate(instance=settings_json, schema=settings_schema_json)
except Exception as e:
    raise ModuleError("Incorrect value in the settings file\n{}".format(str(e)))
    
phone_number_field = settings_json["phoneNumberField"] if "phoneNumberField" in settings_json else ""

with open("ihub_parameters.json", "rb") as ihub_params_file:
    ihub_params_json = json.loads(ihub_params_file.read().decode("utf-8"))

notification_service = SmsNotifService(settings_json["serviceId"],
                                       settings_json["ovUrl"], 
                                       settings_json["ovAccessKey"],
                                       settings_json["ovSecretKey"],
                                       phone_number_field,
                                       settings_json["awsAccessKeyId"],
                                       settings_json["awsSecretAccessKey"],
                                       settings_json["awsRegion"], 
                                       settings_json["maxAttempts"],
                                       settings_json["nextAttemptDelay"], 
                                       ihub_params_json["processId"],
                                       ihub_params_json["logLevel"])
notification_service.start()
