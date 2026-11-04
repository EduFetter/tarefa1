import socket
import pickle

SERVER = "192.168.1.190"
PORT = 6767



#arquivo = open("pombao.jfif", "rb")
#arquivo = open("nugget.jfif", "rb")
#arquivo = open("moranguete.jfif", "rb")
arquivo = open("frutas.jfif", "rb")


message = {
    "file" : "frutas.jfif",
    "content" : arquivo.read(),
    "author" : "Edu"
}

# Serializacao
data = pickle.dumps(message, protocol=pickle.HIGHEST_PROTOCOL)







client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(data, (SERVER, PORT))
print(f"Dados enviados com {len(data)} bytes")

client.close()