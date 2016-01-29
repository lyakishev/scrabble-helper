$(function () {
    Handlebars.registerHelper('wordRepr', function (word, onboard) {
        word = word.replace(new RegExp(onboard, 'g'),
            '<strong>' + onboard + '</strong>')
        return new Handlebars.SafeString(word);
    });

    var template = Handlebars.compile($("#word-template").html()),
        form = $('form'),
        //b_letters,
        letters;

    form.submit(function (e) {
        e.preventDefault();
        var words = $('#words');
        words.empty();
        letters = $('#letters').val();
        //b_letters = $('#board-strings').val();
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                words.append(template(data));
            },
            dataType: 'json'
        });
    });
    $('#words').on('click', '.word', function (e) {
        var $word = $(this),
            word = $.trim($word.text()).replace($word.attr('onboard'), '', 1),
            new_letters = letters;
        $.each(word.split(''), function (idx, c) {
            if (new_letters.indexOf(c) === -1) {
                c = '.';
            }
            new_letters = new_letters.replace(c, '', 1)
        })
        $('#letters').val(new_letters);
    });
});
