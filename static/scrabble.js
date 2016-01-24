$(function () {
    var form = $('form');

    var get_link = function (word) {
        return '<a class="word-def" href="https://ru.wiktionary.org/wiki/' +
               word + '#.D0.97.D0.BD.D0.B0.D1.87.D0.B5.D0.BD.D0.B8.D0.B5"' +
               ' target="_blank">?</a>';
    };
    
    var word_tmpl = function (word, cost) {
        return '<tr>'+
               '<td class="word">' + word + '</td>' + 
               '<td>' + cost + '</td>' + 
               '<td>' + get_link(word) + '</td>' + 
               '</tr>';
    };

    var letters,
        b_letters;

    form.submit(function (e) {
        e.preventDefault();
        letters = $('#my-letters').val();
        b_letters = $('#board-letters').val();
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                var words = $('#words');
                words.empty();
                $.each(data, function (idx, word_cost) {
                    words.append(word_tmpl(word_cost[0], word_cost[1]));
                });
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
