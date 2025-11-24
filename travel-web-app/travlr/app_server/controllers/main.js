/* GET home page */
// index arrow function (expression)
const index = (req, res) => {
    // Render index view and pass title parameter
    res.render('index', {title: "Travlr Getaways"});
};

// Export index function to make it available to other parts of the app
module.exports = {
    index
}
