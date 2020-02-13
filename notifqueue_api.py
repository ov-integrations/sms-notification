from curl import Curl


class NotifQueueApi:
    def __init__(self, service_id, url, user_name, password):
        self._service_id = service_id
        self._url = url
        self._user_name = user_name
        self._password = password
        self._headers = {'content-type': 'application/json'}

    def get_notif_queue(self):
        url = self._url + "/api/internal/notif/queue?service_id=" + str(self._service_id)
        curl = Curl('GET', url, headers=self._headers, auth=(self._user_name, self._password))
        if len(curl.errors) > 0:
            raise Exception(curl.errors)
        return curl.jsonData

    def update_notif_queue_rec_status(self, notif_queue_rec_id, status):
        url = self._url + "/api/internal/notif/queue/" + str(notif_queue_rec_id) + "/update_status?status=" + status
        curl = Curl('PATCH', url, headers=self._headers, auth=(self._user_name, self._password))
        if len(curl.errors) > 0:
            raise Exception(curl.errors)

    def add_new_attempt(self, notif_queue_rec_id, error_message):
        url = self._url + "/api/internal/notif/queue/" + str(notif_queue_rec_id) + "/attempts?error_code=" + error_message
        curl = Curl('POST', url, headers=self._headers, auth=(self._user_name, self._password))
        if len(curl.errors) > 0:
            raise Exception(curl.errors)

    def update_notif_queue_rec_status_by_object(self, notif_queue_rec):
        self.update_notif_queue_rec_status(notif_queue_rec.notif_queue_id, notif_queue_rec.status)
