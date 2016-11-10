var bodyParser = require("body-parser"),
express        = require("express"),
axios          = require('axios'),
app            = express();

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended: true}));

var reply = "Sure, I'll do that!";

app.get("/", function(req, res){
   res.redirect("/chatbot");
});

app.get("/chatbot", function(req, res){
   res.render("chatbot");
});

app.get("/getMessage", function(req, res){
    axios.get('http://localhost:8080?message=' + req.query.message)
      .then(function (response) {
        res.send(response.data);
      })
      .catch(function (error) {
        console.log("get request to python server didn't work: " + error);
      });
})

app.listen(3000, function(){
    console.log("Node.js HTTP server started on port 3000!");
})
