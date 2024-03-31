variable "credentials" {
  description = "My Credentials"
  default     = "/home/<username>/.google/credentials/<your-service-account-key-file>.json"
}


variable "project" {
  description = "Project ID"
  default     = "<your-gcp-project-id>"
}


variable "region" {
  description = "Region"
  default     = "<your-project-region>" # e.g. us-central1-c
}


variable "location" {
  description = "Project Location"
  default     = "<your-project-location>" # e.g. US
}


variable "stg_bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "flights_stg"
}

variable "prod_bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "flights_prod"
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}