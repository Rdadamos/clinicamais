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

  $("#searchInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tableSearch tr:not(:first)").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

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

  $(".addMedicine:not(:first)").appendTo(".holdInputsMedicineForm");
  $(".addMedicine td:eq(4), .addMedicine td:eq(5)").addClass("d-none")
  $(".addMedicineBtn").bind("click", (function () {
    $(this).addClass('d-none');
    $(".holdInputsMedicineForm").find(".addMedicine:first").appendTo('.medicineTb tbody').find("td:eq(4), td:eq(5)").addClass("d-none");
    var total = +$("#totalMedicines").val() + 1;
    $("#totalMedicines").val(total);
  }));

  $(".addExam:not(:first)").appendTo(".holdInputsExamForm");
  $(".addExam td:eq(2), .addExam td:eq(3)").addClass("d-none")
  $(".addExamBtn").bind("click", (function () {
    $(this).addClass('d-none');
    $(".holdInputsExamForm").find(".addExam:first").appendTo('.examTb tbody').find("td:eq(2), td:eq(3)").addClass("d-none");
    var total = +$("#totalExam").val() + 1;
    $("#totalExam").val(total);
  }));
});
