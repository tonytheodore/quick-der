include_directories(${CMAKE_SOURCE_DIR}/include)

# Test X509 decode/encode
add_executable (certio.test
	certio.c)
target_link_libraries (certio.test
	quickderStatic)
add_test(certio-c-test
	certio.test ${CMAKE_CURRENT_SOURCE_DIR}/verisign.der)
add_test(certio-py-test
	python ${CMAKE_CURRENT_SOURCE_DIR}/certio.py ${CMAKE_CURRENT_SOURCE_DIR}/verisign.der)

# Test construction of an empty instance
add_test(empty-py-test
	python ${CMAKE_CURRENT_SOURCE_DIR}/empty-instance.py)
add_test(pack-py-test
	python ${CMAKE_CURRENT_SOURCE_DIR}/der_format.py)

if (SPEC_RFC)
    # LDAP tests only work if the LDAP ASN.1 bindings have been generated
	add_executable (ldap.test
		ldapsearch.c)

	add_dependencies(ldap.test rfc-modules)

	target_include_directories(ldap.test PUBLIC ${CMAKE_BINARY_DIR}/rfc)
	target_link_libraries(ldap.test
		quickderStatic)
	add_test (ldap.test.0
		ldap.test ${CMAKE_CURRENT_SOURCE_DIR}/ldap-search-request-0.bin)
	add_test (ldap.test.1
		ldap.test ${CMAKE_CURRENT_SOURCE_DIR}/ldap-search-request-1.bin)
	add_test (ldap.test.2
		ldap.test ${CMAKE_CURRENT_SOURCE_DIR}/ldap-search-request-2.bin)
endif ()

add_executable (der_data.test
	der_data.c)
target_link_libraries(der_data.test
	quickderStatic)
add_test (der_data.test
	der_data.test)
