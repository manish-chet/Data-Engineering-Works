## **Jupyter Notebook Install**

!!!-  "Install kerberos package to connect to HDFS or Kerberos Kafka"
    ```
    yum install krb5-workstation krb5-libs krb5-kdc krb5-config krb5-user 
    ```

!!!-  "Download miniconda and setup"
    ```
    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-py39_24.9.2-0-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm ~/miniconda3/miniconda.sh
    source ~/miniconda3/bin/activate
    conda init --all
    ```

!!!-  "Install required packages"
    ```
    pip install --no-cache-dir  --no-deps -r requirements.txt
    pip install jupyter jupyter-notebook
    ```

!!!-  "Edit config file"
    ```
    c.NotebookApp.ip = 'ServerIP'
    c.NotebookApp.open_browser = False
    c.NotebookApp.port = 18888
    ```
!!!-  "Start the Notebook"
    ```
    nohup jupyter notebook >> /home/jupyter/jupyterui.log 2>&1 &
    ```

## **JupyterHub Install**

!!!-  "Install NodeJS and NPM"
    ``` 
    yum install nodejs npm
    npm install -g configurable-http-proxy
    ```

!!!-  "Install packages and dependencies"
    ```
    python -m venv /data1/jupyterhub/
    source /data1/jupyterhub/bin/activate
    /data1/jupyterhub/bin/python -m pip install wheel ipywidgets jupyterhub==4.1.5 jupyterlab==4.2.0 jupyterhub-ldapauthenticator==1.3.2 pyspark==3.0.1 mysqlclient spylon-kernel
    /data1/jupyterhub/bin/python -m pip install --no-cache-dir  --no-deps -r requirements.txt

    ```

!!!-  "Edit config file"
    ```
    mkdir -p /data1/jupyterhub/etc/jupyterhub/
    cd /data1/jupyterhub/etc/jupyterhub/
    /data1/jupyterhub/bin/jupyterhub --generate-config
    ------add the following for LDAP setting------
    c.LDAPAuthenticator.server_address = 'ldaps://adldaps.in.com:636'
    c.LDAPAuthenticator.use_ssl = True
    c.LDAPAuthenticator.lookup_dn = False
    c.LDAPAuthenticator.server_port = 636
    c.LDAPAuthenticator.valid_username_regex = '^[a-z][.a-z0-9_-]*$'
    c.LDAPAuthenticator.lookup_dn_search_filter = '({login_attr}={login})'
    c.LDAPAuthenticator.lookup_dn_search_user = 'username
    c.LDAPAuthenticator.lookup_dn_search_password = 'password'
    c.LDAPAuthenticator.tls_strategy = 'on_connect'
    c.LDAPAuthenticator.user_search_base = 'OU=FTE,OU=USERS,OU=CORPORATE,OU=,DC=in,DC=,DC=com'
    c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
    c.LDAPAuthenticator.lookup_dn_user_dn_attribute = 'cn'
    c.LDAPAuthenticator.escape_userdn = False
    c.LDAPAuthenticator.bind_dn_template = '{username}@abc.com'
    c.LDAPAuthenticator.debug = True
    c.LDAPAuthenticator.admin_users = {'manishkumar'}
    ```

!!!-  "Create a systemd service"
    ```
    sudo mkdir -p /data1/jupyterhub/etc/systemd
    vim /data1/jupyterhub/etc/systemd/jupyterhub.service

    ----add the following in jupyterhub.service----
    [Unit]
    Description=JupyterHub
    After=syslog.target network.target
    [Service]
    User=root
    Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/data1/jupyterhub/bin"
    ExecStart=/data1/jupyterhub/bin/jupyterhub -f /data1/jupyterhub/etc/jupyterhub/jupyterhub_config.py --ip IP --port=18888
    [Install]
    WantedBy=multi-user.target

    ----create symlink for the service----
    sudo ln -s /data1/jupyterhub/etc/systemd/jupyterhub.service /etc/systemd/system/jupyterhub.service

    ----start the service----
    sudo systemctl daemon-reload
    sudo systemctl enable jupyterhub.service
    sudo systemctl start jupyterhub.service
    sudo systemctl status jupyterhub.service
    ```

!!!-  "For SSL"
    ```
    /data1/jupyterhub/bin/jupyterhub -f /data1/jupyterhub/etc/jupyterhub/jupyterhub_config.py --ip ServerIP --port=18888 
    /data1/jupyterhub/bin/jupyterhub -f /data1/jupyterhub/etc/jupyterhub/jupyterhub_config.py --ip ServerIP --port 443 --ssl-key /data1/jupyterhub/etc/jupyterhub/my_ssl.key --ssl-cert /data1/jupyterhub/etc/jupyterhub/my_ssl.cert
    ```



