resource "aws_ecr_repository" "llm_app_image_repo" {
  name                 = "llm_app_image_repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "docker_image" "llm_app_image" {
  name = "${aws_ecr_repository.llm_app_image_repo.repository_url}:latest"
  depends_on = [aws_ecr_repository.llm_app_image_repo]
  build {
    context = "${path.cwd}/../runtime_container/."
    build_args = {
      REDIS_HOST: "${aws_elasticache_cluster.llm_cache.cache_nodes.0.address}"
      LLM_FORBIDDEN_WORDS: "${var.forbidden_words}"
    }
  }
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "${path.cwd}/runtime_container/[Dl]*") : filesha1(f)]))
  }
}

resource "docker_registry_image" "llm_app_image_ecr" {
  name = docker_image.llm_app_image.name
}
