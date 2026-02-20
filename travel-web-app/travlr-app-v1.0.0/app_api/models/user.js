/* user model (schema) */
const mongoose = require('mongoose');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// User Schema: email, name, hash, salt
const userSchema = new mongoose.Schema({
    email: {
        type: String,
        unique: true,
        required: true    
    },
    name: {
        type: String,
        required: true
    },
    hash: String,
    salt: String
});

// Generates and stores salt and hash (hashed password) in user record
userSchema.methods.setPassword = function(password){ 
    // Generates a cryptographically random 16-byte salt
    this.salt = crypto.randomBytes(16).toString('hex');
    this.hash = crypto.pbkdf2Sync(
        password,   
        this.salt,  
        1000,       // iterations
        64,         // key length
        'sha512'    // digest algorithm
    ).toString('hex'); 
};

// Compares entered password against stored hash 
userSchema.methods.validPassword = function(password) { 
    // Generates hash to compare to stored hash
    var hash = crypto.pbkdf2Sync(
        password, 
        this.salt,
        1000, 
        64, 
        'sha512'
    ).toString('hex'); 
    return this.hash === hash; 
};

// Generate a JSON Web Token (JWT) for the current record 
userSchema.methods.generateJWT = function() { 
    return jwt.sign( 
    { // Payload (JSON object) containing user authentication data
        _id: this._id, 
        email: this.email, 
        name: this.name, 
    }, // SECRET stored in .env file  
    process.env.JWT_SECRET, 
    // Token expires an hour from creation 
    { expiresIn: '1h' });   
};

// model name 'users' binds to userSchema schema
const User = mongoose.model('users', userSchema);
module.exports = User;
