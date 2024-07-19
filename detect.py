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

sensitive_data = "My name  , i'm from Vietnam iufhewiuhriuewyrhiuwhkjsndkldsfk oidjfoewoi oweuroiwueroiw oiuroiwuoiruw oqwoiweuoirw odwjfoiewu8rtew798 ouewrweyriuwehfkjwf"  
fuzzy_fingerprints = preprocess_sensitive_data(sensitive_data)
print(f"Fuzzy Fingerprints: {fuzzy_fingerprints}")

traffic_data = "Kho;fkew oiwejoiew 09qq-q- 9e99e 999  qqq  -wq0e-wq ng co gi weriurhiue" 

T_hat = detect_traffic(traffic_data, fuzzy_fingerprints, M)

print("T_hat:", T_hat)

# Output
threshold = 0.8
if len(T_hat) / len(fuzzy_fingerprints) > threshold:
    print("Sensitive data detected!")
else:
    print("No sensitive data detected!")
