# Dockerfile
FROM node:latest-alpine as build

WORKDIR /app

COPY app/package*.json ./
COPY /app .

RUN npm ci
RUN npm run build

FROM node:latest-alpine as prod

WORKDIR /app
COPY app/package.json app/package-lock.json ./
RUN npm ci --production

FROM node:latest-alpine

WORKDIR /app
COPY --from=build /app/__sapper__/build __sapper__/build
COPY --from=build /app/static static
COPY --from=prod /app .

CMD ["node", "__sapper__/build"]
