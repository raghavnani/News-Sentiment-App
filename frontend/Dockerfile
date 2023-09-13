
FROM  node:alpine as builder
WORKDIR '/app'

COPY ./package.json ./

RUN npm install

COPY . ./

RUN npm run build

FROM nginx:alpine


EXPOSE 3000

COPY default.conf /etc/nginx/conf.d/default.conf

# Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

#RUN rm -rf /usr/share/nginx

#RUN cd /usr/share/ && mkdir nginx && cd nginx && mkdir html

COPY --from=builder /app/www /usr/share/nginx/html/
