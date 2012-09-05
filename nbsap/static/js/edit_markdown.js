$(function() {
 var converter = Markdown.getSanitizingConverter();

 var en_editor = new Markdown.Editor(converter, '-en');
 var fr_editor = new Markdown.Editor(converter, '-fr');
 var nl_editor = new Markdown.Editor(converter, '-nl');

 en_editor.run();
 fr_editor.run();
 nl_editor.run();
});
