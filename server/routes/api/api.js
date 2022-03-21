const express = require("express")
const router = express.Router()
const db = require('./BDD')


router.post('/AllSeries',db.AllSeries)
router.post('/UserConnect',db.UserConnect)
router.post('/CreateAccount',db.CreateAccount)
router.post('/REcherche',db.REcherche)
router.post('/GETRecoRAND',db.GETRecoRAND)
router.post('/TestNoter',db.TestNoter)
router.post('/RecomendationViaLike',db.RecomendationViaLike)
router.post('/SerieNonNoter',db.SerieNonNoter)
router.post('/RechercheTest',db.RechercheTest)
router.post('/RecoViaRecherche',db.RecoViaRecherche)
router.post('/TestNbMotRechercher',db.TestNbMotRechercher)
router.post('/OlderMot',db.OlderMot)
router.post('/TestMotexiste',db.TestMotexiste)
router.post('/UpdateMotRecher',db.UpdateMotRecher)
router.post('/InsertMot',db.InsertMot)
module.exports = router;