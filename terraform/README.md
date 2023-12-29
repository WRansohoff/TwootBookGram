# Terraform Deployments

These Terraform scripts deploy AWS infrastructure to run the language model as a web app. They are used as part of the wider CI/CD pipeline in GitHub Actions to keep the web app up to date.

It manages the following pieces of AWS infrastructure:

* S3 bucket containing static React site
* Lambda function which runs the LLM inference
* ECR container (Lambda runtime environment)
* ElastiCache Redis instance for rate limiting API requests

If you want to use a custom domain name, you'll need to set that up manually. [AWS' Route53 registrar is pretty easy to use](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html), but you still need to go through some manual steps like entering contact information for the domain. These scripts also do not manage a CloudFront distribution, because I don't think CloudFront can be used without a valid domain registration for DNS queries to target.

The role that you create for running the Terraform commands will need the following permissions:

(TODO)

Once the process completes, you'll get a link to the S3 bucket's static site URL. You'll also need to upload the static site files to the S3 bucket, and generate a new container image which references the new cache URL. These steps are handled by the GitHub Action which builds and deploys the app (minus DNS/CloudFront).

Note that you will incur some charges for this infrastructure. I estimate the major charges at about $0.0003 - $0.0005 per query, plus about $11-15 per month for the small ElastiCache node, S3 bucket, and ECR image. Unfortunately, AWS' serverless ElastiCache offering seems to have a minimum charge of 1GB storage, which comes out to about $90/month - too much for a small demonstration like this.

