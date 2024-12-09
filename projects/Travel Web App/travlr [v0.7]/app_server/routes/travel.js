// Router for travlr controller

// TODO: change var to const or let

// import express module
var express = require('express');
// Create new router object
var router = express.Router();
// Reference to travel controller file
var controller = require('../controllers/travel');

/* GET travel page */
// Define route for GET request to travel page
// GET request to root URL '/' executes travel method from controller
router.get('/', controller.travel);

// Export express router object
module.exports = router;
