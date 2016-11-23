var $messages = $('.messages-content'),
    create_event,
    d, h, m,
    clicks = 0,
    i = 0;

$("body").click(function(){
    if (clicks === 0) {
        $(".popup").fadeToggle();
        clicks = 1;
        $messages.mCustomScrollbar();
        setTimeout(function() {
          welcomeMessage();
        }, 100);
    }
})

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $.get('/getMessage', {message:msg})
    .then(function (result){
        $('<div class="message user-message">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        $('.message-input').val(null);
        updateScrollbar();
        reply(result);
    }).catch(function(err){
        console.log('get request to server failed: ' + err);
    })
}

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

function welcomeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new">' + "Hey, how can I help you?" + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
}, 1000);
}

function reply(result = "{intent:'Unknown',reply:'Sorry, my service is currently unavailable.'}") {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    result = result.replace(/u'/g, '"');
    result = result.replace(/'/g, '"');
    try{
        result = $.parseJSON(result);
        response = result.reply;
    }
    catch(err){
        console.log(err);
        response = "Sorry, can you repeat that?";
    }
    $('<div class="message new">' + response + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    if (result.intent == 'create_event') {
        $('#calendar').attr('src', $('#calendar').attr('src'));
    }
    i++;
  }, 500 + (Math.random() * 20) * 100);
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

$('.speech').click(function() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {

      var recognition = new webkitSpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.lang = "en-US";
      recognition.start();

      recognition.onresult = function(e) {
        $('.message-input')[0].value = e.results[0][0].transcript;
        console.log(e.results[0][0].transcript);
        recognition.stop();
        insertMessage();
      };

      recognition.onerror = function(e) {
        recognition.stop();
      }

    }
});
