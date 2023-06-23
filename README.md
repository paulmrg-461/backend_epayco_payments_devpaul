# ePayco Payments

## _Python Flask - ePayco REST API_

This repository contains the code and configuration files to run the ePayco Payments Flask REST API using Docker.

## Prerequisites

Before getting started, make sure you have the following prerequisites:

- Docker installed on your operating system.
- Your ePayco API Key and Private Key. Make sure to have them handy.

## Setup Instructions

Follow these steps to set up and run the ePayco Payments REST API with Docker:

1. Open the `.env` file and add the following lines, replacing `YOUR_API_KEY` and `YOUR_PRIVATE_KEY` with your actual ePayco API Key and Private Key.

EPAYCO_API_KEY=YOUR_API_KEY

EPAYCO_PRIVATE_KEY=YOUR_PRIVATE_KEY

2. Save the `.env` file.

3. Open a terminal or command prompt and navigate to the root directory of your project.

4. Run the following command to start the Docker container:

```bash
$ docker-compose up --build -d
```

This command will build the Docker image and start the container in detached mode.

Wait for the container to start up. Once it's running, you can access the API.

Open your web browser and navigate to http://127.0.0.1:1616/ or the domain where it was deployed.

This will open the ePayco Payments REST API in your browser.

You can now use the API endpoints to create, retrieve, update, and delete payments using the provided documentation.

## Additional Notes

If you deployed the Docker container to a different domain, replace 127.0.0.1:1616 in step 7 with the appropriate URL.

Ensure that your API Key and Private Key in the .env file are correct and properly formatted.

Remember to keep your API Key and Private Key secure and avoid sharing them publicly.

## POSTMAN API Documentation

For detailed information on the available endpoints and how to use them, refer to the ePayco Payments REST API Documentation.

<a  href="https://documenter.getpostman.com/view/18896773/2s93shzpLb#intro">https://documenter.getpostman.com/view/18896773/2s93shzpLb#intro</a>

## _About_
<a  href="https://github.com/paulmrg-461/backend_epayco_payments_devpaul">Flask ePayco Github Repo</a>

Developed by:
Paul Realpe

Email: paulmrg461@gmail.com

Phone: 3148580454

<a  href="https://devpaul.co">https://devpaul.co/</a>
<a  href="https://github.com/paulmrg-461/flutter_epayco_payments">Flutter ePayco Github Repo</a>
