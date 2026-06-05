# Multi-stage build: compile the React app with Node, then serve the static
# files with a small nginx image.
FROM node:22-alpine AS build

WORKDIR /app

# The API URL is baked in at build time (Vite inlines VITE_* vars).
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- Serve stage ---
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
