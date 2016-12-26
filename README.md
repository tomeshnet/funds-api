# funds-api

Server APIs to interact with Toronto Mesh accounts on [Stripe](https://stripe.com).

This is a light-weight HTTP request handler to interact with the [Stripe Python Library](https://stripe.com/docs/libraries#python-library) using the account's [secret key](https://dashboard.stripe.com/account/apikeys), and should only be deployed on a secured server. The API server retrieves account information (e.g. transactions and balances) to render JSON responses containing information for public display. The `checkout` API is used to fulfill the server-side of a [Stripe checkout process](https://stripe.com/docs/checkout/tutorial).

## Running the API server

1. Make sure you have an updated version of Python

1. Install the **Stripe Python Library**:

    ```
    $ sudo easy_install pip
    $ sudo pip install --upgrade stripe
    ```

1. Set the environment variable `STRIPE_SECRET`:

    ```
    $ STRIPE_SECRET=YOUR_STRIPE_SECRET_KEY
    ```

1. Clone this repository and run the API server in background:

    ```
    $ nohup python funds_api.py &
    ```

## Communicating to the running API server

Assuming the website is served by an Apache HTTP server on the same host...

1. Login as root and enable the necessary Apache modules:

    ```
    # a2enmod proxy
    # a2enmod proxy_http
    ```

1. Add the following lines to **/etc/apache2/sites-available/YOUR.DOMAIN.conf**:

    ```
    <VirtualHost *:80>
            ProxyPreserveHost On
            ProxyRequests Off
            ProxyPassMatch ^/funds-api http://127.0.0.1:8000
            ProxyPassReverse ^/funds-api http://127.0.0.1:8000
            ...
    </VirtualHost>
    ```

1. Restart Apache:

    ```
    service apache2 restart
    ```

1. Try listing the account balance:

    ```
    $ curl https://YOUR.DOMAIN/funds-api/balance
    ```
