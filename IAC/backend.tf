terraform {
  backend "s3" {
    bucket  = "terraform-monitor-provide-states-files"
    key     = "objectDetection.tfstate"
    region  = "us-east-1"
  }
}