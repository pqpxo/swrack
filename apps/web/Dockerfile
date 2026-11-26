# version 27
FROM node:22-alpine AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json vite.config.ts svelte.config.js index.html ./
COPY src ./src
COPY static ./static
# Mount path baked into the bundle's asset and API URLs.
ARG BASE_PATH=/
ENV BASE_PATH=$BASE_PATH
RUN npm run build

# Non-root nginx (UID 101), listening on 8080.
FROM nginxinc/nginx-unprivileged:1.30.6-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
