# Configuration basics
This repository initilitzes and configures a docker container which already installs the **AWS CLI** inside. In order to maintain a good security policy, the configuration of the **AWS CLI** can't be done in advance. To use all features this repository provides, the **AWS CLI** needs to be configures right after cloning and initalizing the docker container

## Setup
### IAM and AWS Security

The setup is rather easy. First make sure that your **AWS account** has a *key pair* for authentication in the terminal. This part part is often done by an AWS administrator account, who can manage all users.

1. Open the `IAM Console`
2. Click on `users` and select the desired user
3. Head over to `Security credentials / Access key`
4. Click on `Create Access key`
5. Next an overlay will pop up and provide you with a downloadable `.csv` file which stores your:
    1. `AWS Acess Key ID`
    2. `AWS Secret Access Key`
6. Keep in mind: the `.csv` is just downloadable once!

### Configure the terminal
With your *key pair* ready to go, the next step is the configuration of your **AWS CLI** instance

Therfore type:

```shell
$ aws configure
```

Next there should be guided interface which lets you fill in your credentials

```shell
AWS Access Key ID [None]: your ID
AWS Secret Access Key [None]: your Secret
Default region name [None]: your default region
Default output format [None]: json
```

## Additional information
A detailed configuration documentation can be found at:

> [https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
