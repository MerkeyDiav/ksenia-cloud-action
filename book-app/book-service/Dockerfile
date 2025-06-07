FROM node:18

# Étape 2 : Crée un répertoire de travail dans le container
WORKDIR /app



# Installer netcat via netcat-openbsd
RUN apt-get update && apt-get install -y bash netcat-openbsd


# Étape 3 : Copie les fichiers package.json pour installer les dépendances
COPY package*.json ./

# Étape 4 : Installe les dépendances Node.js
RUN npm install

# Étape 5 : Copie le reste des fichiers dans le container
COPY . .

# Étape 6 : Expose le port 3000 utilisé par le service
EXPOSE 3002
# Rendre le script exécutable
RUN chmod +x wait-for.sh

# Étape 7 : Démarre le service
# Utiliser wait-for.sh comme point d’entrée
CMD ["bash", "./wait-for.sh", "db", "3306", "--", "node", "index.js"]


