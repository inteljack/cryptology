import random

def generate_aes_key():
    pool = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(pool) for i in range(32))
    # rnd = Crypto.Random.OSRNG.posix.new().read(AES.block_size)
    # return rnd

print generate_aes_key()
