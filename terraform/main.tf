provider "aws" {
  region     = "ap-northeast-1"
}

resource "aws_lambda_function" "compass_stock_handler" {
  function_name = "compass-stock-handler"
  package_type = "Image"
  image_uri = "${var.image_uri}"
  role     = aws_iam_role.lambda_execution_role.arn

  environment {
    variables = {}
  }
}

# Lambda の IAM ロール
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
