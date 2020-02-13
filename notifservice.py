import time
from abc import ABC, abstractmethod

from integration_log import IntegrationLog, LogLevel
from notifqueue_api import NotifQueueApi
from notifqueue_record import NotifQueueRecord
from notifqueue_status import NotifQueueStatus


class NotificationService(ABC):

    def __init__(self, service_id, process_id, ov_url, ov_username, ov_pwd, max_attempts=1, next_attempt_delay=30):
        self._notif_queue_api = NotifQueueApi(service_id, ov_url, ov_username, ov_pwd)
        self._max_attempts = max_attempts
        self._next_attempt_delay = next_attempt_delay
        self._integration_log = IntegrationLog(process_id, ov_url, ov_username, ov_pwd)

    def start(self):
        self._integration_log.add_log(LogLevel.INFO.log_level_name, "Starting Integration")
        attempts = 0

        self._integration_log.add_log(LogLevel.INFO.log_level_name, "Receiving Notif Queue")
        notif_queue_json = self._notif_queue_api.get_notif_queue()
        self._integration_log.add_log(LogLevel.DEBUG.log_level_name, "Notif Queue json data", str(notif_queue_json))

        try:
            notif_queue = self._convert_notif_queue_json_to_list(notif_queue_json)
        except Exception as e:
            self._integration_log.add_log(LogLevel.ERROR.log_level_name, "Can't convert Notif Queue json data to list",
                                          str(e))
            raise Exception("Can't convert Notif Queue json data to list") from e

        prepared_notif_queue = []
        try:
            prepared_notif_queue = self._prepare_notif_queue(notif_queue)
        except Exception as e:
            self._integration_log.add_log(LogLevel.ERROR.log_level_name, "Can't prepare Notif Queue to send",
                                          str(e))
            raise Exception("Can't prepare Notif Queue to send") from e

        self._integration_log.add_log(LogLevel.INFO.log_level_name,
                                      "Notif Queue size: [{}]".format(len(prepared_notif_queue)))

        while len(prepared_notif_queue) > 0 and attempts < self._max_attempts:
            if attempts > 0:
                self._integration_log.add_log(LogLevel.INFO.log_level_name,
                                              "Attempt Number [{}]".format(attempts + 1))

            for notif_queue_rec in prepared_notif_queue:
                self._integration_log.add_log(LogLevel.INFO.log_level_name,
                                              "Sending Notif Queue Record with id = [{}]".format(
                                                  notif_queue_rec.notif_queue_id))
                notif_queue_rec.status = NotifQueueStatus.SENDING.name
                self._notif_queue_api.update_notif_queue_rec_status_by_object(notif_queue_rec)

                try:
                    self.send_notification(notif_queue_rec)
                except Exception as e:
                    self._notif_queue_api.add_new_attempt(notif_queue_rec.notif_queue_id, str(e))
                    self._integration_log.add_log(LogLevel.ERROR.log_level_name,
                                                  "Can't send Notif Queue Record with id = [{}]".format(
                                                      notif_queue_rec.notif_queue_id),
                                                  str(e))

                    if attempts + 1 == self._max_attempts:
                        notif_queue_rec.status = NotifQueueStatus.FAIL.name
                    else:
                        notif_queue_rec.status = NotifQueueStatus.FAIL_WILL_RETRY.name

                else:
                    notif_queue_rec.status = NotifQueueStatus.SUCCESS.name

                self._notif_queue_api.update_notif_queue_rec_status_by_object(notif_queue_rec)

            prepared_notif_queue = list(
                filter(lambda rec: rec.status != NotifQueueStatus.SUCCESS.name, prepared_notif_queue))
            attempts += 1

            if len(prepared_notif_queue) > 0 and self._max_attempts > attempts:
                self._integration_log.add_log(LogLevel.WARNING.log_level_name,
                                              "Can't send [{0}] notifications. Next try in [{1}] seconds".format(
                                                  len(prepared_notif_queue),
                                                  self._next_attempt_delay))
                time.sleep(self._next_attempt_delay)

        if len(prepared_notif_queue) > 0:
            self._integration_log.add_log(LogLevel.ERROR.log_level_name,
                                          "Can't send [{}] notifications. All attempts have been exhausted.".format(
                                              len(prepared_notif_queue)))

    @staticmethod
    def _convert_notif_queue_json_to_list(json_data):
        notif_queue = []
        for json_obj in json_data:
            notif_queue.append(NotifQueueRecord(json_obj))
        return notif_queue

    @abstractmethod
    def send_notification(self, notif_queue_record):
        pass

    def _prepare_notif_queue(self, notif_queue):
        return notif_queue
