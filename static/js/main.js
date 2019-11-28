$(document).ready(function() {
  $('.mainBox').css("paddingTop", $('.mainBox > .position-fixed').height());
  $( window ).resize(function() {
    $('.mainBox').css("paddingTop", $('.mainBox > .position-fixed').height());
  });

  $(".deleteBtn").bind("click", (function () {
    $(".deleteForm").attr('action', $(this).attr("data-url"));
    $("#deleteModal .modal-title").text($(this).text());
  }));
  $(".btnNewAppointment").bind("click", (function () {
    $(this).addClass("d-none").next().removeClass("d-none");

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
  $("#id_birthdate").mask('00/00/0000');

  $("#btnSelectDoctor").click(function() {
    var url = document.location.href + $("#selectDoctor").children("option:selected").val();
    document.location = url;
  });

  sunday_index = $(".tableAppointment th:contains('Domingo')").index();
  $(".tableAppointment tr").each(function() {
    $(this).children().eq(sunday_index).remove();
  });
});
