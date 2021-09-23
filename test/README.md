#Test

You can use "test" as AWS Region to test the Integration. It works as the same but SMS messages are not sent.

You can use Rules from components.xml for automated testing.

TEST_INTEGRATION_SMS_NOTIFICATION Rule is used to create notifications.
TEST_INTEGRATION_SMS_NOTIFICATION_RESULTS is used to check status of the Notif Queue records and Integration Run.

Before enabling the Rules, change User ID and Notif Service ID in the Rules to the ones you use for testing.
