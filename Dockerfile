# Stage 1: Base image for linting
FROM node:16-alpine as lint
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npx eslint .

# Stage 2: Build
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Testing
FROM node:16-alpine as test
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm test

# Stage 4: Static Code Analysis
FROM sonarsource/sonar-scanner-cli as static-analysis
WORKDIR /usr/src

# Copy necessary project files
COPY . . 
COPY sonar-project.properties .

# Set environment variables for SonarQube configuration
ENV SONAR_HOST_URL=http://your-sonarqube-server
ENV SONAR_LOGIN=your-sonar-authentication-token
ENV PROJECT_KEY=your-project-key

# Run SonarScanner
RUN sonar-scanner \
    -Dsonar.projectKey=$PROJECT_KEY \
    -Dsonar.sources=. \
    -Dsonar.host.url=$SONAR_HOST_URL \
    -Dsonar.login=$SONAR_LOGIN


# Stage 5: Final production image
FROM node:16-alpine as production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm ci --only=production

CMD ["node", "dist/index.js"]
