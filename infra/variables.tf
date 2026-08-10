variable "project_name" {
  description = "Name of the project."
  type        = string
  default     = "ai-interview-coach"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "production"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "aws_region" {
  description = "AWS region in which resources are deployed."
  type        = string
  default     = "eu-west-2"
}