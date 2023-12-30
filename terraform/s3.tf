resource "aws_s3_bucket" "llm_site_bucket" {
  bucket = var.llm_bucket_name
}

resource "aws_s3_bucket_ownership_controls" "llmsb_ownership_ctl" {
  bucket = aws_s3_bucket.llm_site_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "llmsb_pub_access" {
  bucket = aws_s3_bucket.llm_site_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "llm_site_bucket_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.llmsb_ownership_ctl,
    aws_s3_bucket_public_access_block.llmsb_pub_access,
  ]

  bucket = aws_s3_bucket.llm_site_bucket.id
  acl    = "public-read"
}
