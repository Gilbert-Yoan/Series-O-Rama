const express = require("express")
const router = express.Router()
const db = require('./BDD')


router.post('/AllSeries',db.AllSeries)
router.post('/UserConnect',db.UserConnect)
router.post('/CreateAccount',db.CreateAccount)
router.post('/REcherche',db.REcherche)


module.exports = router;