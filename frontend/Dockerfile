# Stage 1: Build the React application
FROM node:18-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the React application
# Set relative API URL for production build
ENV REACT_APP_API_BASE_URL=/
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the built artifacts from the build stage to the Nginx html directory
COPY --from=build /app/build /usr/share/nginx/html

# Copy a custom Nginx configuration to handle client-side routing and API proxying
RUN echo 'server { \
    listen 80; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    try_files $uri $uri/ /index.html; \
    } \
    location /api/v1/ { \
    proxy_pass http://backend:8000/; \
    proxy_set_header Host $host; \
    proxy_set_header X-Real-IP $remote_addr; \
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
    proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
