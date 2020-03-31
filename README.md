# S3 File Processor

## Problem

Candidate Exercise for the Engineer Role

Exercise – Going Serverless

* Build a serverless framework (serverless.com) deployment that:
  * creates a Lambda
  * an S3 bucket
  * a Dynamo DB table
  * uploads a file to your bucket.
* Then, write a plugin that:
  * invokes the Lambda after the deployment
  * extracts data from the file in S3 and inserts that data into DynamoDB.
* Be creative.
* Show off.
* Make it interesting.

 Feel free to implement in Node or Python. Please deliver all source code in the form of a git repo.

### Assumptions/Considerations

* Due to time constraints I didn't implement a plugin but rather used a hook in S3 to activate the lambda function directly instead.
  * It doesn't solve the requirements directly as it will trigger when any file is input but to s3, rather than just post-deploy.
* As the input file type was not specified, I used an adaptor pattern coupled with a factory to encapsulate how I'd handle varied file handling.
  * Where a file-type is unsupported, it simply defaults to storing the url, I'm not entirely happy with this solution as it means the content field has mixed types.
* Basically unforgivable, but I haven't written tests, most of my code interacts directly with some AWS resource and again mocking that would take time. 
  * I wrote an article on a potential approach I worked on in Javascript for HackerNoon [here](https://medium.com/hackernoon/better-local-development-for-serverless-functions-b96b5a4cfa8f), I'd probably implement something similar.

## What it actually does

On running `sls deploy` this will:

* Create a Lambda
* Create an S3 bucket
* Create a Dynamo DB table
* It will upload any files in `files/`
  * The subfolders in `files/` are scoped to the environment, so `files/test` will get picked up on the test environment `files/prod` on prod etc.
* Once the files are uploaded, the lambda function will trigger and depending on the file-type insert the contents into the dynamo db.


## Installation

### Prepare Python Dependencies

```
git clone git@github.com:shano/serverless-file-storage.git
cd serverless-file-storage/
virtualenv venv/
source venv/bin/activate
pip install -r requirements.txt
```

### Prepare Node Dependencies

```
npm install
```

### To run

```
sls deploy
```