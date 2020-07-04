# tolack

## Description

Notify Slack via AWS Lambda of Toggl's current entry.

## Requirement

- [Toggl API Token](https://toggl.com/app/profile)
- Webhook URL for Slack Incoming WebHooks

## Usage

1. Creating a function in AWS Lambda
2. Set the Lambda environment variables
   - **slackChannel**: Slack channel name
   - **slackWebhookUrl**: Webhook URL(Requirement)
   - **togglApi**: https://www.toggl.com/api/v8
     - [toggl/toggl_api_docs](https://github.com/toggl/toggl_api_docs/blob/master/toggl_api.md)
   - **togglApiToken**: Toggl API Token(Requirement)
3. Set a rule to periodically execute a Lambda function in Amazon CloudWatch Events

## Licence

[MIT](https://github.com/bryutus/tolack/blob/master/LICENSE)
