$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });
  $('[data-toggle="tooltip"]').tooltip();
  $("#hide_btn").click(function(){
	  $(".form-horizontal").toggle(250);
  });
  $("#hide_log_btn").click(function(){
	  $("#log_files").toggle(250);
  });
});

function deleteEntry() {
	str = $('#pipeline_table').bootstrapTable('getSelections')[0]["1"];
	str = str.substring(0, str.length - 1);
	console.log(str)
	var elm = document.getElementById("dupa")
	console.log($(elm).attr("href") + str)
	return str
}
