FROM tiangolo/uwsgi-nginx-flask:flask
RUN pip install requests
COPY nginx.conf /etc/nginx/conf.d/
COPY ./app /app
