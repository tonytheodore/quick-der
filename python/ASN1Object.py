#DONE# share the bindata and ofslen structures with sub-objects (w/o cycles)
#DONE# add the packer data to the ASN1Object
#DONE# add a der_pack() method
#TODO# generate rfc1234.TypeName classes (or modules, or der_unpack functions)
#DONE# deliver ASN1Object from the der_unpack() called on rfc1234.TypeName
#DONE# manually program a module _quickder.so to adapt Quick DER to Python
#DONE# support returning None from OPTIONAL fields
#DONE# support a __delattr__ method (useful for OPTIONAL field editing)
#DONE# is there a reason, any reason, to maintain the (ofs,len) form in Python?
#DONE# enjoy faster dict lookups with string interning (also done for fields)


if not 'intern' in dir (__builtins__):
	from sys import intern


# We need two methods with Python wrapping in C plugin module _quickder:
# der_pack() and der_unpack() with proper memory handling
#  * Arrays of dercursor are passed as [(ofs,len)]
#  * Bindata is passed as Python strings
import _quickder


# The ASN1Object is a nested structure of class, accommodating nested fields.
# Nesting instances share the bindata list structures, which they modify
# to retain sharing.  The reason for this is that a future der_pack() on the
# class must use changes made in the nested objects as well as the main one.

class ASN1Object (object):

	def __init__ (self, der_packer='\x00', structure={}, bindata=[], ofs=0):
		ASN1Object.der_packer = der_packer
		ASN1Object.structure = structure
		ASN1Object.bindata = bindata
		ASN1Object.offset = ofs
		numcursori = 0
		# Static structure is generated from the ASN.1 grammar
		# Iterate over this structure to forming the instance data
		for (k,v) in structure.items ():
			numcursori = numcursori + 1
			if type (k) != type (""):
				raise Exception ("ASN.1 structure keys can only be strings")
			# Interned strings yield faster dictionary lookups
			# Field names in Python are always interned
			k = intern (k.replace ('-', '_'))
			if type (v) == type (13):
				# Numbers refer to a dercursor index number
				ASN1Object.structure [k] = ofs + v
			elif type (v) == type ((0,)):
				# (class,suboffset) tuples are type references
				# such late linking allows any class order
				(subcls,subofs) = v
				assert (issubclass (subcls, ASN1Object))
				assert (type (subofs) == type (13))
				ASN1Object.structure [k] = subcls (
							bindata,
							v.structure,
							ofs + subofs )
			elif type (v) == type ({}):
				# dictionaries are ASN.1 constructed types
				ASN1Object.structure [k] = ASN1Object (
							bindata,
							structure [k],
							ofs )
			else:
				raise Exception ("ASN.1 structure values can only be int, dict or (subclass,suboffset) tuples")
		ASN1Object.numcursori = numcursori

	def _name2idx (self, name):
		while not ASN1Object.structure.has_key (name):
			if name [-1:] == '_':
				name = name [:1]
				continue
			raise AttributeError (name)
		return ASN1Object.structure [name]

	def __setattr__ (self, name, val):
		idx = self._name2idx (name)
		ASN1Object.bindata [idx] = val

	def __delattr__ (self, name):
		idx = self._name2idx (name)
		ASN1Object.bindata [idx] = None

	def __getattr__ (self, name):
		idx = self._name2idx (name)
		return ASN1Object.bindata [idx]

	def der_pack (self):
		"""Pack the current ASN1Object using DER notation.
		   Follow the syntax that was setup when this object
		   was created, usually after a der_unpack() operation
		   or a der_unpack (ClassName, bindata) or empty(ClassName)
		   call.  Return the bytes with the packed data.
		"""
		bindata = ASN1Object.bindata [ASN1Object.offset:ASN1Object.offset+ASN1Object.numcursori]
		return _quickder.der_pack (self.der_packer, bindata)



# Usually, the GeneratedTypeNameClass is generated by asn2quickder in a module
# named by the specification, for instance, quick-der.rfc4511.LDAPMessage

class GeneratedTypeNameClass (ASN1Object):

	der_packer = '\x30\x04\x04\x00'
	structure = { 'hello': 0, 'world': 1 }

	def __init__ (self, der_data=None):
		if der_data is not None:
			cursori = _quickder.der_unpack (der_packer, der_data, 2)
		else:
			cursori = [None] * 2 #TODO# 2 is an example
		super (GeneratedTypeNameClass, self).__init__ (
			structure={ 'hello':0, 'world':1 }, 
			bindata = cursori )


# A few package methods, instantiating a class

def der_unpack (der_data, cls):
	if not issubclass (cls, ASN1Object):
		raise Exception ('You can only unpack to an ASN1Object')
	if der_data is None:
		raise Exception ('No DER data provided')
	return cls (der_data=der_data)

def empty(cls):
	if not issubclass (cls, ASN1Object):
		raise Exception ('You can only create an empty ASN1Object')
	return cls ()


# class LDAPMessage (ASN1Object):
if True:

	der_packer = '\x30\x04\x04\x00'
	structure = { 'hello': 0, 'world': 1 }
	bindata = ['Hello', 'World']

	# def unpack (self):
	# 	return ASN1Object (bindata=self.bindata, structure=self.structure)

	def unpack ():
		return ASN1Object (der_packer=der_packer, bindata=bindata, structure=structure)


# 
# class LDAPMessage2 (ASN1Object):
# 
# 	bindata = 'Hello World'
# 	ofslen = [ (0,5), (6,5) ]
# 	structure = { 'hello': 0, 'world': 1 }
# 
# 	def __init__ (self):
# 		super (LDAPMessage2,self).__init__ (
# 			bindata='Hello World',
# 			ofslen=[ (0,5), (6,5) ],
# 			structure={ 'hello':0, 'world':1 })
# 
# 
# # a1 = ASN1Wrapper (bindata, ofslen, structure)
# # a1 = ASN1Object (bindata, ofslen, structure)
# # a1 = LDAPMessage ()
# a1 = LDAPMessage2 ()

a1=unpack()

print 'Created a1'

print a1.hello, a1.world

a1.world = 'Wereld'
a1.hello = 'Motjo'

print a1.hello, a1.world

del a1.hello

print a1.hello, a1.world

a1.hello = 'Hoi'
print a1.hello, a1.world

pepe = a1.der_pack ()
print 'pepe.length =', len (pepe)
print 'pepe.data =', ''.join (map (lambda c:'%02x '%ord(c), pepe))

(tag,tlen,hlen) = _quickder.der_header (pepe)
print 'der_header (pepe) =', (tag,tlen,hlen)
pepe2 = pepe [hlen:]
while len (pepe2) > 0:
	print 'pepe2.length =', len (pepe2)
	print 'pepe2.data =', ''.join (map (lambda c:'%02x '%ord(c), pepe2))
	(tag2,tlen2,hlen2) = _quickder.der_header (pepe2)
	print 'der_header (pepe2) =', (tag2,tlen2,hlen2)
	if len (pepe2) == hlen2+tlen2:
		print 'Will exactly reach the end of pepe2'
	pepe2 = pepe2 [hlen2+tlen2:]

a3 = empty (GeneratedTypeNameClass)

print 'EMPTY:', a3.hello, a3.world

a2 = der_unpack (pepe, GeneratedTypeNameClass)

print 'PARSED:', a2.hello, a2.world

