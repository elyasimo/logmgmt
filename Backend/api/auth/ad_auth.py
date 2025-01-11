from ldap3 import Server, Connection, ALL, NTLM

def authenticate_active_directory(username, password, ad_server, domain):
    try:
        server = Server(ad_server, get_info=ALL)
        user = f"{domain}\\{username}"
        conn = Connection(server, user=user, password=password, authentication=NTLM)
        if conn.bind():
            return True
        return False
    except Exception as e:
        raise Exception(f"Active Directory authentication failed: {str(e)}")

