$(function () {

    if($('#filterform').length == 1) {

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));

        var species = $('#species');
        species.remoteChained('#period, #group', species.data('href'));

        var region = $('#region');
        region.remoteChained('#period, #group, #species', region.data('href'));

        if(species.find('option:selected').val() == '') {
            region.prop('disabled', true);
        }

    }

});
