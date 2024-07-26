sudo apt-get update
# socket
sudo apt-get install python3-pip
sudo pip3 install pycryptodome sockets

# generate client key and certificate
openssl genpkey -algorithm RSA -out client_key.pem
openssl req -new -x509 -key client_key.pem -out client_cert.pem -days 365 -subj "/C=VN/ST=./L=HCM/O=HCMUS/OU=./CN=VM1/emailAddress=virtualmachine1@gmail.com"