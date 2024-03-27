variable "credentials" {
  description = "My Credentials"
  default     = "/home/iandemavivas/.google/credentials/flight_analytics.json"
}


variable "project" {
  description = "Project ID"
  default     = "flight-analytics-418504"
}


variable "region" {
  description = "Region"
  default     = "us-central1-c"
}


variable "location" {
  description = "Project Location"
  default     = "US"
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