# Production stage
FROM node:lts-alpine3.22

WORKDIR /app

COPY . .

# Install serve for serving static files
RUN npm ci --legacy-peer-deps

# Expose port 5173
EXPOSE 5173

# Run serve on port 5173
CMD ["npm", "run", "dev"]
