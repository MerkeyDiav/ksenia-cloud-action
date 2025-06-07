const express = require('express')
const app = express()
app.use(express.json());


const mysql = require('mysql2')
const db = mysql.createConnection({
    host:   process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'password',
    database: process.env.DB_NAME || 'bookreview_db'
})

db.connect((err)=>{
    if(err){
        console.error('Erreur de connexion à MYsql', err)
    }else {
        console.log('Connexion reussie')
    }
})




app.get('/', (req, res) => {
    res.send('Book Servoce is up')
})

app.listen(3002, ()=>{
    console.log('Book Service running on port 3002')
})

app.get('/books', (req, res)=>{
    db.query('SELECT * FROM books', (err, results) => {
        if(err){
            console.error('Erreur lors de la récuperation des livres', err);
            res.status(500).json({error: 'Erreur serveur'})
        }else {
            res.json(results)
        }
    })
})

app.post('/books', (req, res) => {
    const {title , author, description , rating} = req.body

    if(!title || !author || !description || !rating) {
        return res.status(400).json({error: 'Champs manquants'})
    }

    const query = 'INSERT INTO books (title, author, description , rating) VALUES (?, ?, ?, ?)';
    const values = [title, author, description, rating]

    db.query(query, values, (err, result)=> {
        if (err){
            console.error('Erreur en ajoutant un livre', err)
            res.status(500).json({error: 'Erreur Serveur'})
        }else {
            res.status(201).json({
                id: result.insertId,
                title, 
                author,
                description,
                rating
            })
        }
    })
})