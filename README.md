# enterlist
practice gspread sheets

# deploy 
1. First, create venv env
2. Download file for pip
3. Zip dir of library
4. Upload zip file to S3
5. Make function

  ```bash
  # cd enterlist
  # pip install -r requirements.txt --target .
  # zip -r ../enterlist.zip ./*
  # cd ..
  # aws s3 cp ./enterlist.zip s3://hogehoge/enterlist.zip
  # aws lambda create-function --cli-input-json file://aws.json
  
  ```
