# Setting up GCP GCS storage bucket and BigQuery datasets with Terraform

1. Navigate to the terraform directory
2. Set the correct values to variables according to your own credentials and GCP project ID in `variables.tf`
```tf
variable "credentials" {
  description = "My Credentials"
  default     = "/home/<username>/.google/credentials/<your-service-account-key-file>.json"
}


variable "project" {
  description = "Project ID"
  default     = "<your-gcp-project-id>"
}
```
3. Initiate terraform `terraform init`
4. View the terraform plan `terraform plan` and check the following services to be created
5. Apply the plan by running `terraform apply` . Enter ‘yes’.

Note: When you want to destroy the services run `terraform destroy`.