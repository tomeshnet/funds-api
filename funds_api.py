import BaseHTTPServer
import cgi
import os
import stripe
import sys

class stripeHandler(BaseHTTPServer.BaseHTTPRequestHandler):

  def do_GET(self):
    if self.path == '/funds-api/balance':
      stripe.api_key = secret_key
      resp = stripe.Balance.retrieve()
      self.send_response(200)
      self.send_header('content-type','application/json')
      self.end_headers()
      self.wfile.write(str(resp))
    else:
      self.send_response(200)
      self.send_header('content-type','application/json')
      self.end_headers()
      self.wfile.write('{}')

  def do_POST(self):
    if self.path == '/funds-api/checkout':
      stripe.api_key = secret_key
      length = int(self.headers.getheader('content-length'))
      form = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
      token = form['stripeToken'][0]

      # Process the tokenized transaction
      try:
        charge = stripe.Charge.create(
          amount=999, # Amount in cents
          currency="cad",
          source=token,
          description="Example charge"
        )

        # Send success response
        self.send_response(200)
        self.send_header('content-type','application/json')
        self.end_headers()
        self.wfile.write('{"success":true}')
      except stripe.error.CardError as e:
        # The card has been declined
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write('{"success":false}')
    else:
      self.send_response(200)
      self.send_header('content-type','application/json')
      self.end_headers()
      self.wfile.write('{}')

#######
# Main
#######
try:
  # Get Stripe secret key from environment variables
  secret_key = os.environ['STRIPE_SECRET']
  if secret_key:
    # Start API server
    servAddr = ('', 8000)
    serv = BaseHTTPServer.HTTPServer(servAddr, stripeHandler)
    serv.serve_forever()
  else:
    sys.exit('Please set the environment variable STRIPE_SECRET to your Stripe secret key')
except KeyError as e:
  sys.exit('Please set the environment variable STRIPE_SECRET to your Stripe secret key')

