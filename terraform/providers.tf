terraform {
  backend "s3" {
    bucket = "%%TF_STATE_BUCKET_NAME%%"
    key    = "terraform.tfstate"
    region = "us-east-2"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

provider "docker" {
  registry_auth {
    address = "${var.ecr_address}"
    username = "AWS"
    password = "${var.ecr_pw}"
  }
}
