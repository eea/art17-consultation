$(function () {

    if($('#filterform').length == 1) {

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));

        var subject = $('#subject');
        subject.remoteChained('#period, #group', subject.data('href'));

        var region = $('#region');
        region.remoteChained('#period, #group, #subject', region.data('href'));

        if(subject.find('option:selected').val() == '') {
            region.prop('disabled', true);
        }

    }

});
