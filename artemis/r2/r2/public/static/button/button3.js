(function() {
  var write_string="<iframe src=\"//www.branchestatic.com/button/button3.html?url=";

  if (window.artemis_url)  { 
      write_string += encodeURIComponent(artemis_url); 
  }
  else { 
      write_string += encodeURIComponent(window.location.href);
  }
  if (window.artemis_title) {
       write_string += '&title=' + encodeURIComponent(window.artemis_title);
  }
  if (window.artemis_target) {
       write_string += '&sr=' + encodeURIComponent(window.artemis_target);
  }
  if (window.artemis_css) {
      write_string += '&css=' + encodeURIComponent(window.artemis_css);
  }
  if (window.artemis_bgcolor) {
      write_string += '&bgcolor=' + encodeURIComponent(window.artemis_bgcolor); 
  }
  if (window.artemis_bordercolor) {
      write_string += '&bordercolor=' + encodeURIComponent(window.artemis_bordercolor); 
  }
  if (window.artemis_newwindow) { 
      write_string += '&newwindow=' + encodeURIComponent(window.artemis_newwindow);}
  write_string += "\" height=\"52\" width=\"69\" scrolling='no' frameborder='0'></iframe>";
  document.write(write_string);
})()
