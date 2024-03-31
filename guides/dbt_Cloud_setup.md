# Setting up dbt Cloud project

1. Create a [dbt account](https://www.getdbt.com/).
2. Once logged in, complete setup by creating a new project.
3. Connect your BigQuery data warehouse by uploading the service account json.
4. Set the development dataset name under the as the Development Credentials `flights_stg` as set up in terraform. Then, click Test Connection to ensure dbt cloud has access to the development dataset.
![](images/dbt_3.png)

Note: This step requires that you clone the project repository to your own repository.

5. Select git clone and paste the SSH key from your repository. Then take note of the deploy key provided.
6. Head to your GitHub repository and in the Settings tab, navigate to Security > Deploy keys. Select Add deploy key and paste the deploy key provided by dbt cloud. Make sure to select Allow write access.
![](images/dbt_5.png)
7. Then in Advanced Settings in dbt Cloud, make sure the project subdirectory is in `dbt`.
![](images/dbt_6.png)

## Setting up the production environment and the dbt Cloud job
8. Ensure that the `schema.yml` has the correct database (your GCP Project ID).
```YAML
sources:
  - name: staging
    database: <your-GCP-Project-ID>
    schema: flights_stg
```
9. Then in Deploy > Environments, select Create environment and name your production environment and Set deployment type as Production. In Deployment credentials > Dataset, enter the production dataset in BigQuery, flights_stg, as setup in terraform.
![](images/dbt_7.png)
10. Then in the Production environment you just created, navigate to Jobs > Create job > Deploy job. Name the deployment job and under Triggers > Schedule > Run on schedule, set Timing as Cron schedule and set the Custom cron schedule (UTC) to be `1 * * * *`.