$(function () {
    var country_select = $(".select_country");
    var other_country = $(".other_country");
    var ms = $(".MS");

    $('form').on("submit", function(e) {
        if (country_select.val() == '') {
            ms.val(other_country.val());
        } else {
            ms.val(country_select.val());
        }
        $(this).submit();
    });

    country_select.on("change", function() {
        alert($(this).val());
        if($(this).val() == '') {
            other_country.show();
        } else {
            other_country.hide();
        }
    });

});

