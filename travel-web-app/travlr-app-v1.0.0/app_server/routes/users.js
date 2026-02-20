// Import express module
var express = require('express');
// Create new router object
var router = express.Router();

/* GET users listing. */
// Define route for GET request to users listing page
// GET request for root URL '/' sends response 'respond with a resource'
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

// Export router object to make it available to other parts of the app
module.exports = router;
