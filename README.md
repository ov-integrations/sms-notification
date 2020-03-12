# sms-notification

SMS-Notification is an integration that works as an external Notification Serviece for sending SMS notifications. It uses 
Amazon Simple Notification Service (SNS) to send SMS.

## Requirements
- Python 3
- Requests - [library for python](http://docs.python-requests.org/en/master/)
- boto3 - [Boto is the Amazon Web Services (AWS) SDK for Python](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Usage
1. Install this integartion 
2. Create a new separate Notification Service
3. Craete separate Notifications with the new Notification Service
4. Fill the settings file of the integartion
   - oneVizionUrl - OneVizion URL
   - oneVizionLogin - OneVizion Login
   - oneVizionPwd - OneVizion Password
   - serviceId - Notification Service ID
   - phoneNumberField - The name of the field which contains the phone number of the recepient. Recepient is a user trackor related with User ID from the Notif Queue record.
   - awsAccessKeyId - AWS Access Key ID
   - awsSecretAccessKey - AWS Secret Access Key
   - maxAttempts - The number of attempts to send SMS
   - nextAttemptDelay - The delay in seconds before the next SMS sending after an unsuccessful attempt
   - awsRegion - AWS Region. [AWS SNS Regions](https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html)
5. Enable the integartion

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

