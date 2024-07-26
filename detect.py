from config import LENGTH_SHINGLE, LENGTH_FINGERPRINT, FUZZY_LENGTH, p_x, M
from preprocess import rabin_fingerprint, preprocess_sensitive_data

def fuzzy_equivalence(f, f_star, M):
    return not (M & (f ^ f_star))

def detect_traffic(traffic_data, fuzzy_fingerprints, M):
    T_hat = set()
    shingle = [traffic_data[i:i+LENGTH_SHINGLE] for i in range(len(traffic_data) - LENGTH_SHINGLE + 1)]
    
    for s in shingle:
        f_dash = rabin_fingerprint(s, p_x)
        for f_star in fuzzy_fingerprints:
            if fuzzy_equivalence(f_dash, f_star, M):
                T_hat.add(f_dash)
                break
    return T_hat

sensitive_data = ""  

# read sensitive data from file: MOCK_DATA.csv
with open("MOCK_DATAs.csv", "r") as file:
    for line in file:
        sensitive_data += line
print(len(sensitive_data))


fuzzy_fingerprints = preprocess_sensitive_data(sensitive_data)
print(f"Fuzzy Fingerprints: {fuzzy_fingerprints}")

traffic_data = "" 
with open("MOCK_DATAt.csv", "r") as file:
    for line in file:
        traffic_data += line

print(len(traffic_data))

T_hat = detect_traffic(traffic_data, fuzzy_fingerprints, M)

print("T_hat:", T_hat)

# Output
threshold = 0.7
if len(T_hat) / len(fuzzy_fingerprints) > threshold:
    print("Sensitive data detected!")
else:
    print("No sensitive data detected!")
