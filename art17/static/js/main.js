$(function () {

    if($('#filterform').length == 1) {

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));

        var subject = $('#subject');
        subject.remoteChained('#period, #group', subject.data('href'));

        var region = $('#region');
        region.remoteChained('#period, #group, #subject', region.data('href'));

        if(group.find('option:selected').val() == '') {
            subject.prop('disabled', true);
        }

        if(subject.find('option:selected').val() == '') {
            region.prop('disabled', true);
        }

    }

    if($('#report-filterform').length == 1) {

        var region = $('#region');
        region.remoteChained('#period, #country', region.data('href'));

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));
    }

    if($('#progress-filterform').length == 1) {

        var group = $('#group');
        var conclusion = $('#conclusion');

        group.remoteChained('#period', group.data('href'));
    }
});

$(function() {
    $('body').on('click', '.comments-btn', function(evt) {
      evt.preventDefault();
      var link = $(this);
      var url = link.attr('href');
      var title = "Comments";
      var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
      var popup = window.open(url, title, params);
      popup.focus();
    });

    $('.close-popup').on('click', function (evt) {
      evt.preventDefault();
      window.close();
    });

    $('body').on('click', '.delete-btn', function (evt) {
        evt.preventDefault();
        var url = $(this).attr('href');
        var request = $.ajax({
            type: "GET",
            url: url,
            dataType: "script"
        }).done(function (msg) { location.reload(); });
    });

    $('body').on('click', '.popup', function(evt) {
      evt.preventDefault();
      var link = $(this);
      var url = link.attr('href');
      var title = link.data('title');
      var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
      var popup = window.open(url, title, params);
      popup.focus();
    });

})();

