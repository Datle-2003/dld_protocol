LENGTH_SHINGLE = 8 # Length of shingle in bytes
LENGTH_FINGERPRINT = 32 * 8 # Length of fingerprint in bytes
FUZZY_LENGTH = 10 # Length of fuzzy hash in bytes
threshold = 0.7 # Threshold for detecting sensitive data

# p_x is irredicible polynomial 33 bits
p_x = 0x104C11DB7 # 33 bits
M = 0b11111111011111111011111101111111 # mask 32 bits

# loop back address for testing
vm1_address = ("127.0.0.1", 12345)  # VM1 listening on port 12345
vm2_address = ("127.0.0.1", 12353)  # VM2 listening on port 12346
vm3_address = ("127.0.0.1", 12347)  # VM3 listening on port 12347
