# Dockerfile
FROM node:12-alpine as build

RUN apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers autoconf automake make nasm python git && \
  npm install --quiet node-gyp -g

WORKDIR /app

COPY app/package*.json ./
COPY /app .

RUN npm ci
RUN npm run build

FROM node:12-alpine as prod

RUN apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers autoconf automake make nasm python git && \
  npm install --quiet node-gyp -g

WORKDIR /app
COPY app/package.json app/package-lock.json ./
RUN npm ci --production

FROM node:12-alpine

WORKDIR /app
COPY --from=build /app/__sapper__/build __sapper__/build
COPY --from=build /app/static static
COPY --from=prod /app .

CMD ["node", "__sapper__/build"]
