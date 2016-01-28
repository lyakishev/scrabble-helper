$(function () {
    Handlebars.registerHelper('wordSpan', function (word, span) {
        var parts = [];
        for (var i=0; i<word.length; i++) {
            if (i == span[0]) {
                parts.push('<strong>')
            } else if (i == span[1]) {
                parts.push('</strong>')
            }
            parts.push(word[i])
        }
        return new Handlebars.SafeString(parts.join(''));
    });

    var template = Handlebars.compile($("#word-template").html()),
        form = $('form'),
        letters,
        b_letters;

    form.submit(function (e) {
        e.preventDefault();
        var words = $('#words');
        words.empty();
        letters = $('#my-letters').val();
        b_letters = $('#board-letters').val();
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
        var word = $(this).text().replace(b_letters, '', 1);
        var new_letters = letters;
        $.each(word.split(''), function (idx, c) {
            if (new_letters.indexOf(c) === -1) {
                c = '.';
            }
            new_letters = new_letters.replace(c, '', 1)
        })
        $('#my-letters').val(new_letters);
    });
});
