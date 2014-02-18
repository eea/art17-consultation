$(function () {

    var country_select = $("#country_options");
    var other_country = $("#other_country");
    var other_country_container = $("#other_country_container");
    var ms = $("#MS");

    var predefined = country_select.find("option")
        .map(function(idx, elm) {
            return elm.value
        }
    ).toArray();

    if (predefined.indexOf(ms.val()) !== -1) {
       country_select.val(ms.val());
    }
    else {
        country_select.val('');
        other_country.val(ms.val());
    }

    other_country.on("blur", function () {
        ms.val(other_country.val());
    })

    country_select.on("change", function() {
        if($(this).val() == '') {
            other_country_container.show();
            ms.val(other_country.val());
        } else {
            other_country_container.hide();
            ms.val(country_select.val());
        }
    }).change();
});

