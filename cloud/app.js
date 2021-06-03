const express = require('express')
const app = express()
const { upload } = require('./imageMiddleware')

const port = 8000

app.use(express.static('public'));

app.post('/image', upload, (req, res) => {
    console.log("Image upload success")
    console.log('req.type : ', req.type, ' req.fileName : ', req.fileName)
    let image_path = req.type + '/' + req.fileName
    res.status(200).json({'msg' : 'Image upload success', 'image_path' : image_path})
})

app.use('/', (req, res) => {
    res.status(200).json({'msg' : 'Hello World'})
})

app.listen(port, () => {
	  console.log(`app listening ${port}`)
})
