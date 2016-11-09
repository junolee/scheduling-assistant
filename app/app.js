var bodyParser = require("body-parser"),
sass           = require('node-sass'),
express        = require("express"),
app            = express();

sass.render({
  file: scss_filename,
  [, options..]
}, function(err, result) { /*...*/ });

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended: true}));

var messages = [
    {sender: "bot", text: "Hello there"},
    {sender: "user", text: "Can you schedule a meeting for 9am tomorrow?"},
    {sender: "bot", text: "Sure, I'll add that to the calendar."},
    {sender: "user", text: "Thanks!"},
    {sender: "bot", text: "No problem."}
]

app.get("/", function(req, res){
   res.redirect("/chatbot");
});

app.get("/chatbot", function(req, res){
   res.render("chatbot", {messages:messages});
});

app.listen(3000, function(){
    console.log("SERVER IS RUNNING!");
})
