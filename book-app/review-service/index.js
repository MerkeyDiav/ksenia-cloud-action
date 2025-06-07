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
        console.error("Echec connexion a la bd", err)
    }else{
        console.log("connexion reussie")
    }
})


app.get('/reviews/:bookId', (req, res) => {
    const bookId = req.params.bookId;

    db.query('SELECT * FROM reviews WHERE book_id = ?', [bookId], (err, results) => {
        if (err) {
            console.error('Erreur lors de la récupération des critiques', err);
            return res.status(500).json({ error: 'Erreur base de données' });
        }

        res.json(results);
    });
});

app.get('/', (req, res)=>{
    res.send('Lancement du review service')
})

app.post('/reviews', (req, res)=>{
    const {bookId, content} = req.body;
    if(!bookId || !content){
        return res.status(404).json({error: 'id et contenu requis'})
    }
    const sql = 'INSERT INTO reviews (book_id, content) VALUES (?,?)';
    db.query(sql, [bookId, content], (err, results)=>{
        if(err){
            console.error('Erreur lors de insertion de la critique', err)
            return res.status(500).json({error: 'Erreur de la bd'})
        }
        res.status(201).json({id: results.insertId, bookId, content})
    })
})

app.listen(3003, () => {
    console.log('Demarrage du review service au port 3003')
})