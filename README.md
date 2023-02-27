# Building serverless applications in Python with AWS Chalice

Check that you AWS credentials were already configured locally:
```bash
aws configure list --profile jdac
```

You need to create a Table in DynamoDB for this exercise. Let's call it `images`. To check if the table exists, execute:

```bash
aws dynamodb list-tables --profile jdac
```

You also need to have a bucket on S3 in order to store the images. Let's call it `images-jdac-mtt`. To check if the bucket already exists, execute:

```bash
aws s3 ls --profile jdac
```

Make sure the Python version is supported by AWS Lambda:

```bash
python3 --version
```

Install Chalice:

``bash
pip install chalice
``

Check the Chalice version:

```bash
chalice --version
```

Create a new project with Chalice:

```bash
chalice new-project images-descriptor
```

Install dependencies:

```bash
pip install -r requirements.txt
```
