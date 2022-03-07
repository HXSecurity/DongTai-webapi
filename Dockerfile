FROM python:3.7.7
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-key fingerprint ABF5BD827BD9BF62 \
    && apt-get update -y \
    && apt install -y gettext libc6-dev unzip curl vim cron swig
    
RUN curl -L https://github.com/Endava/cats/releases/download/cats-7.0.1/cats-linux -o  /usr/local/bin/cats \
	&& chmod +x /usr/local/bin/cats \
	&& ln -s /usr/local/bin/cats /usr/bin/cats

COPY requirements-prod.txt /opt/dongtai/webapi/requirements.txt
RUN pip3 install -r /opt/dongtai/webapi/requirements.txt

COPY . /opt/dongtai/webapi
WORKDIR /opt/dongtai/webapi

RUN python manage.py compilemessages

ENTRYPOINT ["/bin/bash","/opt/dongtai/webapi/docker/entrypoint.sh"]
