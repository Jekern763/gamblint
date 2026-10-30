# Welcome to your CDK TypeScript project

This is a blank project for CDK development with TypeScript.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

(Make sure Docker Desktop is running)

- `pnpm test` perform the jest unit tests
- `pnpm synth` deploy this stack to your default AWS account/region

## Infrastructure Graph

```mermaid
graph TB

subgraph Internet
    User([User])
    DNS["Route 53<br/>gamblint.jamesekern.com"]
end

subgraph AWS["AWS Infrastructure"]

    CF["CloudFront Distribution"]

    S3[(S3 Frontend File Storage)]

    API["API Gateway"]

    Lambda["Backend Lambda Function"]

    DB[(DynamoDB)]

    Logs[(CloudWatch Logs)]

    DNS --> CF

    CF -->|Frontend Files| S3
    CF -->|/api/*| API
    API --> Lambda
    Lambda <--> DB
    Lambda --> Logs

end

subgraph CICD["CI / CD"]

    GitHub["GitHub Actions"]

    CDK["AWS CDK"]

    Infra["Infrastructure Stack"]

    Frontend["Frontend Build"]

    GitHub --> CDK
    CDK --> Infra

    Infra --> CF
    Infra --> API
    Infra --> Lambda
    Infra --> DB
    Infra --> S3

    CDK --> Frontend
    Frontend --> S3

end

User --> DNS
```
