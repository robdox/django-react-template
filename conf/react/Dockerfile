FROM node:10-alpine
MAINTAINER Robert Wells <rwells@dvele.com>


WORKDIR /tmp
COPY front/package.json /tmp/

ENV NODE_ENV=development
RUN npm config set unsafe-perm true

RUN npm install yarn && \
    yarn global add webpack@4.29.6 && \
    yarn global add webpack-dev-server@3.5.1 && \
    yarn global add eslint@5.16.0 && \
    yarn install

RUN mv /tmp/node_modules /
ENV NODE_PATH=/node_modules

WORKDIR /app

# So docker is not being run as a root user
RUN chown -R node:node /app

COPY /front/package.json /app/
COPY /front/.eslintrc.json /app/

COPY /conf/react/webpack.dev.js /app/
COPY /conf/react/webpack.common.js /app/
