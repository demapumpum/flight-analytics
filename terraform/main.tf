terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "flights-analytics-data-lake-bucket" {
  name          = "${var.project}-bucket"
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 3 # days
    }
    action {
      type = "Delete"
    }
  }
}


resource "google_bigquery_dataset" "flights_stg_dataset" {
  dataset_id                 = var.stg_bq_dataset_name
  project                    = var.project
  location                   = var.location
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "flights_prod_dataset" {
  dataset_id                 = var.prod_bq_dataset_name
  project                    = var.project
  location                   = var.location
  delete_contents_on_destroy = true
}
