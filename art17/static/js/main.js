$(function () {

    if($('#filterform').length == 1) {

        var group = $('#group');
        $.getJSON(group.data('href')).done(function (data) {
            $.each(data, function (k, v) {
                var option = $('<option>').val(k).text(v);
                group.append(option);
            });
        });

        var species = $('#species');
        species.remoteChained('#group', species.data('href'));

        var region = $('#region');
        region.remoteChained('#species', region.data('href'));

    }

});
