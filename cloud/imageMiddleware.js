const multer = require('multer')
const moment = require('moment')
const fs = require('fs')

const makeDir = async(dir) => {
    if(!fs.existsSync(dir)) {
        fs.mkdirSync(dir)
    }
}

const datetimeTight = async() => {
    return moment().format('YYYYMMDDHHmmss')
}

const storage = multer.diskStorage({
    destination: async function(req, file, cb) {
        let type = file.originalname[0]
        await makeDir('public/upload/' + type)
        cb(null, 'public/upload/' + type) // file save path(backend/upload)
    },
    filename: async function(req, file, cb) {
        console.log('file name : ', file.originalname)
        cb(null, await datetimeTight() + '_' + file.originalname) // 저장되는 file명
    }
})

exports.upload = multer({ storage: storage }).single("file") // single : 하나의 file 업로드