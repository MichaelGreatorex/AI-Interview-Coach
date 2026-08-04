FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY --chown=node:node app ./app
COPY --chown=node:node features ./features
COPY --chown=node:node public ./public
COPY --chown=node:node package*.json ./
COPY --chown=node:node tsconfig.json ./
COPY --chown=node:node next.config.ts ./
COPY --chown=node:node postcss.config.mjs ./
COPY --chown=node:node eslint.config.mjs ./

USER node

EXPOSE 3000

CMD ["npm", "run", "dev"]