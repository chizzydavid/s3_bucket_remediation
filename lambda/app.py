import json
import boto3

s3_client = boto3.client("s3")
config_client = boto3.client("config")
sns_client = boto3.client("sns")

def lambda_handler(event, context):
    response = config_client.get_compliance_details_by_config_rule(
        ConfigRuleName='s3-bucket-level-public-access-prohibited',
        ComplianceTypes=['NON_COMPLIANT'],
    )
    
    response_payload = json.loads(json.dumps(response, default=str))
    non_compliant_items = list(map(get_resource_id, response_payload.get('EvaluationResults')))

    if len(non_compliant_items) > 0:
        for item in non_compliant_items:
            response = s3_client.put_public_access_block(
                Bucket = item,
                PublicAccessBlockConfiguration = {
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
        send_sns_notification(non_compliant_items)
        return {
            'statusCode': 200,
            'body': json.dumps('Non Compliant S3 buckets updated.')
        }
    
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('No non-compliant S3 buckets were found')
        }


def get_resource_id(item):
    return item.get('EvaluationResultIdentifier').get('EvaluationResultQualifier').get('ResourceId')

def send_sns_notification(items):
    items_to_str = "\n".join(items)
    sns_target_arn = ''
    sns_client.publish(
        TargetArn = sns_target_arn,
        Subject = 'Non Compliant S3 Buckets Remediated',        
        Message = 'The following S3 buckets were discovered to be public and have been updated to private. \n' + items_to_str
    )
    
    
    
