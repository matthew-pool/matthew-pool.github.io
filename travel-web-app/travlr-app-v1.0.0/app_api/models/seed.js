// NOTE: seeding the collection removes any existing records
// EXECUTE SCRIPT: <project_root> node .\app_server\models\seed
// VERIFY LOADED DATA: MongoDB Compass (or DBeaver): 'Connect' > travlr > trips

// Bring in the DB connection and the Trip schema
const Mongoose = require('./db');
const Trip = require('./travlr');

// Read seed data from JSON file
var fs = require('fs');
var trips = JSON.parse(fs.readFileSync('./data/trips.json', 'utf8'));

// Delete any existing records and insert seed data
const seedDB = async () => {
    await Trip.deleteMany({});
    await Trip.insertMany(trips);
};

// Close the MongoDB connection and then exit
seedDB().then(async () => {
    await Mongoose.connection.close();
    process.exit(0);
});
