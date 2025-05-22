# Airflow Webserver - LDAP Configuration

A webserver config file to integrate Airflow with LDAP and RBAC

???-  "Airflow LDAP configuration"
    ```bash
    from airflow.www.fab_security.manager import AUTH_LDAP
    AUTH_TYPE=AUTH_LDAP
    #AUTH_TYPE = AUTH_LDAP
    #AUTH_LDAP_SERVER = "ldap://adldap.in.ril.com"
    AUTH_LDAP_SERVER="ldaps://adldaps.in.ril.com:636"
    AUTH_LDAP_USE_TLS = False
    AUTH_LDAP_ALLOW_SELF_SIGNED = True
    #AUTH_LDAP_TLS_CACERTFILE = "/etc/pki/ca-trust/source/anchors/ldap.crt"
    AUTH_LDAP_TLS_CACERTFILE = "/data/airflow/ldap_combined.pem"
    # registration configs
    AUTH_USER_REGISTRATION = True  # allow users who are not already in the FAB DB
    AUTH_USER_REGISTRATION_ROLE = "Public"  # this role will be given in addition to any AUTH_ROLES_MAPPING
    AUTH_LDAP_FIRSTNAME_FIELD = "givenName"
    AUTH_LDAP_LASTNAME_FIELD = "sn"
    AUTH_LDAP_EMAIL_FIELD = "mail"  # if null in LDAP, email is set to: "{username}@email.notfound"
    # bind username (for password validation)
    AUTH_LDAP_BIND_USER = "CN=TrinoDatalake,OU=SERVICEACCT,DC=in,DC=abc,DC=com"  
    AUTH_LDAP_BIND_PASSWORD = "Datalake@2023"  # the special bind password for search
    #AUTH_LDAP_USERNAME_FORMAT = "cn=%s,OU=FTE,OU=USERS,OU=CORPORATE,OU=ABC,DC=in,DC=abc,DC=com"  # %s is replaced with the provided username
    AUTH_LDAP_SEARCH = "DC=in,DC=abc,DC=com"  # the LDAP search base (if non-empty, a search will ALWAYS happen)
    AUTH_LDAP_UID_FIELD = "cn"  # the username field
    ```

Restart the airflow webserver
