$(function() {
  app.converter = Markdown.getSanitizingConverter();

  app.en_editor = new Markdown.Editor(app.converter, '-en');
  app.fr_editor = new Markdown.Editor(app.converter, '-fr');
  app.nl_editor = new Markdown.Editor(app.converter, '-nl');

  app.en_editor.run();
  app.fr_editor.run();
  app.nl_editor.run();

  $('#wmd-preview-en').hide();
  $('#wmd-preview-fr').hide();
  $('#wmd-preview-nl').hide();

  $('#wmd-quote-button-en').remove();
  $('#wmd-quote-button-fr').remove();
  $('#wmd-quote-button-nl').remove();

  $('#wmd-code-button-en').remove();
  $('#wmd-code-button-fr').remove();
  $('#wmd-code-button-nl').remove();

  $('#wmd-image-button-en').remove();
  $('#wmd-image-button-fr').remove();
  $('#wmd-image-button-nl').remove();

  $('#wmd-hr-button-en').remove();
  $('#wmd-hr-button-fr').remove();
  $('#wmd-hr-button-nl').remove();

  $('.preview').appendTo("#wmd-button-row-en, #wmd-button-row-fr, #wmd-button-row-nl");

  $('.preview').on('click', function () {
    var language = $('#language').val();
    var text = $('#wmd-preview-' + language).html();
    $('.modal-body').find('p').html(text);
    return true;
  });
});
