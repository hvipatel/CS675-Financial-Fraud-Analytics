# AWS setup from scratch

For someone new to AWS and the command line, including a student setting up their own AWS
account (with their own credit card) for the project. It takes you from no account to working
credentials on your machine. If you already have an AWS account and the AWS CLI configured,
skip to the main `README.md`.

You do this once. It covers: create an account, make an access key, install the command-line
tools (AWS CLI and Terraform), configure your credentials, and run Terraform.

> Cost note: an AWS account is free to open, but running queries and clusters costs money.
> Set a budget alert (last section) and tear resources down when done.

## 1. Create an AWS account

1. Go to https://aws.amazon.com and choose **Create an AWS Account**.
2. Enter an email, a password, and an account name.
3. Provide contact details and a credit or debit card (AWS verifies it with a small charge).
4. Verify your phone number and pick the **Basic (free)** support plan.
5. Sign in to the **AWS Management Console** with the email and password you just set. This
   login is the **root user** - the account owner.

Use the root user only for account setup and billing. For everyday work you create a
separate **IAM user**, which is safer.

## 2. Create an access key (IAM user)

An **access key** is the id and secret the command line uses to act on your account.

1. In the console search bar, type **IAM** and open it.
2. In the left menu choose **Users**, then **Create user**.
3. Name the user (for example `admin-cli`). Leave console access off - this user is for the
   command line. Choose **Next**.
4. Choose **Attach policies directly**, tick **AdministratorAccess**, then **Next** and
   **Create user**.
5. Open the new user, go to the **Security credentials** tab, and choose **Create access key**.
6. Pick the **Command Line Interface (CLI)** use case, acknowledge the note, and **Create**.
7. You now see an **Access key ID** and a **Secret access key**. Copy both, or **Download
   .csv file**. The secret is shown only once.

> Keep the secret private. Never commit it to Git, paste it into chat, or email it. You can
> delete or rotate the key anytime from this same screen.

## 3. Open a terminal

- **macOS:** open **Terminal** (Applications > Utilities, or search with Spotlight).
- **Windows:** open **Windows Terminal** or **PowerShell** (search from the Start menu).
- **Linux:** open your **Terminal** application.

A terminal is a window where you type commands and press Enter. The steps below are typed
there.

## 4. Install the AWS CLI and Terraform

Install the tool, then confirm it works.

- **macOS:**
  ```bash
  curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
  sudo installer -pkg AWSCLIV2.pkg -target /
  ```
- **Windows:** download and run the installer from
  https://awscli.amazonaws.com/AWSCLIV2.msi (double-click, click through), then reopen the
  terminal.
- **Linux:**
  ```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip && sudo ./aws/install
  ```

Confirm the install:
```bash
aws --version        # prints something like: aws-cli/2.x.x ...
```
If `aws` is "not found", close and reopen the terminal, or follow the official guide at
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html.

Now install **Terraform 1.5+** (it turns this starter's code into real AWS resources):

- **macOS:** `brew install hashicorp/tap/terraform` (or download from the install page below).
- **Windows:** `choco install terraform`, or download the zip from the install page, unzip it,
  and add the folder to your PATH.
- **Linux:** download the zip from https://developer.hashicorp.com/terraform/install, unzip it,
  and `sudo mv terraform /usr/local/bin/`.

Confirm the install:
```bash
terraform -version        # prints something like: Terraform v1.x.x
```

## 5. Configure your credentials

Run:
```bash
aws configure
```
It asks four things - answer each and press Enter:
- **AWS Access Key ID:** paste the key id from step 2.
- **AWS Secret Access Key:** paste the secret from step 2.
- **Default region name:** `us-east-2`.
- **Default output format:** `json`.

This saves your settings to a hidden folder in your home directory (`~/.aws/`). You will not
need to paste the keys again on this machine.

## 6. Verify it works

```bash
aws sts get-caller-identity
```
You should see JSON with your account number and a `user/admin-cli` ARN. That means your
credentials are set. Common errors:

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: aws` | CLI not installed or terminal not reopened | Redo step 4, reopen terminal |
| `Unable to locate credentials` | `aws configure` not completed | Rerun step 5 |
| `InvalidClientTokenId` / `SignatureDoesNotMatch` | Key or secret mistyped | Rerun step 5 and paste carefully |

## 7. Set a budget alert (recommended)

1. In the console search bar, type **Billing** and open it, then choose **Budgets**.
2. **Create budget** > **Zero spend** or a small **monthly cost** budget (for example $10).
3. Add your email so AWS warns you before charges grow.

Also turn on **MFA** for the root user (IAM > add MFA) for account safety.

## Configure and run Terraform

Terraform reads the `.tf` files in this starter and creates the matching AWS resources. There
is no separate Terraform login: it uses the AWS credentials you configured above, plus the
region and inputs set in the code and your `terraform.tfvars`.

You run four commands inside a starter directory (`instructor-roles/` or `student-workspace/`):

- `terraform init` - run once per directory; downloads the AWS provider.
- `terraform plan` - preview what will be created or changed (changes nothing).
- `terraform apply` - create or update the resources.
- `terraform destroy` - remove everything it created (run this to stop costs).

What you configure:

- Copy the provided `*.tfvars.example` to `terraform.tfvars` and edit your inputs (the roster,
  your `student_id`, and so on). The exact variables are described in each directory's `Readme.md`.

Keep these out of Git:

- Terraform writes `terraform.tfstate` and caches the provider under `.terraform/`. These, and
  `terraform.tfvars`, are gitignored already - never commit them, since state can hold sensitive
  values.

The exact commands for each directory are in `instructor-roles/Readme.md` and
`student-workspace/Readme.md`.

## Next

You now have working AWS credentials. Continue in `README.md`:
- **Student using your own account:** you are the owner, so your access key works directly.
  Go straight to `student-workspace/Readme.md`, set your own `student_id`, and `make apply`.
  You do not need `instructor-roles/` (that is only for an instructor issuing scoped creds to
  a shared account).
- **Instructor owning a shared account:** run `instructor-roles/` to create per-student roles
  and hand out credentials.
- **Student given credentials by an instructor:** see the student steps in
  `student-workspace/Readme.md`.
