from .config import LENGTH_SHINGLE, FUZZY_LENGTH, RELEASE_RATIO, p_x
from pybloom_live import BloomFilter
import random 
import pyrabin_fingerprint

def generate_fuzzy_fingerprints(fingerprints, ratio=RELEASE_RATIO):
    fuzzy_fingerprints = []
    for f in fingerprints:
        f_perturbed = f >> FUZZY_LENGTH
        fuzzy_fingerprints.append(f_perturbed)
    print("Fuzzy Fingerprints: ", len(fuzzy_fingerprints))
    return random.choices(list(fuzzy_fingerprints), k=int(len(fuzzy_fingerprints) * ratio))

def preprocess_sensitive_data(data):
    # 1. Shingle the data
    shingle = [data[i:i+LENGTH_SHINGLE] for i in range(len(data) - LENGTH_SHINGLE + 1)]

    # 2. compute the fingerprint of each shingle
    S = {pyrabin_fingerprint.rabin_fingerprint(s, p_x) for s in shingle} # set of fingerprints
    
    # 3. Generate fuzzy fingerprints
    fuzzy_fingerprints = generate_fuzzy_fingerprints(S)
    print(fuzzy_fingerprints)
    bf = BloomFilter(capacity=10000, error_rate=0.001)
    for fingerprint in fuzzy_fingerprints:
        bf.add(fingerprint)
    # 4. Add to a bloom filter 
    return bf, len(fuzzy_fingerprints)

def generate_original_fingerprints(data):
    shingle = [data[i:i+LENGTH_SHINGLE] for i in range(len(data) - LENGTH_SHINGLE + 1)]
    S = {pyrabin_fingerprint.rabin_fingerprint(s, p_x) for s in shingle} # set of fingerprints
    bf = BloomFilter(capacity=50000, error_rate=0.001)
    for fingerprint in S:
        bf.add(fingerprint)
    return bf