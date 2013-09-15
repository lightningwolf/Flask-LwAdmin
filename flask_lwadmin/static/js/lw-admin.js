$(document).ready(function(){
	
	$('.j-datepicker').datepicker({
		dateFormat: 'yy-mm-dd'
	});
	
	$('.j-datetimepicker').datetimepicker({
		dateFormat: 'yy-mm-dd',
		timeFormat: 'hh:mm:ss',
		showSecond: true
	});
});