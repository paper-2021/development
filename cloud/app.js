const express = require('express')
const app = express()
const { upload } = require('./imageMiddleware')

const port = 8000

app.use(express.static('public'));

app.post('/image', upload, (req, res) => {
    res.status(200).json({'msg' : 'Image upload success'})
})

app.use('/', (req, res) => {
    res.status(200).json({'msg' : 'Hello World'})
})

app.listen(port, () => {
	  console.log(`app listening ${port}`)
})
