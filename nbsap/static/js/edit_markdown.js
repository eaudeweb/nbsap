$(function() {
  app.converter = Markdown.getSanitizingConverter();

  app.en_editor = new Markdown.Editor(app.converter, '-en');
  app.en_editor.run();
  $('#wmd-preview-en').hide();
  $('#wmd-quote-button-en').remove();
  $('#wmd-code-button-en').remove();
  $('#wmd-image-button-en').remove();
  $('#wmd-hr-button-en').remove();

  if($('#wmd-input-fr').length) {
    app.fr_editor = new Markdown.Editor(app.converter, '-fr');
    app.fr_editor.run();
    $('#wmd-preview-fr').hide();
    $('#wmd-quote-button-fr').remove();
    $('#wmd-code-button-fr').remove();
    $('#wmd-image-button-fr').remove();
    $('#wmd-hr-button-fr').remove();
  }

  if($('#wmd-input-nl').length) {
    app.nl_editor = new Markdown.Editor(app.converter, '-nl');
    app.nl_editor.run();
    $('#wmd-preview-nl').hide();
    $('#wmd-quote-button-nl').remove();
    $('#wmd-code-button-nl').remove();
    $('#wmd-image-button-nl').remove();
    $('#wmd-hr-button-nl').remove();
  }

  $('.preview').appendTo("#wmd-button-row-en, #wmd-button-row-fr, #wmd-button-row-nl");
  $('.help').appendTo("#wmd-button-row-en, #wmd-button-row-fr, #wmd-button-row-nl");

  $('.preview').on('click', function () {
    var language = $('#language').val();
    var text = $('#wmd-preview-' + language).html();
    $('#preview').find('.modal-body').html(text);
    return true;
  });

});
