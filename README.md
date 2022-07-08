# s3_bucket_remediation



#### **Architecture Diagram**
![Architecture_diagram](diagrams/s3_remediation_architecture.png)


#### Config Rule

* Create an AWS Config Rule that checks all S3 buckets and returns those that are public(non-compliant)
* ![Screenshot_2021-11-14_at_18](diagrams/Screenshot_2021-11-14_at_18.25.46.png)

#### Lambda Function

* Create a Lambda Function that uses the Config rule above to get the public S3 buckets and update their status to private.

![Screenshot_2021-11-14_at_18](diagrams/Screenshot_2021-11-14_at_18.30.55.png)

#### SNS Notification

* The Lambda Function should also trigger an email notification using AWS Simple Notification Service(SNS) showing the non-compliant buckets and their updated status.

![Screenshot_2021-11-14_at_18](diagrams/Screenshot_2021-11-14_at_18.33.16.png)