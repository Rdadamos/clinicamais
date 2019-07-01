$(document).ready(function() {
  $(".deleteBtn").bind("click", (function () {
    $(".deleteForm").attr('action', $(this).attr("data-url"));
  }));

  $(".shiftField").each(function() {
    shift = $(this);
    if (shift.text() == "I") {
      shift.text("Integral");
    } else if (shift.text() == "M") {
      shift.text("Manhã");
    } else {
      shift.text("Tarde");
    }
  });
  $(".genderField").each(function() {
    gender = $(this);
    if (gender.text() == "H") {
      gender.text("Homem");
    } else if (gender.text() == "M") {
      gender.text("Mulher");
    } else {
      gender.text("Outro");
    }
  });
  $("#id_phone").mask('(00) 00000-0000');
});
