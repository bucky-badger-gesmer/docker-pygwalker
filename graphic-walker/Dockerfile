FROM node:lts-alpine3.22

WORKDIR /app

COPY . .

RUN npm ci --legacy-peer-deps

EXPOSE 5173

CMD ["npm", "run", "dev"]
