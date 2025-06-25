## Jupyter Notebook Install

???-  "Install kerberos package to connect to HDFS or Kerberos Kafka"
      ```bash
        yum install krb5-workstation krb5-libs krb5-kdc krb5-config krb5-user 
        ```

???-  "Download miniconda and setup"
        ```bash
        mkdir -p ~/miniconda3
        wget https://repo.anaconda.com/miniconda/Miniconda3-py39_24.9.2-0-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
        bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
        rm ~/miniconda3/miniconda.sh
        source ~/miniconda3/bin/activate
        conda init --all
        ```

???-  "Install required packages"
    ```bash
    pip install --no-cache-dir  --no-deps -r requirements.txt
    pip install jupyter jupyter-notebook
    ```

???-  "Generate config file"
    ```bash
    jupyter notebook --generate-config
    wget https://github.com/manish-chet/DataEngineering/blob/main/jupyter/jupyter_notebook_config.py
    ```
???-  "Start the Notebook"
    ```bash
     nohup jupyter notebook >> /home/jupyter/jupyterui.log 2>&1 &
    ```

## JupyterHub Install

???-  "Install NodeJS and NPM"
    ```bash 
    yum install nodejs npm
    npm install -g configurable-http-proxy
    ```

???-  "Install packages and dependencies"
    ```bash
    python -m venv /data1/jupyterhub/
    source /data1/jupyterhub/bin/activate
    /data1/jupyterhub/bin/python -m pip install wheel
    /data1/jupyterhub/bin/python -m pip install ipywidgets
    /data1/jupyterhub/bin/python -m pip install jupyterhub==4.1.5
    /data1/jupyterhub/bin/python -m pip install jupyterlab==4.2.0
    /data1/jupyterhub/bin/python -m pip install jupyterhub-ldapauthenticator==1.3.2
    /data1/jupyterhub/bin/python -m pip install pyspark==3.0.1
    /data1/jupyterhub/bin/python -m pip install --no-cache-dir  --no-deps -r requirements.txt
    /data1/jupyterhub/bin/python -m pip install spylon-kernel
    /data1/jupyterhub/bin/python -m pip install --no-cache-dir  --no-deps mysqlclient
    ```

???-  "Generate config file"
        ```bash
        mkdir -p /data1/jupyterhub/etc/jupyterhub/
        cd /data1/jupyterhub/etc/jupyterhub/
        /data1/jupyterhub/bin/jupyterhub --generate-config
        wget https://github.com/manish-chet/DataEngineering/blob/main/jupyter/jupyterhub_config.py
        ```

???-  "Create a systemd service"
    ```bash
    sudo mkdir -p /data1/jupyterhub/etc/systemd
    vim /data1/jupyterhub/etc/systemd/jupyterhub.service


    [Unit]
    Description=JupyterHub
    After=syslog.target network.target
    [Service]
    User=root
    Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/data1/jupyterhub/bin"
    ExecStart=/data1/jupyterhub/bin/jupyterhub -f /data1/jupyterhub/etc/jupyterhub/jupyterhub_config.py --ip IP --port=18888
    [Install]
    WantedBy=multi-user.target

    sudo ln -s /data1/jupyterhub/etc/systemd/jupyterhub.service /etc/systemd/system/jupyterhub.service

    sudo systemctl daemon-reload
    sudo systemctl enable jupyterhub.service
    sudo systemctl start jupyterhub.service
    sudo systemctl status jupyterhub.service
    ```

???-  "For SSL"
    ```bash
    /data1/jupyterhub/bin/jupyterhub -f /data1/jupyterhub/etc/jupyterhub/jupyterhub_config.py --ip IP --port=18888 
    /data1/jupyterhub/bin/jupyterhub -f /data1/jupyterhub/etc/jupyterhub/jupyterhub_config.py --ip  IP --port 443 --ssl-key /data1/jupyterhub/etc/jupyterhub/my_ssl.key --ssl-cert /data1/jupyterhub/etc/jupyterhub/my_ssl.cert
    ```



