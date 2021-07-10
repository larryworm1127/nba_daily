$(function () {
  $("#datepicker").datepicker({
    dateFormat: 'm-dd-yy',
    constrainInput: false,
    onSelect: function () {
      $('#dateform').submit();
    }
  });
});