var popover = (function() {
  function pop(id, hover, popover_id) {
    hover = JSON.parse(hover.toLowerCase());
    var on = false;
    var container = document.getElementById(id);
    if (hover) {
      container.onclick = togglePopover;
      container.addEventListener('mouseover', togglePopoverOn);
      container.addEventListener('mouseout', togglePopoverOff);
    } else {
      container.onclick = togglePopover;
    }

    var width = container.clientWidth;
    var popover = document.getElementById(popover_id);
    popover.style.left = width + 'px';
    container.appendChild(popover);

    function togglePopover() {
      if (on) {
        togglePopoverOff();
      } else {
        togglePopoverOn();
      }
    };

    function togglePopoverOn() {
      var popover = document.getElementById(popover_id);
      popover.setAttribute('class', 'pop');
      on = true;
    };

    function togglePopoverOff() {
      var popover = document.getElementById(popover_id);
      popover.setAttribute('class', 'popnomore');
      on = false;
    };
  };
  return {
    pop: pop
  };
})();