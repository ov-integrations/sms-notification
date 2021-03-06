import json

from sms_notifservice import SmsNotifService

with open('settings.json', "rb") as SFile:
    pwd_data = json.loads(SFile.read().decode('utf-8'))

ov_url = "https://" + pwd_data["oneVizionUrl"]
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

notification_service = SmsNotifService(service_id, process_id, ov_url, ov_login, ov_pwd, phone_number_field,
                                       awsAccessKeyId, awsSecretAccessKey, awsRegion, max_attempts,
                                       next_attempt_delay)
notification_service.start()
