(function() {
  ctx = $("#ctx-json").data('ctx');
  var host = window.location.host;  
  var talkboard = CodeMirror.fromTextArea(document.getElementById("text"), {
      autofocus: true,
      lineWrapping: true,
    }
  );
  var WebSocket = window.WebSocket || window.MozWebSocket;
  if (WebSocket) {
      try {
          var socket = new WebSocket('ws://'+ host + '/new-msg/socket');
      } catch (e) {

      }
  }

  var delay = (function(){
    var timer = 0;
    return function(callback, ms){
      clearTimeout (timer);
      timer = setTimeout(callback, ms);
    };
  })();

  if (socket) {
      socket.onmessage = function(event) {
          talkboard.setValue(event.data);
          talkboard.setCursor(talkboard.lineCount(), 0)
      }
      talkboard.on('keyup',function(cMirror){
        delay(function(){
          socket.send(cMirror.getValue());
        }, 1000 ); 
      })
  }
})();