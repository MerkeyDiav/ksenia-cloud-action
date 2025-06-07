FROM node:18

WORKDIR /app



# Installer netcat via netcat-openbsd
RUN apt-get update && apt-get install -y bash netcat-openbsd
COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3003

# Rendre le script exécutable
RUN chmod +x wait-for.sh

# Utiliser wait-for.sh comme point d’entrée
CMD ["bash", "./wait-for.sh", "db", "3306", "--", "node", "index.js"]


