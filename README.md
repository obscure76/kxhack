# Install virtual env

pip install virtualenv

python3 -m venv env

source ./env/bin/activate 



# install dependencies

pip install -r requirements.txt


# create zip 
cd env/lib/python3.7/site-packages/
zip -r ../lambda.zip ./*

# upload the zip to S3 bucket and update the lambda



