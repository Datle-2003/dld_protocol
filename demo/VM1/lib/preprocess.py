from lib.config import LENGTH_SHINGLE, LENGTH_FINGERPRINT, FUZZY_LENGTH, p_x, M
import random 


def rabin_fingerprint(shingle, polynomial):
    finger_print = 0
    for byte in shingle.encode('utf-8'): # read byte by byte
        # shift the fingerprint to the left by 8 bits to make room for the next byte
        finger_print = (finger_print << 8) | byte # append the byte to the fingerprint

        # apply the polynomial
        for _ in range(8):
            if finger_print & (1 << (LENGTH_FINGERPRINT+ 8)):  # If the highest bit is set
                finger_print ^= polynomial
            finger_print <<= 1
        finger_print >>= 1
        
        return finger_print & ((1 << LENGTH_FINGERPRINT) - 1)
    
def generate_fuzzy_fingerprints(fingerprints):
    fuzzy_fingerprints = set()
    for f in fingerprints:
        f_hat = random.getrandbits(LENGTH_FINGERPRINT)
        not_M = ~M & ((1 << LENGTH_FINGERPRINT) - 1)  # Ensure not_M is pf bits long
        f_perturbed = (not_M & f_hat) ^ f
        fuzzy_fingerprints.add(f_perturbed)
    return fuzzy_fingerprints




def preprocess_sensitive_data(data):
    # 1. Shingle the data
    shingle = [data[i:i+LENGTH_SHINGLE] for i in range(len(data) - LENGTH_SHINGLE + 1)]

    # 2. compute the fingerprint of each shingle
    S = {rabin_fingerprint(s, p_x) for s in shingle} # set of fingerprints

    # 3. Generate fuzzy fingerprints
    fuzzy_fingerprints = generate_fuzzy_fingerprints(S)
    
    return fuzzy_fingerprints