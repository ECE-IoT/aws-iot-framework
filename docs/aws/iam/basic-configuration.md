# Identity and Access Management

IAM is a web service that helps to securely control access to AWS resources. In order to operate securely when handling with multiple developers, projects a good access hierarchy is compulsory.

*Link* to the [docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)


## Users
### Root
When creating a AWS account the first user is the **root** user, which owns the account, has all access rights. This account provides the billing information, has the ability to change the password of all other **sub-users**. This level of access can be dangerous when handling with lower-level tasks, so it's recommended to not use the root user credentials for *everyday* development/access.

### Administrator
The Administrator user has almost the same access rights as the root. The biggest exception is that the Administrator is **not** the owner of the account. An Administrator can be used for managing the rest of the Accounts with a extra level of security.

### Developer
Multiple developer accounts can be created. They do have access to the certain resource in which they are building the desired Application.

## Groups and Policies
Summed up, those two sections are used to an easier management of different resource distribution.

---

!!! warning
    This summary is only a rough overview of the complex functionality of AWS IAM. In order to get a deeper understanding reading the docs is mandatory!
