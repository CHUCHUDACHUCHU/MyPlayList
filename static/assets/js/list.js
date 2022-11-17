



function get_posts() {
    $.ajax({
        type: "GET",
        url: "/api/posts",
        data: {},
        success: function (response) {
            console.log(response);
            let posts = response["posts"]
            for (let i = 0; i < posts.length; i++) {
                let post = posts[i]
                let img = post['img']
                let title = post['title']
                let singer = post['singer']
                let comment = post['comment']
                let genre = post['genre']
                let index = post['index']
                let time_post = new Date(post['date'])
                let time_before = time2str(time_post)

                let temp_html = `<div id="" style="cursor:pointer" class="card" onclick="window.location.href = \`/detail/?card=${index}\`">

                                    <div class="card-image">
                                        <figure class="image is-square">
                                            <img src="${img}" alt="Placeholder image">
                                        </figure>
                                    </div>
                                    <div class="card-content">
                                        <div class="media">
                                            <div class="media-content">
                                                <p class="title is-5">${title} - ${singer}</p>
                                                <h6 class="subtitle is-6">${genre}</h6>
                                            </div>
                                        </div>
                                        <div class="content">
                                            <p>${comment}</p><small>${time_before}</small>
                                        </div>
                                    </div>
                                </div>`;
                $('#cards-box').append(temp_html);
            }
        }
    })
}
function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}