The rsa module

This file provides the RSA object, string/int/hex conversion helper
methods and basic UI methods. This is a COMPLETE file, and is useful for
testing your code. You do NOT need to edit this file or submit it. You
are welcome to learn how this file works in order to learn more about
python. You may be surprised by how short each method is, given what it
does.

The recommended usage of this file is from the interpreter. Start with:
>> python
> from rsa import *

# Examples of the various commands are below:

# encrypts the message below using someone else's public keys
> RSA.encrypt('attack at dawn', 12314, 1514231231223)

# creates a new RSA instance. Object creation calls the keygen method in
# primes.py. The public keys of this object are stored in a.n and a.e.
# You can publish these. You can optionally specify a bit length for the
# primes.
> a = RSA() #default is 64 bit
> b = RSA(256)

# encrypts this message using your own public keys as a hex string
> a.encrypt_own('attack at dawn')

# decrypts a message sent to this user with your private keys
# if this is not actually decipherable, you can get an error in the string
# conversion
> a.decrypt('2ff873a832de234')

# saves the information (n,e,d) in this RSA object into a file for later use.
> a.save('myRSA.txt')

# loads the information from another file into an RSA object
> a = RSA.load('myRSA.txt')
# now a has been loaded with the RSA object that you saved before

"""

from primegen import keygen 
from modarithmetic import expMod 
from math import ceil
import pickle

# convert the string s into ascii and then chunk the ascii into a list of integers
# so each integer is at most n (n must be at least 256)
def str_to_ints(s,n):
  b = int(n.bit_length()/8) #max number of bytes per int
  return list(int.from_bytes(s[i:i+b].encode(),'little') for i in range(0,len(s),b))

# transform a list of converted integers back into a string.
def ints_to_str(l):
  return ''.join(x.to_bytes(ceil(x.bit_length()/8),'little').decode() for x in l)

# turn a list of integers to one hex string, padded with 0s as needed
def ints_to_hex(l,n):
  b = ceil(n.bit_length()/4)
  return ''.join(hex(x)[2:].zfill(b) for x in l)

# transform hex string s into integers, each at most n
def hex_to_ints(s,n):
  b = ceil(n.bit_length()/4)
  return list(int(s[i:i+b],16) for i in range(0,len(s),b))


class RSA:
  # Creates a new RSA object, where each prime has some number of bits.
  # The default if nothing is specified is 64 bits per prime
  def __init__(self,bits=64):
    n,e,d = keygen(2**(bits-1),2**(bits))
    self.n = n
    self.e = e
    self._d = d # this is python convention for private variables

  # function encrypt(msg, e, n)
  # inputs: the message msg, the public exponent e and the public
  # modulus n
  # output: the encrypted ciphertext of msg according to the RSA
  # algorithm.
  @staticmethod
  def encrypt(msg,e,n):
    return ints_to_hex((expMod(m,e,n) for m in
            str_to_ints(msg,n)),n)

  # function encrypt_own(msg)
  # inputs: the message msg
  # output: the encrypted ciphertext of msg according to the RSA algorithm
  # using the exponent and modulus stored in 'self'
  def encrypt_own(self,msg):
    return ints_to_hex((expMod(m,self.e,self.n) for m in str_to_ints(msg,self.n)), self.n)

  # decrypt(cpt, d, n)
  # inputs: the encrypted ciphertext c, the private exponent d, and the
  # public modulus n
  # output: the decrypted msg from c according to the RSA algorithm.
  def decrypt(self,cpt):
    return ints_to_str(expMod(c,self._d,self.n) for c in hex_to_ints(cpt,self.n))

  # saves this RSA object in a given file
  def save(self,fn):
    try:
      fileo = open(fn,'wb')
      pickle.dump(self,fileo)
      fileo.close()
    except:
      print("Error while saving!")

  #loads an RSA object from a given file
  @staticmethod
  def load(fn):
    try:
      fileo = open(fn,'rb')
      a = pickle.load(fileo)
      fileo.close()
      return a
    except:
      print("Error while loading!")
