# Setting up a GCP project

1. Setup your [GCP account](https://cloud.google.com/free).
2. Then, setup your [GCP project](https://console.cloud.google.com/) by creating a new project and taking note of the project name.
3. Navigate to [Compute Engine](https://console.cloud.google.com/compute) and enable the API.

## Creating a Service Account
4. In the GCP Navigation Menu, navigate to IAM & Admin > Service Accounts then select CREATE SERVICE ACCOUNT.
5. Name your service account and give it the following roles:
   * Cloud Storage > `Storage Admin`, BigQuery > `BigQuery Admin`, and Compute Engine > `Compute Admin`
6. In the Service Accounts page, navigate to the service account you just created and under Actions, click the ellipsis button > Manage Keys. Add a new key in the ADD KEY > Create new key button. 
7. Create a JSON service account key file and store it in a separate directory like `home/<user>/.google/credentials/` for easy access.