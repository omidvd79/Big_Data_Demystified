echo creating private.pem **************************
openssl genrsa -out private.pem 2048
echo creating cacert.pem ***************************
openssl req -new -x509 -key private.pem -out cacert.pem -days 10950
