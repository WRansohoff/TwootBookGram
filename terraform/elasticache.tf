resource "aws_security_group" "llm_secgroup" {
  vpc_id      = "${aws_vpc.llm_vpc.id}"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_elasticache_subnet_group" "llm_subnet_group" {
  name       = "llm-cache-subnet"
  subnet_ids = "${aws_subnet.llm_subnets[*].id}"
}

resource "aws_elasticache_cluster" "llm_cache" {
  cluster_id                 = "llm-cache-cluster"
  engine                     = "redis"
  node_type                  = "cache.t4g.micro"
  num_cache_nodes            = 1
  port                       = 6379
  parameter_group_name       = "default.redis7"
  engine_version             = "7.1"
  subnet_group_name          = "${aws_elasticache_subnet_group.llm_subnet_group.name}"
  security_group_ids         = ["${aws_security_group.llm_secgroup.id}"]
}
