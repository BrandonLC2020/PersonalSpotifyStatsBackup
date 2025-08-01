# Personal Spotify Stats Backup

This project, "Personal Spotify Stats Backup," is designed to automatically fetch your top Spotify tracks, artists, and albums on a monthly basis and store this data in a **MySQL** database. It runs as an **AWS Lambda function**, automating the entire backup process.

-----

## Features

  * **Fetches Top Data:** Retrieves your top 50 tracks and artists from the last month using the Spotify Web API.
  * **Calculates Top Albums:** Determines your top albums based on the frequency of tracks from those albums in your top tracks list.
  * **Monthly Snapshots:** Organizes the fetched data into monthly snapshots before database insertion.
  * **Automated and Serverless:** Designed to run as an AWS Lambda function, providing an automated, serverless solution for backing up your stats.
  * **Secure Credential Management:** Uses **AWS Secrets Manager** to securely store and retrieve your Spotify refresh token.
  * **Database Storage:** Stores the retrieved Spotify statistics in a **MySQL** database for historical tracking and analysis.

-----

## Setup and Installation

To set up and run this project, you'll need an AWS account and a MySQL database.

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd personalspotifystatsbackup
    ```

2.  **Install Dependencies:**
    The required Python packages are listed in the `requirements.txt` file. You will need to create a deployment package for your Lambda function that includes these libraries.

      * `python-dotenv==1.0.1`
      * `Requests==2.32.3`
      * `boto3==1.28.66`
      * `mysql-connector-python==8.0.33`

3.  **Spotify API Application Setup:**

      * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
      * Log in and create a new application.
      * Note down your `Client ID` and `Client Secret`.
      * In the application settings, add a Redirect URI. For local development and generating your initial token, `http://localhost:8888/callback` is a good choice.

4.  **Generate a Spotify Refresh Token:**

      * The project includes a `SpotifyRefreshTokenGenerator.py` script to get your initial refresh token.
      * Add your `CLIENT_ID` and `CLIENT_SECRET` to a `.env` file.
      * Run the script: `python SpotifyRefreshTokenGenerator.py`.
      * Follow the prompts to authorize your account. The script will print a refresh token to the console.

5.  **AWS and Environment Configuration:**

      * **AWS Secrets Manager:**

          * Navigate to AWS Secrets Manager in your AWS console.
          * Create a new secret to store your Spotify refresh token. Your `SpotifyAPIManager.py` expects the secret to be a key-value pair, for example: `{'spotify_refresh_token': 'YOUR_REFRESH_TOKEN'}`.

      * **Environment Variables for Lambda:**

          * When you create your Lambda function, you will need to set the following environment variables. You can use the `sample.env` file as a template.
              * `CLIENT_ID`: Your Spotify application Client ID.
              * `CLIENT_SECRET`: Your Spotify application Client Secret.
              * `REDIRECT_URI`: The redirect URI you set in the Spotify Developer Dashboard.
              * `SECRET_NAME`: The name of the secret you created in AWS Secrets Manager.
              * `DB_HOST`: The endpoint for your MySQL database.
              * `DB_USERNAME`: Your database username.
              * `DB_PASSWORD`: Your database password.
              * `DB_NAME`: The name of your database.
              * `DB_PORT`: The port for your database (usually 3306 for MySQL).

6.  **Deploy to AWS Lambda:**

      * Package your Python code (`lambda_function.py`, the `Managers` and `Types` directories) and the installed dependencies from `requirements.txt` into a .zip file.
      * Create a new Python Lambda function in your AWS account.
      * Upload the .zip file as your deployment package.
      * Set the handler to `lambda_function.lambda_handler`.
      * Configure the environment variables as described above.
      * You can set up a trigger, such as an Amazon EventBridge (CloudWatch Events) rule, to run the function on a schedule (e.g., once a month).

    ### Deployment Script (`deploy.sh`)

    To simplify the packaging process, you can use the following bash script. Save it as `deploy.sh` in the root of your project directory and make it executable with `chmod +x deploy.sh`.

    ```bash
    #!/bin/bash

    # Exit immediately if a command exits with a non-zero status.
    set -e

    # Define variables
    PACKAGE_DIR="package"
    ZIP_FILE="deployment_package.zip"

    echo "--- Starting deployment packaging ---"

    # Create a clean directory for the package
    echo "Creating a clean package directory..."
    rm -rf $PACKAGE_DIR $ZIP_FILE
    mkdir $PACKAGE_DIR

    # Install dependencies into the package directory
    echo "Installing dependencies from requirements.txt..."
    pip install --target $PACKAGE_DIR -r requirements.txt

    # Copy the Lambda function and other necessary Python files
    echo "Copying source files..."
    cp lambda_function.py $PACKAGE_DIR/
    cp -r Managers $PACKAGE_DIR/
    cp -r Types $PACKAGE_DIR/

    # Create the deployment zip file
    echo "Creating deployment package: $ZIP_FILE..."
    cd $PACKAGE_DIR
    zip -r ../$ZIP_FILE .
    cd ..

    # Clean up the package directory
    echo "Cleaning up..."
    rm -rf $PACKAGE_DIR

    echo "--- Deployment package created successfully: $ZIP_FILE ---"
    ```

    ### AWS CLI Commands

    Once you have created your `deployment_package.zip` and have the AWS CLI configured, you can use the following commands to manage your Lambda function.

    **To create the Lambda function (run this once):**
    *(Replace the placeholder values with your own information)*

    ```bash
    aws lambda create-function \
      --function-name PersonalSpotifyStatsBackup \
      --runtime python3.9 \
      --role arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/YOUR_LAMBDA_EXECUTION_ROLE \
      --handler lambda_function.lambda_handler \
      --zip-file fileb://deployment_package.zip \
      --environment "Variables={CLIENT_ID=your_client_id,CLIENT_SECRET=your_client_secret,REDIRECT_URI=your_redirect_uri,SECRET_NAME=your_secret_name,DB_HOST=your_db_host,DB_USERNAME=your_db_username,DB_PASSWORD=your_db_password,DB_NAME=your_db_name,DB_PORT=3306}" \
      --timeout 60 \
      --memory-size 256
    ```

    **To update the function's code:**
    *(This is the command you will use most often to deploy new versions of your code)*

    ```bash
    aws lambda update-function-code \
      --function-name PersonalSpotifyStatsBackup \
      --zip-file fileb://deployment_package.zip
    ```