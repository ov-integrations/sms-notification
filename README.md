# sms-notification

SMS-Notification is an integration that works as an external Notification Service for sending SMS notifications. It uses 
Amazon Simple Notification Service (SNS) to send SMS.

## Requirements
- Python 3
- Requests - [library for python](https://requests.readthedocs.io/en/master/)
- boto3 - [Boto is the Amazon Web Services (AWS) SDK for Python](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## AWS Configuration
1. Log into AWS console
2. Create an IAM policy using SNSPublishSMSOnly.json
3. Create an IAM user and store credentials
4. Attach this new profile to the user
5. In SNS section, choose Text messaging (SMS) and change default message type from Promotional to Transactional


## Usage
1. Create a new Notification Service in OneVizion. All settings of this service are ignored by Integration, use random values for required fields
2. Install this integration
3. Create dedicated account for integration with following privs:
   * WEB_SERVICES R
   * ADMIN_NOTIF_QUEUE RE
   * ADMIN_USERS R
   * ADMIN_INTEGRATION_LOG RA
   
   The following privs are required if phoneNumberField is used:
   * \<User Trackor Type\> R
   * \<User Trackor Type Tab containing phoneNumberField\> R

4. Fill the integration settings file:
   - oneVizionUrl - OneVizion URL
   - oneVizionLogin - OneVizion Login
   - oneVizionPwd - OneVizion Password
   - serviceId - ID of the Notification Service created at step 2
   - phoneNumberField (Optional. Needed when there are no phones numbers in User Settings) - The name of the field which contains the phone number of the recipient. Recipient is a user trackor related with User ID from the Notif Queue record.
   - awsAccessKeyId - AWS Access Key ID
   - awsSecretAccessKey - AWS Secret Access Key
   - maxAttempts - The number of attempts to send SMS
   - nextAttemptDelay - The delay in seconds before the next SMS sending after an unsuccessful attempt
   - awsRegion - AWS Region. [AWS SNS Regions](https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html)
5. Enable the integration

To get SMS notifications select newly created Notification Service in "Notif Service" drop-down on Notification admin form. OneVizion URL is automatically added to the end of the message for clarity.

Please note that in order to send SMS, phone numbers must consist of a "+" character and no more than 15 digits (including the country code) or no more than 14 digits, then the country code equal to +1 will be added to the phone number. The phone number allows the use of characters "(", ")", "-".

Example of settings.json

```json
{
    "oneVizionUrl" : "test.onevizion.com",
    "oneVizionLogin" : "username",
    "oneVizionPwd" : "*****",
    "serviceId" : 1000043,
    "phoneNumberField" : "U_PHONE_NUMBER",
    "awsAccessKeyId" : "*****",
    "awsSecretAccessKey" : "*****",
    "maxAttempts" : 2,
    "nextAttemptDelay" : 30,
    "awsRegion": "eu-west-1"
}
```

