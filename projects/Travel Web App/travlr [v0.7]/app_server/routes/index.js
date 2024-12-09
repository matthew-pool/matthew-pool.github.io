// Pass request for site's default starting page to main controller

// TODO: change 'var' to 'const' or 'let'

// Import express module
var express = require('express');
// Create new router object
var router = express.Router();

// Reference to controller's main file
const ctrlMain = require('../controllers/main');

/* GET home page. */
// Define route for GET request to home page
// GET request to root URL '/' executes index method from ctrlMain
router.get('/', ctrlMain.index);  // Get index method from controller's main file

// Export router object to be used by other parts of app
module.exports = router;
