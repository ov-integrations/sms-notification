class NotifQueueRecord:

    def __init__(self, json_object):
        self.notif_queue_id = json_object['notifQueueId']
        self.user_id = json_object['userId']
        self.sender = json_object['sender']
        self.to_address = json_object['toAddress']
        self.cc = json_object['cc']
        self.bcc = json_object['bcc']
        self.subj = json_object['subj']
        self.reply_to = json_object['replyTo']
        self.created_ts = json_object['createdTs']
        self.status = json_object['status']
        self.msg = json_object['msg']
        self.html = json_object['html']
        self.blob_data_ids = json_object['blobDataIds']
