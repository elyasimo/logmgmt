import ldap

def authenticate_ldap(username, password, ldap_server):
    try:
        conn = ldap.initialize(ldap_server)
        conn.protocol_version = ldap.VERSION3
        conn.set_option(ldap.OPT_REFERRALS, 0)

        conn.simple_bind_s(username, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.SERVER_DOWN:
        raise Exception("LDAP server is not available")
    finally:
        conn.unbind_s()

