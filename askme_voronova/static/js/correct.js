$(".correct").on('click', function (ev) {
    var $this = $(this)
    $.ajax({
        method: "POST",
        url: "/correct/",
        data: {'id': $this.data('id'),
        },
        headers: {'X-CSRFToken': csrftoken}
    })
        .done(function ({'correct': correct}) {
            document.getElementById('correct' + $this.data('id')).checked = correct;
        });
})