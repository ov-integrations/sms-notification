import re
import boto3
from onevizion import NotificationService, LogLevel

from curl import Curl

HTTPS = "https://"
HTTP = "http://"


def get_scheme_url(url):
    if url.startswith(HTTPS) or url.startswith(HTTP):
        return url
    else:
        return HTTPS + url


def get_url_without_scheme(url):
    if url.startswith(HTTPS) or url.startswith(HTTP):
        return url.replace(HTTPS, "").replace(HTTP, "")
    else:
        return url


class SmsNotifService(NotificationService):

    def __init__(self, service_id, ov_url, ov_username, ov_pwd, phone_number_field_name, access_key_id,
                 secret_access_key, aws_region, max_attempts, next_attempt_delay, process_id, log_level):
        super().__init__(serviceId=service_id, URL=get_url_without_scheme(ov_url), userName=ov_username,
                         password=ov_pwd, maxAttempts=max_attempts, nextAttemptDelay=next_attempt_delay,
                         processId=process_id, logLevel=log_level)
        self._url = get_url_without_scheme(ov_url)
        self._scheme_url = get_scheme_url(ov_url)
        self._phone_number_field_name = phone_number_field_name
        self._user_trackor = UserTrackor(self._scheme_url, ov_username, ov_pwd)
        self._client = self._create_client(access_key_id, secret_access_key, aws_region)

    def _create_client(self, access_key_id, secret_access_key, aws_region):
        if aws_region == "test":
            self._integrationLog.add(LogLevel.WARNING,
                                     "Warning! The stub is used instead of the real client for sending SMS")
            return StubClient()
        else:
            return boto3.client(
                "sns",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=aws_region
            )

    def sendNotification(self, notif_queue_record):
        if not (hasattr(notif_queue_record, 'phone_number')) or notif_queue_record.phone_number is None:
            raise Exception(
                "Notif Queue Record with ID [{}] has no phone number".format(notif_queue_record.notifQueueId))

        attachments = "Attachments: "
        for blob_id in notif_queue_record.blobDataIds:
            attachments = attachments + self._scheme_url + "/efiles/EFileGetBlobFromDb.do?id=" + str(blob_id) + " "

        msg = notif_queue_record.subj + " " + notif_queue_record.msg + " " + self._url
        if len(notif_queue_record.blobDataIds) > 0:
            msg = msg + " " + attachments

        phone_number = self._format_phone_number(notif_queue_record.phone_number)
        self._check_phone_number(notif_queue_record.phone_number, phone_number)

        self._integrationLog.add(LogLevel.INFO,
                                 "Sending SMS to [{}] phone number".format(phone_number),
                                 "Message Text: [{}]".format(msg))
        # Send your sms message.
        response = self._client.publish(
            PhoneNumber=phone_number,
            Message=msg,
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            }
        )

        self._integrationLog.add(LogLevel.DEBUG,
                                 "Received response from SNS",
                                 "Response: [{}]".format(response))
        try:
            http_status_code = int(response["ResponseMetadata"]["HTTPStatusCode"])
        except Exception as e:
            self._integrationLog.add(LogLevel.ERROR, "Incorrect response from SNS", response)
            raise Exception("Incorrect response from SNS") from e

        if http_status_code >= 400:
            self._integrationLog.add(LogLevel.ERROR,
                                     "Error when sending SMS. HTTPStatusCode: [{}]".format(http_status_code),
                                     "Response: [{}]".format(response))
            raise Exception("Error when sending SMS. HTTPStatusCode: [{}]".format(http_status_code))

    def _prepareNotifQueue(self, notif_queue):
        user_ids = list(map(lambda rec: rec.userId, notif_queue))
        if None in user_ids:
            for notif_queue_rec in notif_queue:
                if notif_queue_rec.userId is None:
                    self._integrationLog.add(LogLevel.ERROR,
                                             "Notif Queue Record doesn't have User ID. Notif Queue ID: [{}]".format(
                                                 str(notif_queue_rec.notifQueueId)))
            user_ids = [user_id for user_id in user_ids if user_id]

        if len(user_ids) > 0:
            users = dict((user["userId"], user) for user in self._user_trackor.get_users_by_ids(user_ids))

            for notif_queue_rec in notif_queue:
                if notif_queue_rec.userId is not None:
                    notif_queue_rec.phone_number = self._get_phone_number(users[notif_queue_rec.userId])

        return notif_queue

    def _get_phone_number(self, user):
        if self._phone_number_field_name:
            try:
                phone_number = self._user_trackor.get_phone_number_by_field_name_and_trackor_id(
                    self._phone_number_field_name,
                    user["trackorId"])
            except Exception as e:
                self._integrationLog.add(LogLevel.ERROR, "Can't get Phone Number from User Trackor. "
                                                         "Trackor ID = [{}]".format(str(user["trackorId"])),
                                        str(e))
        else:
            phone_number = user["phoneNumber"]

        return phone_number
    
    def _format_phone_number(self, phone_number):
        formatted_phone_number  = phone_number.replace("-", "")
        formatted_phone_number = formatted_phone_number.replace("(", "").replace(")", "")
        if formatted_phone_number[0] != "+":
            formatted_phone_number = "+1" + formatted_phone_number
            self._integrationLog.add(LogLevel.WARNING,
                                     "Warning! +1 prefix added to phone number. Final value: [{}]".format(formatted_phone_number))
        
        return formatted_phone_number
    
    def _check_phone_number(self, phone_number, formatted_phone_number):
        if re.fullmatch("\+\d{2,15}", formatted_phone_number) is None:
            self._integrationLog.add(LogLevel.ERROR,
                                     "Incorrect Phone Number format.",
                                     "Original Phone Number: [{0}]\nProcessed Phone Number: [{1}]".format(phone_number, formatted_phone_number))
            raise Exception("Incorrect Phone Number format. Phone Number: [{}]".format(phone_number))

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

    def get_users_by_ids(self, user_ids):
        user_ids = list(set(user_ids))
        url = self._url + "/api/internal/users?user_ids="
        url = url + ','.join([str(user_id) for user_id in user_ids])

        curl = Curl('GET', url, headers=self._headers, auth=(self._username, self._password))
        if len(curl.errors) > 0:
            raise Exception(curl.errors)
        return curl.jsonData


class StubClient:

    def publish(self, **kwargs):
        return {"ResponseMetadata": {"HTTPStatusCode": 203}}
