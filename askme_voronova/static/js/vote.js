$(".vote").on('click', function (ev) {
    var $this = $(this)
    $.ajax({
        method: "POST",
        url: "/vote/",
        data: {'id': $this.data('id'),
            'action': $this.data('action'),
            'model': $this.data('model'),
        },
        headers: {'X-CSRFToken': csrftoken}
    })
        .done(function ({'rating': rating}) {
            if (rating !== undefined) {
                document.getElementById($this.data('model') + $this.data('id')).innerHTML = rating;
                if ($this.data('action') === 1) {
                    if ($this.data('model') === "answer") {
                        if (window.getComputedStyle(document.getElementById("vote-up-a" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                            document.getElementById("vote-up-a" + $this.data('id')).style.color = "black"
                        } else {
                            if (window.getComputedStyle(document.getElementById("vote-down-a" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                                document.getElementById("vote-down-a" + $this.data('id')).style.color = "black"
                            }
                            document.getElementById("vote-up-a" + $this.data('id')).style.color = "#0a53be"
                        }
                    } else {
                        if (window.getComputedStyle(document.getElementById("vote-up-q" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                            document.getElementById("vote-up-q" + $this.data('id')).style.color = "black"
                        } else {
                            if (window.getComputedStyle(document.getElementById("vote-down-q" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                                document.getElementById("vote-down-q" + $this.data('id')).style.color = "black"
                            }
                            document.getElementById("vote-up-q" + $this.data('id')).style.color = "#0a53be"
                        }
                    }
                } else {
                    if ($this.data('model') === "answer") {
                        if (window.getComputedStyle(document.getElementById("vote-down-a" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                            document.getElementById("vote-down-a" + $this.data('id')).style.color = "black"
                        } else {
                            if (window.getComputedStyle(document.getElementById("vote-up-a" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                                document.getElementById("vote-up-a" + $this.data('id')).style.color = "black"
                            }
                            document.getElementById("vote-down-a" + $this.data('id')).style.color = "#0a53be"
                        }
                    } else {
                        if (window.getComputedStyle(document.getElementById("vote-down-q" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                            document.getElementById("vote-down-q" + $this.data('id')).style.color = "black"
                        } else {
                            if (window.getComputedStyle(document.getElementById("vote-up-q" + $this.data('id'))).color === "rgb(10, 83, 190)") {
                                document.getElementById("vote-up-q" + $this.data('id')).style.color = "black"
                            }
                            document.getElementById("vote-down-q" + $this.data('id')).style.color = "#0a53be"
                        }
                    }
                }
            }

            if (rating < 0) {
                document.getElementById($this.data('model') + $this.data('id')).style.color = "red"
            } else if (rating > 0) {
                document.getElementById($this.data('model') + $this.data('id')).style.color = "green"
            } else {
                document.getElementById($this.data('model') + $this.data('id')).style.color = "black"
            }
        });
})