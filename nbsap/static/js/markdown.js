$(function() {
    $('.markdown_less').on("click", function() {
        $('.markdown_all').show();
        $(this).hide();
    });

    $('.markdown_button').on("click", function() {
        $('.markdown_less').show();
        $('.markdown_all').hide();
    });
});
