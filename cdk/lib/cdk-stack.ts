import * as cdk from 'aws-cdk-lib';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export interface CustomizedProps extends cdk.StackProps {
  projectName: string;
}

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: CustomizedProps) {
    super(scope, id, props);

    // IAM
    const iamRoleForLambda = new iam.Role(this, "iamRoleForLambda", {
      roleName: `${props.projectName}-lambda-role`,
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
      managedPolicies: [
        {
          "managedPolicyArn": "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        }
      ]
    })

    // Lambda
    const pythonPackagePath = "../src/" + props.projectName.replace(/-/g, "_");
    const lambdaFunctions = new lambda.Function(this, "lambdaFunction", {
      functionName: `${props.projectName}-lambda`,
      runtime: lambda.Runtime.PYTHON_3_12,
      timeout: cdk.Duration.seconds(900),
      code: lambda.Code.fromAsset(pythonPackagePath),
      handler: "lambda_handler.lambda_function",
      role: iamRoleForLambda,
      environment: {
        "LOGLEVEL": "INFO",
        "SECRET_KEY": "secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      }
    })

    // EventBridge
    new events.Rule(this, "eventBridge", {
      schedule: events.Schedule.cron({minute: "0"}),
      targets: [new targets.LambdaFunction(lambdaFunctions, {
        event: events.RuleTargetInput.fromObject({
          DATABASE_ID: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          PROPERTY_NAME_STATUS: "Status",
          PROPERTY_VALUE_STATUS_DONE: "Done",
          PROPERTY_NAME_PUBLISH: "Publish",
          PROPERTY_NAME_PUBLISH_DATE: "PublishDate"
        })
      })]
    })
  }
}
