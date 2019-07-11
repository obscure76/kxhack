# Install virtual env

pip install virtualenv

python3 -m venv env

source ./env/bin/activate 



# install dependencies

pip install -r requirements.txt


# create zip 
cp *.py env/lib/python3.7/site-packages/

cd env/lib/python3.7/site-packages/

zip -r ../lambda.zip ./*


# upload the zip to S3 bucket and update the lambda
S3 bucket: https://console.aws.amazon.com/s3/buckets/alexakxhackathon/?region=us-east-1&tab=overview
Lambda: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/hello-world-python?tab=graph

