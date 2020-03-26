# sms-notification

SMS-Notification is an integration that works as an external Notification Serviece for sending SMS notifications. It uses 
Amazon Simple Notification Service (SNS) to send SMS.

## Requirements
- Python 3
- Requests - [library for python](https://requests.readthedocs.io/en/master/)
- boto3 - [Boto is the Amazon Web Services (AWS) SDK for Python](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Usage
1. Create a new Notification Service in OneVizion. All settings of this service are ignored by Integration, use random values for required fields
2. Install this integration
3. Create dedicated account for integration with following privs:
   * WEB_SERVICES R
   * ADMIN_NOTIF_QUEUE RE
   * ADMIN_USERS R
   *  ADMIN_INTEGRATION_LOG RA
   * \<User Trackor Type\> R
   * \<User Trackor Type Tab containing phoneNumberField\> R
4. Fill the integartion settings file:
   - oneVizionUrl - OneVizion URL
   - oneVizionLogin - OneVizion Login
   - oneVizionPwd - OneVizion Password
   - serviceId - ID of the Notification Service createf at step 2
   - phoneNumberField - The name of the field which contains the phone number of the recepient. Recepient is a user trackor related with User ID from the Notif Queue record.
   - awsAccessKeyId - AWS Access Key ID
   - awsSecretAccessKey - AWS Secret Access Key
   - maxAttempts - The number of attempts to send SMS
   - nextAttemptDelay - The delay in seconds before the next SMS sending after an unsuccessful attempt
   - awsRegion - AWS Region. [AWS SNS Regions](https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html)
5. Enable the integartion

To get SMS notifications select newly created Notification Service in "Notif Service" drop-down on Notification admin form. OneVizion URL is automatically added to the end of the message for clarity.

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

