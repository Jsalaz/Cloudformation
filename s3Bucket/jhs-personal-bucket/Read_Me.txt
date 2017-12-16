Regular deploy default params
aws cloudformation create-stack --stack-name personal-s3bucket --template-body "file://jhs_S3bucket.json" 

Deploy with params key:value as string
aws cloudformation create-stack --stack-name personal-s3bucket-String --template-body "file://jhs_S3bucket.json" --parameters ParameterKey=BucketName,ParameterValue=jhs-from-string-bucket-s3

Deploy with params key:value from json file
aws cloudformation create-stack --stack-name personal-s3bucket-JSON --template-body "file://jhs_S3bucket.json" --parameters "file://../params/jhs_S3bucket_params.json"

Update Stack (removing lifeCycle policies)
aws cloudformation update-stack --stack-name personal-s3bucket --template-body "file://jhs_S3bucket.json" --parameters "file://../params/jhs_S3bucket_params.json"

Validate template
aws cloudformation validate-template --template-body file://jhs_S3bucket.json