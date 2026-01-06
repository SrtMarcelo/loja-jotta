const mysql = require('mysql2');
const express = require('express');
const path = require('path');
const app = express();

// Simplificado: Removemos as duplicatas e mantivemos o essencial
app.use(express.json()); 

app.use(express.static(path.join(__dirname, 'site-jotta')));

const connection = mysql.createConnection({
  host: process.env.MYSQLHOST,
  user: process.env.MYSQLUSER,
  password: process.env.MYSQLPASSWORD,
  database: process.env.MYSQLDATABASE,
  port: process.env.MYSQLPORT || 3306
});
// Rota principal
app.get('/', (req, res) => {
 res.sendFile(path.join(__dirname, 'site-jotta', 'loja.html'));
});

// --- ROTA DE CADASTRO ---
app.post('/cadastrar', (req, res) => {
  const { nome, email, senha } = req.body;
  const query = 'INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)';
  
  connection.query(query, [nome, email, senha], (err, result) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ erro: 'Erro ao cadastrar usuário.' });
    }
    res.json({ mensagem: 'Usuário cadastrado com sucesso!' });
  });
});

// --- ROTA DE LOGIN ---
app.post('/login', (req, res) => {
  const { email, senha } = req.body;
  const query = 'SELECT * FROM usuarios WHERE email = ? AND senha = ?';
  
  connection.query(query, [email, senha], (err, results) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ erro: 'Erro interno no servidor' });
    }
    
    if (results.length > 0) {
      res.json({ mensagem: 'Acesso Autorizado!' });
    } else {
      res.status(401).json({ erro: 'E-mail ou senha incorretos.' });
    }
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});