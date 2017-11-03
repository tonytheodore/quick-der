# Stubs for quick_der.primitive (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

def der_prefixhead(tag, body): ...
def der_format_STRING(sval): ...
def der_parse_STRING(derblob): ...
def der_format_OID(oidstr, hdr: bool = ...): ...
def der_parse_OID(derblob): ...
def der_format_RELATIVE_OID(oidstr): ...
def der_parse_RELATIVE_OID(oidstr): ...
def der_format_BITSTRING(bitint): ...
def der_parse_BITSTRING(derblob): ...
def der_format_UTCTIME(tstamp): ...
def der_parse_UTCTIME(derblob): ...
def der_format_GENERALIZEDTIME(tstamp): ...
def der_parse_GENERALIZEDTIME(derblob): ...
def der_format_BOOLEAN(bval): ...
def der_parse_BOOLEAN(derblob): ...
def der_format_INTEGER(ival, hdr: bool = ...): ...
def der_parse_INTEGER(derblob): ...
def der_format_REAL(rval): ...
def der_parse_REAL(): ...