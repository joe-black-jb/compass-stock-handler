provider "aws" {
  region     = "ap-northeast-1"
}

resource "aws_lambda_function" "compass_stock_handler" {
  function_name = "compass-stock-handler"
  package_type = "Image"
  image_uri = "${var.image_uri}"
  role     = aws_iam_role.compass_stock_handler_role.arn

  environment {
    variables = {}
  }
}

# Lambda の IAM ロール
resource "aws_iam_role" "compass_stock_handler_role" {
  name = "compass-stock-handler-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# AmazonS3FullAccess ポリシーのアタッチ
resource "aws_iam_role_policy_attachment" "s3_full_access" {
  role       = aws_iam_role.compass_stock_handler_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# AWSLambdaBasicExecutionRole ポリシーのアタッチ
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.compass_stock_handler_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
