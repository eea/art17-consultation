$(function () {

    if($('#filterform').length == 1) {

        var species = $('#species');
        species.remoteChained('#group', species.data('href'));

        var region = $('#region');
        region.remoteChained('#species', region.data('href'));

        if(species.find('option:selected').val() == '') {
            region.prop('disabled', true);
        }
    }

});
