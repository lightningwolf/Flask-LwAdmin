$(document).ready(function () {

	$('.j-datepicker').datepicker({
		dateFormat: 'yy-mm-dd'
	});

	$('.j-datetimepicker').datetimepicker({
		dateFormat: 'yy-mm-dd',
		timeFormat: 'hh:mm:ss',
		showSecond: true
	});

	$('.table-active td').live('click', function () {
		if (jQuery(this).index() > 0) {
			var checkbox = jQuery(this).parents('tr').find('input[type=checkbox]');
			if (checkbox.is(':checked')) {
				checkbox.attr('checked', false);
			} else {
				checkbox.attr('checked', true);
			}
		}
	});
});