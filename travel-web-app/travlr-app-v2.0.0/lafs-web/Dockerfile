# Base image Node v10
FROM node:10

# Create app directory
WORKDIR /usr/src/lafs

# Wildcard ensures app dependencies (package.json and package-lock.json) are copied where available (npm@5+)
COPY package*.json ./

# Install Angular
RUN npm install -g @angular/cli@v6-lts 
# Install dependencies
RUN npm install
# RUN npm ci --only=production  # production only

# Bundle app source (copies all files in the app)
COPY . .

# Expose port 3000 outside container
EXPOSE 4200
# http://localhost:3000 or http://localhost:3000/explorer

# Default command to start application
#CMD ["node", "server/server.js"]
CMD ["ng", "serve", "--host", "0.0.0.0"]
