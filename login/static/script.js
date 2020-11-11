$(document).ready(function (){

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    let update_days = function (days){
        for (let day in days){
            $('.' + day + ' > p:nth-child(2)').text(days[day]);
        }
    }

    $('#date-counter').submit(function(e){
        e.preventDefault();

        let data = {
            'start_date': $('#start_date').val(),
            'end_date': $('#end_date').val(),
        }

        $.ajax({
            url: window.location.href,              
            type: "POST",          
            data: data,
            dataType: 'json', 
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data, textStatus, xhr){
                update_days(data);
            },
            error: function(data, textStatus, xhr){
                alert(data['responseJSON'].date_error);
            }
        });
    });

});