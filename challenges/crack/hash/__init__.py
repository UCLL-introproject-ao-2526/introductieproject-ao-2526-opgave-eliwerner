import hashlib
import itertools
import string

# De hash die we willen kraken
target_hash = "10ceee87f8b145ab495c3bca73b94455970159c6"

# Alle hoofdletters
letters = string.ascii_uppercase

# Lengte van het wachtwoord
password_length = 7

count = 0  # teller voor het aantal pogingen

# itertools.product geeft alle combinaties van lengte 7
for combo in itertools.product(letters, repeat=password_length):
    # Van tuple naar string maken
    password = ''.join(combo)
    count += 1  # teller verhogen

    # Toon progressie elke 1.000.000 pogingen
    if count % 1_000_000 == 0:
        print(f"Tried {count:,} passwords… last = {password}")

    # SHA-1 hash maken
    hash_object = hashlib.sha1(password.encode())
    hash_hex = hash_object.hexdigest()
    
    # Vergelijken met de target hash
    if hash_hex == target_hash:
        print("\nWachtwoord gevonden:", password)
        break



# ik heb dit met de hulp van chatgpt, ik heb het niet uren kunnen laten runnen, dus hoop dat het werkt.

