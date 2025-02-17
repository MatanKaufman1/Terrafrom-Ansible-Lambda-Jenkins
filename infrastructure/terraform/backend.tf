terraform {
  backend "s3" {
    bucket  = "bucket-matan"
    key     = "tf_backend/terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
}
