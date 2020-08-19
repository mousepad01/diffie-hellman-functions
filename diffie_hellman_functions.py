import secrets


def gcd(x, y):

    while x % y != 0:

        aux = x % y
        x = y
        y = aux

    return y


def logpow(exp, base, mod):

    base %= mod

    if exp == 0:
        return 1

    if exp == 1:
        return base % mod

    if exp & 1 == 0:
        return logpow(exp // 2, base ** 2, mod) % mod

    if exp & 1 == 1:
        return (base * logpow(exp // 2, base ** 2, mod) % mod) % mod


def prime_generator(b_dim):

    def ciur():
        global erath
        global primes

        erath[0] = 1
        erath[1] = 1

        i = 2
        while i <= 500:
            if erath[i] == 0:

                j = i * i
                while j <= 250000:

                    erath[j] = 1
                    j += i

            i += 1

        for i in range(2, 250000):
            if erath[i] == 0:
                primes.append(i)

    def bignumgen(b_dim):
        return secrets.randbits(b_dim)

    def checkdiv(x):
        global primes

        for i in range(20000):
            if x % primes[i] == 0:
                return 0

        return 1

    def primecheck(candidate):
        global primes

        if checkdiv(candidate) == 0:
            return False

        mod = candidate

        n_minus_1 = candidate - 1

        exp = 0

        while n_minus_1 & 1 == 0:
            n_minus_1 //= 2
            exp += 1

        dp = n_minus_1

        alist = primes[:15] + [primes[secrets.randbelow(22000) + 5] for i in range(35)]

        lalist = len(alist)

        for i in range(lalist):
            a = alist[i]

            ad = logpow(dp, a, mod)

            if ad != 1 and ad != candidate - 1:

                r_found = False

                for r in range(1, exp):

                    ad *= ad
                    ad %= candidate

                    if ad == candidate - 1:
                        r_found = True

                if not r_found:
                    return False

        return True

    erath = []
    primes = []

    def primegen(b_dim):
        global erath
        global primes

        erath = [0 for i in range(250001)]
        primes = []
        ciur()

        candidate = bignumgen(b_dim)

        while not primecheck(candidate):
            candidate = bignumgen(b_dim)

        return candidate

    return primegen(b_dim)


def global_parameters():  # returns pair (global group modulus, global group generator)

    modulus = prime_generator(4096)

    g = 0

    ok = False
    while not ok:

        g_candidate = secrets.randbelow(modulus - 2) + 2

        while gcd(modulus - 1, g_candidate) == 0:
            g_candidate = secrets.randbelow(modulus - 2) + 2

        count = 0
        currently_generated = g_candidate

        while currently_generated != 1:

            count += 1

            currently_generated *= g_candidate
            currently_generated %= modulus

        if count == modulus - 2:

            ok = True
            g = g_candidate

    return modulus, g


def key_generator(global_modulus, global_generator):  # returns pair (public key, private key)

    private_key = secrets.randbelow(global_modulus - 2) + 2

    public_key = logpow(private_key, global_generator, global_modulus)

    return public_key, private_key


def common_secret_generator(public_key, own_private_key, global_modulus):

    return logpow(own_private_key, public_key, global_modulus)





