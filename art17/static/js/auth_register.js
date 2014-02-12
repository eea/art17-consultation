$(function () {

    var country_select = $("#country_options");
    var other_country = $("#other_country");
    var other_country_container = $("#other_country_container");
    var ms = $("#MS");

    other_country.on("blur", function () {
        ms.val(other_country.val());
    })

    country_select.on("change", function() {
        if($(this).val() == '') {
            other_country_container.show();
        } else {
            other_country_container.hide();
            ms.val(country_select.val());
        }
    }).change();

});

