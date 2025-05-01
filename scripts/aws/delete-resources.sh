# aws cloudformation delete-stack --stack-name LanginfraAppStack
aws ecr delete-repository --repository-name langinfra-backend-repository --force
# aws ecr delete-repository --repository-name langinfra-frontend-repository --force
# aws ecr describe-repositories --output json | jq -re ".repositories[].repositoryName"