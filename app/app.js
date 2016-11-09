var bodyParser = require("body-parser"),
express        = require("express"),
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
    console.log(req.query);
    // send message to python server
    // when u get a response, send back to client
    res.send(reply);
})

app.listen(3000, function(){
    console.log("SERVER IS RUNNING!");
})
