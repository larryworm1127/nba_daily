function getAOColumnsDesc(numColumns) {
  let list = []
  for (let i = 0; i < numColumns; i++) {
    list.push({"orderSequence": ["desc", "asc"]})
  }
  return list;
}


$(document).ready(function () {
  $('.boxscores-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".boxscores-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": [null].concat(getAOColumnsDesc(21))
  });
});

$(document).ready(function () {
  $('.player-games-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".player-games-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": getAOColumnsDesc(20)
  });
});

$(document).ready(function () {
  $('.seasons-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".seasons-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": getAOColumnsDesc(20)
  });
});

$(document).ready(function () {
  $('.team-games-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".team-games-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": getAOColumnsDesc(19)
  });
});

$(document).ready(function () {
  $('.roster-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".roster-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": getAOColumnsDesc(9)
  });
});

$(document).ready(function () {
  $('.standings-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".standings-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": [
      {"orderSequence": ["desc", "asc"]},
      {"bSortable": false},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]},
      {"orderSequence": ["desc", "asc"]}
    ]
  });
});

$(document).ready(function () {
  $('.team-player-stats-datatable').DataTable({
    "drawCallback": function (settings) {
      $(".team-player-stats-datatable").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    pageLength: 50,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "order": [[24, "desc"]],
    "columnDefs": [
      {type: "natural", targets: 7}
    ],
    "aoColumns": getAOColumnsDesc(28)
  });
});

$(document).ready(function () {
  $('.player-list-table').DataTable({
    "drawCallback": function (settings) {
      $(".player-list-table").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    pageLength: 50,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": getAOColumnsDesc(20)
  });
});

$(document).ready(function () {
  $('.team-list-table').DataTable({
    "drawCallback": function (settings) {
      $(".player-list-table").wrap("<div class='table-responsive'></div>");
    },

    paging: false,
    "bFilter": false,
    "bInfo": false,
    /* Disable initial sort */
    "aaSorting": [],
    "aoColumns": getAOColumnsDesc(26)
  });
});
