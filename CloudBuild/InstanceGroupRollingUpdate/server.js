const express = require('express');
const app = express();
app.get('/', (req, res) => {
    res.send('This is index page');
});
app.get('/users', (req, res) => {``
    res.send('lists of users');
})

app.listen(3000);