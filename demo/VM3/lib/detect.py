from config import LENGTH_SHINGLE, FUZZY_LENGTH, p_x, RELEASE_RATIO
from preprocess import preprocess_sensitive_data
from pybloom_live import BloomFilter
import pyrabin_fingerprint

def postprocess_traffic(traffic_data, fingerprints, threshold):
    # check the fingerprint in original (non-fuzzy form) in entire set
    T = set()
    shingle = [traffic_data[i:i+LENGTH_SHINGLE] for i in range(len(traffic_data) - LENGTH_SHINGLE + 1)]
    
    for s in shingle:
        f = pyrabin_fingerprint.rabin_fingerprint(s, p_x)
        if f in fingerprints:
            T.add(f)
    if len(T)/min(len(traffic_data), len(fingerprints)) > threshold:
        print("Sensitive data detected!")
    else:
        print("No sensitive data detected!")
    

def detect_traffic(traffic_data, fuzzy_fingerprints, count_fingerprints, threshold):
    # fingerprint in partial set of fuzzy form
    T_hat = set()
    shingle = [traffic_data[i:i+LENGTH_SHINGLE] for i in range(len(traffic_data) - LENGTH_SHINGLE + 1)]
    fingerprints = [pyrabin_fingerprint.rabin_fingerprint(s, p_x) for s in shingle]
    print(fingerprints)
    for s in shingle:
        f_dash = pyrabin_fingerprint.rabin_fingerprint(s, p_x)
        f_dash >>= FUZZY_LENGTH
        if f_dash in fuzzy_fingerprints:
            T_hat.add(f_dash)
    print(len(T_hat))
    print(len(traffic_data))
    if len(T_hat) / (min(count_fingerprints, len(traffic_data)) * RELEASE_RATIO) > threshold:
        print(len(T_hat) / (min(count_fingerprints, len(traffic_data)) * RELEASE_RATIO))
        print("Sensitive data detected!")
        return True;
    else:
        print(len(T_hat) / (min(count_fingerprints, len(traffic_data)) * RELEASE_RATIO))
        print("No sensitive data detected!")
        return False;


sensitive_data = bytes()

# read sensitive data from file: MOCK_DATA.csv
with open("MOCK_DATA.csv", "rb") as file:
    sensitive_data = file.read()


fuzzy_fingerprints, count_fingerprints = preprocess_sensitive_data(sensitive_data)

traffic_data = "My name is Le Thanh Dat".encode('utf-8')
T_hat = detect_traffic(traffic_data, fuzzy_fingerprints, count_fingerprints, threshold=0.6)

