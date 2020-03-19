FROM nginx

COPY nginx.sh /nginx.sh
RUN /nginx.sh