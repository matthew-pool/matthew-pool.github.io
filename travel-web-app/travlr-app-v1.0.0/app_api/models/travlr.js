// Trips schema module
const mongoose = require('mongoose');

// Define trip schema
const tripSchema = new mongoose.Schema({
    // 'code' and 'name' data indexed for faster retrieval
    code: { type: String, required: true, index: true },
    name: { type: String, required: true, index: true },
    length: { type: String, required: true },
    // 'start' date in ISO standard date format
    start: { type: Date, required: true },
    resort: { type: String, required: true },
    perPerson: { type: String, required: true },
    image: { type: String, required: true },
    description: { type: String, required: true }
});

// collection named 'trips' and uses tripsSchema
const Trip = mongoose.model('trips', tripSchema);
module.exports = Trip;