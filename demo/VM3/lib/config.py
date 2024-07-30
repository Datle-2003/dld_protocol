LENGTH_SHINGLE = 8 # Length of shingle in bytes
FUZZY_LENGTH = 5 # Length of fuzzy hash in bits
RELEASE_RATIO = 0.3 # Release ratio
# p_x is irredicible polynomial 33 bits
p_x = 0x104C11DB7 # 33 bits


vm1_address = ("127.0.0.1", 12345)  # VM1 listening on port 12345
vm2_address = ("127.0.0.1", 12353)  # VM2 listening on port 12346
vm3_address = ("127.0.0.1", 12347)  # VM3 listening on port 12347
