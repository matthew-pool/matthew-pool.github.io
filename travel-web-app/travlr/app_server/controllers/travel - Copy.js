// Controller for travlr page

const tripsEndpoint = 'http://localhost:3000/api/trips';
const options = {
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
}

// Use built-in Node.js file system component to read data file
//var fs = require('fs');
//var trips = JSON.parse(fs.readFileSync('./data/trips.json', 'utf8'));  // TODO: change from reading JSON file every server request, once in production env

/* GET travel view */
// travel arrow function (expression)
const travel = async function(req, res, next) {
    // console.log('TRAVEL CONTROLLER BEGIN');
    await fetch(tripsEndpoint, options)  // fetch(url, options)
        .then(res => res.json())    // outputs fetch results as JSON    
        .then(json => {             // passes JSON object to render method
            // console.log(json);
            let message = null;
            if(!(json instanceof Array)) {
                message = 'API lookup error';
                json = [];
            } else {
                if(!json.length) {
                    message = 'No trips exist in our database!';
                }
            }
            // Render travel view and pass title parameter
            res.render('travel', {title: 'Travlr Getaways', trips: json});
        })
        .catch(err => res.status(500).send(e.message));
    // console.log('TRAVEL CONTROLLER AFTER RENDER');
};

// Export travel function to make it available to other parts of the app
module.exports = {
    travel
};
