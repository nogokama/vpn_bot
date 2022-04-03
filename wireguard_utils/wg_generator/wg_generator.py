import subprocess


class KeyPair:
    def __init__(self, private_key="", public_key=""):
        self.private_key = str(private_key)
        self.public_key = str(public_key)


class WgGenerator:
    def __init__(self):
        pass

    @staticmethod
    def gen_new_key_pair() -> KeyPair:
        result = subprocess.run(["wg", "genkey"], stdout=subprocess.PIPE)
        private_key = result.stdout

        p = subprocess.Popen(["wg", "pubkey"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        public_key = p.communicate(input=private_key)[0]

        return KeyPair(str(private_key, "utf-8")[:-1], str(public_key, encoding="utf-8")[:-1])
