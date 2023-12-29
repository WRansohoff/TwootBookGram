# VPC for the app to use.
resource "aws_vpc" "llm_vpc" {
  cidr_block           = "${var.vpc_cidr_block}"
  enable_dns_hostnames = true
}

# Internet gateway for VPC subnets
resource "aws_internet_gateway" "llm_gateway" {
  vpc_id = "${aws_vpc.llm_vpc.id}"
}

# Allow internet access for the VPC.
data "aws_route_table" "selected" {
  vpc_id = "${aws_vpc.llm_vpc.id}"
  filter {
    name = "association.main"
    values = ["true"]
  }
}
resource "aws_route" "llm_internet_access" {
  route_table_id         = "${data.aws_route_table.selected.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.llm_gateway.id}"
}

# Subnets for the app's VPC.
data "aws_availability_zones" "available" {}
resource "aws_subnet" "llm_subnets" {
  count                   = "${length(var.cidr_blocks)}"
  vpc_id                  = "${aws_vpc.llm_vpc.id}"
  availability_zone       = "${data.aws_availability_zones.available.names[count.index]}"
  cidr_block              = "${var.cidr_blocks[count.index]}"
  map_public_ip_on_launch = true
}
