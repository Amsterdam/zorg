FROM amsterdam/docker_python:latest
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get install -y \
		gdal-bin \
		libgeos-dev \
		netcat \
		redis-server \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system zorg \
	&& mkdir -p /static \
	&& chown zorg /static \
	&& pip install uwsgi

WORKDIR /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

USER zorg
COPY zorg /app/
CMD /app/docker-entrypoint.sh

