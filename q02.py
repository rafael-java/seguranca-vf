import ssl
import http.server

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


handler = MyRequestHandler

# Criar servidor
httpserver = http.server.HTTPServer(
    ('localhost', 4040), handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./openssl/cert.pem', './openssl/private.pem')

# Deixando o servidor seguro passando o socket por entre o TLS
httpserver.socket = context.wrap_socket(
    httpserver.socket, server_side=True)

print("OBSERVAÇÃO:" +
      "\n Esta questão pede para utilizar um certificado válido" +
      "\n Porém isso não é possível para um servidor em localhost, da forma como ocorre com websites" +
      "\n A forma como ocorre com websites é tendo uma autoridade certificadora gerando o certificado" +
      "\n Isso não é possível desde 2015 (!) pois ninguém realmente \"possui\" localhost" +
      "\n O localhost não possui um top level domain" +
      "\n Portanto a unica forma de eliminar o aviso de certificado inválido é" +
      "\n adicionando o certificado à lista de certificados válidos do SO" +
      "\n Como fazer isso no windows: https://learn.microsoft.com/en-us/skype-sdk/sdn/articles/installing-the-trusted-root-certificate" +
      "\n Fonte: https://comodosslstore.com/resources/ssl-certificate-for-localhost/"
      )
print("servidor rodando... acesse https://localhost:4040 no seu navegador. \n -> Não esqueça de adicionar o https antes!!")

httpserver.serve_forever()
