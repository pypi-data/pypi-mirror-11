var modal = (function() {
  function init(trigger_id, overlay_id) {
    var trigger = document.getElementById(trigger_id);
    trigger.onclick = (function(e) {
      return function() { 
          modal.overlay(overlay_id);
      }
    })();
  }

  function overlay(overlay_id) {
    el = document.getElementById(overlay_id);
    el.style.visibility = (el.style.visibility == 'visible') ? 'hidden' : 'visible';
  }

  function closer(closer_id, overlay_id) {
    var closer = document.getElementById(closer_id);
    closer.onclick = (function(e) {
      return function() {
        modal.overlay(overlay_id);
      }
    })();
  }

  return {
    init: init,
    overlay: overlay,
    closer: closer
  }
})();