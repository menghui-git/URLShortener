FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default

COPY sites-enabled/ /etc/nginx/sites-enabled
COPY static/ /usr/share/nginx/static