output "redis_endpoint" {
  value = "${aws_elasticache_cluster.llm_cache.cache_nodes.0.address}"
}

output "lambda_endpoint" {
  value = "${aws_lambda_function_url.llm_app_function_url.function_url}"
}

output "lambda_name" {
  value = "${var.lambda_name}"
}

output "ecr_repository" {
  value = "${aws_ecr_repository.llm_app_image_repo.repository_url}"
}

output "s3_url" {
  value = "${aws_s3_bucket.llm_site_bucket.bucket_domain_name}"
}

output "s3_arn" {
  value = "${aws_s3_bucket.llm_site_bucket.arn}"
}

output "s3_static_page" {
  value = "${aws_s3_bucket.llm_site_bucket.bucket_regional_domain_name}/index.html"
}
