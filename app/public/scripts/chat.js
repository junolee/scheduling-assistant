var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).on('load', function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    welcomeMessage();
  }, 100);
});

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

$('.message-submit').click(function() {
  insertMessage();
});

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
    $('<div class="message new">' + 'Hello there' + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
}, 1000);
}

function reply(msg = 'Sorry, my service is currently unavailable.') {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();

    $('<div class="message new">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');

    setDate();
    updateScrollbar();
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
