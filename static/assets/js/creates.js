 function save_order(){
        let img = $('#img').val()
        let title = $('#title').val()
        let singer = $('#singer').val()
        let comment = $('#comment').val()
        let genre = $('#id_select option:selected').val()
        let today = new Date().toISOString()

        $.ajax({
            type: 'POST',
            url: '/api/posts',
            data: {img_give: img, title_give: title, singer_give: singer, comment_give: comment, genre_give: genre, date_give: today},
            success: function (response) {
                alert(response['msg'])
                window.location.href = `/`
            }
        });
    }