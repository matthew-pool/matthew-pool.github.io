/* App starting point */

/**
 * Backend Server:
 *  cd <backend_directory>
 *  npm install
 *  node .
 *  HTML: http://localhost:3000
 *  JS: http://localhost:3000/travel
 *  API Explorer (LoopBack): http://localhost:3000/explorer
 * 
 * Frontend Server:
 *  cd <frontend_directory>
 *  npm install
 *  ng serve
 *  http://localhost:4200 
 * 
 */

/**
 * NOTE:  Handlebars is a JS templating engine that dynamically generates HTML
 *        and separates the presentation layer (view) from the logic layer.
 *        Handlebars also provides a way to embed variables and expressions in HTML templates.
 *        Handlebars partials allow creating reusable chunks of code (like Headers and Footers).
 */

// Imports
var createError = require('http-errors');
var express = require('express'); // Express framework
var path = require('path');       // Utility for file and directory paths
var cookieParser = require('cookie-parser');
var logger = require('morgan');   // HTTP request logger

// Route handlers
var indexRouter = require('./app_server/routes/index');   // '/'
var usersRouter = require('./app_server/routes/users');   // '/users'
var travelRouter = require('./app_server/routes/travel'); // '/travel'
var apiRouter = require('./app_api/routes/index');

// Wire in authentication module
var passport = require('passport');
require('./app_api/config/passport');

// Handlebars templating
var handlebars = require('hbs');
//===========================================================================================================

// Bring in database
require('./app_api/models/db');

// Pull contents of .env file (dotenv module) to access its variables
require('dotenv').config();

// Express app instance
var app = express();

// View engine setup
app.set('views', path.join(__dirname, 'app_server', 'views'));  // Set views directory

// Register Handlebars partials
handlebars.registerPartials(__dirname + '/app_server/views/partials');  // Set Handlebasrs partials directory

// Set Handlebars as the view engine
app.set('view engine', 'hbs');

// Middelware setup
app.use(logger('dev'));   // Log HTTP requests in 'Development' environment
app.use(express.json());  // Parse JSONs
app.use(express.urlencoded({ extended: false }));  // Parse URL-encoded bodies
app.use(cookieParser());  // Parse cookies
app.use(express.static(path.join(__dirname, 'public')));  // Serve static files from 'public' directory
app.use(passport.initialize());

// Enable CORS (Cross Origin Resource Sharing)
// Allow Angular admin site to make calls against Express backend API for external calls
app.use('/api', (req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'http://localhost:4200');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  next();
});

// Wire-up routes to controllers
app.use('/', indexRouter);          // Route handler for index (/) page
app.use('/users', usersRouter);     // Route handler for /users page
app.use('/travel', travelRouter);   // Route handler for /travel page
app.use('/api', apiRouter);         // Route handler for /api

// Catch unauthorized error and create 401
app.use((err, req, res, next) => { 
  if(err.name === 'UnauthorizedError') { 
    res 
      .status(401) 
      .json({"message": err.name + ": " + err.message}); 
  } 
});

// Catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));  // Create 404 error and pass to next middleware 
});

// Error handler
app.use(function(err, req, res, next) {
  // Set locals, only providing error in development
  res.locals.message = err.message;  // Set error message
  // Set error stack trace only in 'development'
  // '===' does not perform type coversion before comparison
  res.locals.error = req.app.get('env') === 'development' ? err : {};  // true returns err; false returns empty {}

  // Render the error page
  res.status(err.status || 500);  // Set response status code
  res.render('error');  // Render error view
});

// Export app module
module.exports = app;
