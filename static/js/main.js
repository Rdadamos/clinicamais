$(document).ready(function() {
  $(".deleteBtn").bind("click", (function () {
    $(".deleteForm").attr('action', $(this).attr("data-url"));
  }));
});
