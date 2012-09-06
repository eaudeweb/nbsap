$(function() {
    $("#language").on("change", function() {
        var lang = $(this).val();
        $('.original-hideout').show();
        if (lang == 'en') {
            $('.original-hideout').hide();
        }
        $(".language-container").hide();
        $(".language-" + lang).show();
    }).change();
});
