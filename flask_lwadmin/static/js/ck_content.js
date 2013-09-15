CKEDITOR.editorConfig = function( config )
{
    config.language = 'pl';
    config.uiColor = '#C2CEEA';
    config.entities_greek = false;
    config.entities_latin = false;
    config.toolbar =
    [
        ['Source','-','Preview','-',],
        ['Cut','Copy','Paste','PasteText','PasteFromWord'],
        ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
        ['Image','Flash','Table','HorizontalRule','SpecialChar','PageBreak'],
        ['Link','Unlink','Anchor'],
        ['TextColor','BGColor','-','Maximize','-','About'],
        '/',
        ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
        ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
        ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
        ['Styles','Format','Font','FontSize','-','SpellChecker', 'Scayt']
    ];
    config.allowedContent = true;
};
