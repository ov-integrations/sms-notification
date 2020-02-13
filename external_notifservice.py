import boto3

from curl import Curl
from integration_log import LogLevel
from notifservice import NotificationService


class ExternalNotifService(NotificationService):

    def __init__(self, service_id, process_id, ov_url, ov_username, ov_pwd, phone_number_field_name, access_key_id,
                 secret_access_key,
                 aws_region, max_attempts=1, next_attempt_delay=30):
        super().__init__(service_id, process_id, ov_url, ov_username, ov_pwd, max_attempts, next_attempt_delay)
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._aws_region = aws_region
        self._phone_number_field_name = phone_number_field_name
        self._user_trackor = UserTrackor(ov_url, ov_username, ov_pwd)
        self._url = ov_url

    def send_notification(self, notif_queue_record):
        client = boto3.client(
            "sns",
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._secret_access_key,
            region_name=self._aws_region
        )

        tid = 1000970167
        phone_number = self._user_trackor.get_phone_number_by_field_name_and_trackor_id(self._phone_number_field_name,
                                                                                        tid)
        attachments = "Attachments: "
        for blob_id in notif_queue_record.blob_data_ids:
            attachments = attachments + self._url + "/efiles/EFileGetBlobFromDb.do?id=" + str(blob_id) + " \r\n"

        msg = notif_queue_record.subj + " " + notif_queue_record.msg
        if len(attachments) > 0:
            msg = msg + " " + attachments

        self._integration_log.add_log(LogLevel.INFO.log_level_name,
                                      "Sending SMS to [{}] phone number".format(phone_number),
                                      "Message Text: [{}]".format(msg))
        # Send your sms message.
        response = client.publish(
            PhoneNumber=phone_number,
            Message=msg
        )

        self._integration_log.add_log(LogLevel.DEBUG.log_level_name,
                                      "Received response from SNS",
                                      "Response: [{}]".format(response))
        try:
            http_status_code = int(response["ResponseMetadata"]["HTTPStatusCode"])
        except Exception as e:
            self._integration_log.add_log(LogLevel.ERROR.log_level_name,
                                          "Incorrect response from SNS",
                                          response)
            raise Exception("Incorrect response from SNS") from e

        if http_status_code >= 400:
            self._integration_log.add_log(LogLevel.ERROR.log_level_name,
                                          "Error when sending SMS. HTTPStatusCode: [{}]".format(http_status_code),
                                          "Response: [{}]".format(response))
            raise Exception("Error when sending SMS. HTTPStatusCode: [{}]".format(http_status_code)) from e


class UserTrackor:

    def __init__(self, url, username, password):
        self._url = url
        self._username = username
        self._password = password
        self._headers = {'content-type': 'application/json'}

    def get_phone_number_by_field_name_and_trackor_id(self, field_name, tid):
        url = self._url + "/api/v3/trackors/" + str(tid) + "?fields=" + field_name
        curl = Curl('GET', url, headers=self._headers, auth=(self._username, self._password))
        if len(curl.errors) > 0:
            raise Exception(curl.errors)
        return curl.jsonData[field_name]
