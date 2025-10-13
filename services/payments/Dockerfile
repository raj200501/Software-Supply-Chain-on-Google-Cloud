# syntax=docker/dockerfile:1
FROM node:18-slim AS base
WORKDIR /app
COPY package.json ./
COPY src ./src
EXPOSE 8083
CMD ["node", "src/server.js"]
