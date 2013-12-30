$(document).ready(function () {

	$('.j-datepicker').datepicker({
		dateFormat: 'yy-mm-dd'
	});

	$('.j-datetimepicker').datetimepicker({
		dateFormat: 'yy-mm-dd',
		timeFormat: 'hh:mm:ss',
		showSecond: true
	});

	$('.table-active td').click(function () {
		if ($(this).index() > 0) {
			var checkbox = $(this).parents('tr').find('input[type=checkbox]');
			if (checkbox.is(':checked')) {
				checkbox.removeAttr('checked');
			} else {
				checkbox.attr('checked', true);
			}
		}
	});
});