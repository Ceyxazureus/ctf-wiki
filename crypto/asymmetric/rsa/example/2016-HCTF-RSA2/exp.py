from pwn import *
from hashlib import sha512
import time
sh = remote('127.0.0.1', 9999)
context.log_level = 'debug'

k = 2048
key = "abcdefg1"


def pi_b(x, m):
    '''
	m:
	1: encrypt
	0: decrypt
	'''
    enc = DES.new(key)
    if m:
        method = enc.encrypt
    else:
        method = enc.decrypt
    s = long_to_bytes(x)
    sp = [s[a:a + 8] for a in xrange(0, len(s), 8)]
    r = ""
    for a in sp:
        r += method(a)
    return bytes_to_long(r)


def sha512_proof(prefix, verify):
    i = 0
    pading = ""
    while True:
        try:
            i = randint(0, 1000)
            pading += str(i)
            if len(pading) > 200:
                pading = pading[200:]
            #print pading
        except StopIteration:
            break
        r = sha512(prefix + pading).hexdigest()
        if verify in r:
            return pading


def verify():
    sh.recvuntil("Prefix: ")
    prefix = sh.recvline()
    print len(prefix)
    prefix = prefix[:-1]
    prefix = prefix.decode('base64')
    proof = sha512_proof(prefix, "fffffff")
    sh.send(proof.encode('base64'))


if __name__ == '__main__':
    verify()
    print 'verify success'
    sh.recvuntil("token: ", timeout=1)
    token = "5c9597f3c8245907ea71a89d9d39d08e"
    sh.sendline(token)

    sh.recvuntil("n: ")
    n = sh.readline().strip()
    n = int(n[2:-1], 16)

    sh.recvuntil("e: ")
    e = sh.readline().strip()
    e = int(e[2:-1], 16)

    sh.recvuntil("e2: ")
    e2 = sh.readline().strip()
    e2 = int(e2[2:-1], 16)

    sh.recvuntil("is: ")
    enc_flag = sh.readline().strip()
    enc_flag = int(enc_flag[2:-1], 16)
    print "n: ", hex(n)
    print "e: ", hex(e)
    print "e2: ", hex(e2)
    print "flag: ", hex(enc_flag)
