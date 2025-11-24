// Controller to retrieve a list of available trips from MongoDB database
// TODO: Integrate multiple controllers
const mongoose = require('mongoose');
const Trip = require('../models/travlr');  // Register model
const Model = mongoose.model('trips');

// GET: /trips - lists all trips
// Response must include HTML status code
// and JSON message to requesting client
const tripsList = async(req, res) => {
    const q = await Model
        .find({})  // No filter (return all records)
        .exec();

        // Show query results on console
        console.log(q);
    
    if(!q)  // Database returned no data
    {
        return res
            .status(404)  // Resource not found status code
            .json(err);
    } else {  // Database returns list
        return res
            .status(200)  // Success (OK) status code
            .json(q);
    }
};

// GET: /trips/:tripCode - lists a single trip
// Response must include HTML status code
// and JSON message to requesting client
const tripsFindByCode = async(req, res) => {
    const q = await Model
        .find({ 'code' : req.params.tripCode })  // Returns a single (filtered) record
        .exec();

        // Show query results on console
        console.log(q);
    
    if(!q)  // Database returned no data
    {
        return res
            .status(404)  // Resource not found status code
            .json(err);
    } else {  // Database returns list
        return res
            .status(200)  // Success (OK) status code
            .json(q);
    }
};

// POST: /trips - adds a new Trip.
// response includes HTML status code and JSON message to requesting client
const tripsAddTrip = async(req, res) => {
    const newTrip = new Trip({
        code: req.body.code,
        name: req.body.name,
        length: req.body.length,
        start: req.body.start,
        resort: req.body.resort,
        perPerson: req.body.perPerson,
        image: req.body.image,
        description: req.body.description
    });

    const q = await newTrip.save();

    if(!q)  // Database returned no data
    {
        return res
            .status(404)  // Resource not found status code
            .json(err);
    } else {  // Database returns list
        return res
            .status(200)  // Success (OK) status code
            .json(q);
    }

    // Show query results on console
    console.log(q);
}

// PUT: /trips/:tripCode - Updates a Trip
const tripsUpdateTrip = async(req, res) => {
    console.log(req.params); 
    console.log(req.body); 
 
    const q = await Model 
        // MongoDB findOneAndUpdate() from Mongoose
        .findOneAndUpdate( 
            { 'code' : req.params.tripCode }, 
            { 
                code: req.body.code, 
                name: req.body.name, 
                length: req.body.length, 
                start: req.body.start, 
                resort: req.body.resort, 
                perPerson: req.body.perPerson, 
                image: req.body.image, 
                description: req.body.description 
            }  
        ) 
        .exec(); 
         
        if(!q) 
        { // Database returned no data 
            return res 
                .status(400) 
                .json(err); 
        } else { // Return resulting updated trip 
            return res 
                .status(201) 
                .json(q); 
        }     
                
        // Show results of operation on the console 
        console.log(q); 
};

module.exports = {
    tripsList,
    tripsFindByCode,
    tripsAddTrip,
    tripsUpdateTrip
};
