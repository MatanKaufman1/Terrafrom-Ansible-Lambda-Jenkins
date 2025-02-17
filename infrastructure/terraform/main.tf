terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "gitlab_sg" {
  name        = "gitlab-sg"
  description = "Allow traffic for GitLab"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = var.protocol_sg
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = var.protocol_sg
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "jenkins_sg" {
  name        = "jenkins-sg"
  description = "Allow traffic for Jenkins"

  dynamic "ingress" {
    for_each = var.jenkins_gitlab_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = var.protocol_sg
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "gitlab" {
  ami             = var.ami_id
  instance_type   = var.gitlab_instance_type
  key_name        = var.ssh_key_name
  security_groups = [aws_security_group.gitlab_sg.name]
  root_block_device {
    volume_size = 15
    volume_type = "gp3"
  }
  tags = {
    Name = "gitlab-server",
  }
}

resource "aws_instance" "jenkins" {
  ami             = var.ami_id
  instance_type   = var.jenkins_instance_type
  key_name        = var.ssh_key_name
  security_groups = [aws_security_group.jenkins_sg.name]
  tags = {
    Name = "jenkins-server"
  }
}
