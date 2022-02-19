const express = require("express")
const router = express.Router()
const db = require('./BDD')


router.post('/AllSeries',db.AllSeries)



module.exports = router;