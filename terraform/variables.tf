variable "vpc_cidr_block" {
  description = "The top-level CIDR block for the VPC."
  default     = "10.8.0.0/16"
}

variable "cidr_blocks" {
  description = "The CIDR blocks to create subnets for."
  default     = ["10.8.1.0/24", "10.8.2.0/24"]
}

variable "forbidden_words" {
  description = "List of words that the LLM is not allowed to print."
  default = ""
}

variable "ecr_pw" {
  description = "Password for private container registry login"
  default = ""
}

variable "ecr_address" {
  description = "Address for private container registry login"
  default = ""
}

variable "lambda_name" {
  description = "Function name for the Lambda function which runs the LLM inference."
  default = "LLMAppLambda"
}

variable "llm_bucket_name" {
  description = "S3 bucket to store the static React site in."
  default = "llm-app-staticsite-bucket"
}
