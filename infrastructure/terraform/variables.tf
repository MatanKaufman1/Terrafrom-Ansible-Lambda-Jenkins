variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "ami_id" {
  description = "AMI ID to use for instances"
  type        = string
  default     = "ami-0084a47cc718c111a"
}

variable "ssh_key_name" {
  description = "Key name to connect to instance"
  type        = string
  default     = "k8s"
}

variable "gitlab_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.large"
}

variable "jenkins_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.medium"
}

variable "protocol_sg" {
  description = "The protocol used for Kubernetes security group ingress rules"
  type        = string
  default     = "tcp"
}

variable "jenkins_gitlab_ports" {
  description = "List of ports for Jenkins and GitLab instances ingress rules"
  type        = list(any)
  default     = [22, 80, 443, 2424, 8080]
}

