LENGTH_SHINGLE = 8 # Length of shingle in bytes
LENGTH_FINGERPRINT = 32 * 8 # Length of fingerprint in bytes
FUZZY_LENGTH = 10 # Length of fuzzy hash in bytes

# p_x is irredicible polynomial 33 bits
p_x = 0x104C11DB7 # 33 bits
M = 0b11111111011111111011111101111111 # mask 32 bits

client_cert = "client_cert.pem"
client_key = "client_key.pem"
vm1_address = ("REPLACE WITH VM1 IP", 12345)
vm2_address = ("REPLACE WITH VM2 IP", 12345)
vm3_address = ("REPLACE WITH VM3 IP", 12346)
