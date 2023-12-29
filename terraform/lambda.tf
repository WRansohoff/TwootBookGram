data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json

  inline_policy {
    name = "LLMLambdaRoleInlinePolicy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["ec2:CreateNetworkInterface",
                      "ec2:DeleteNetworkInterface",
                      "ec2:DescribeNetworkInterfaces",
                      "logs:CreateLogGroup",
                      "logs:CreateLogStream",
                      "logs:PutLogEvents"]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
}

resource "aws_cloudwatch_log_group" "llm_lambda_logs" {
  name              = "/aws/lambda/LLMAppLambda"
  retention_in_days = 7
}

resource "aws_lambda_function" "llm_app_function" {
  function_name = "LLMAppLambda"
  role          = aws_iam_role.iam_for_lambda.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.llm_app_image_repo.repository_url}:latest"
  memory_size   = 2048
  timeout       = 180
  publish       = true

  vpc_config {
    security_group_ids = ["${aws_security_group.llm_secgroup.id}"]
    subnet_ids = "${aws_subnet.llm_subnets[*].id}"
  }

  depends_on = [
    aws_iam_role.iam_for_lambda,
    aws_cloudwatch_log_group.llm_lambda_logs
  ]
}

resource "aws_lambda_function_url" "llm_app_function_url" {
  function_name      = "${aws_lambda_function.llm_app_function.function_name}"
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}
