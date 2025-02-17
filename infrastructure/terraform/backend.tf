terraform {
  backend "s3" {
    bucket  = BUCKET_NAME
    key     = "tf_backend/terraform.tfstate"
    region  = AWS_REGION
    encrypt = true
  }
}
