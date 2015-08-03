var base_url = "http://127.0.0.1:5000"

$('#city').typeahead({
    ajax: {
            url: base_url + "/find"
          }
});


$('#checkin_date').datepicker({
    format: "dd/mm/yyyy",
    language: "pt-BR"
});

$('#checkout_date').datepicker({
    format: "dd/mm/yyyy",
    language: "pt-BR"
});

$('#no_date_range').click(function(obj){

    if(this.checked){

        $('#checkin_date').attr('disabled', true);
        $('#checkout_date').attr('disabled', true);

    }else{

        $('#checkin_date').attr('disabled', false);
        $('#checkout_date').attr('disabled', false);

    }

});

$('#search').click(function(){

    var query_string = ""

    if( $('#no_date_range')[0].checked ){
        query_string = "?city=" + $('#city').val() + "&no_date_range=" + $('#no_date_range').val()
    }else{

        var checkin_date = $('#checkin_date').val()
        var checkout_date = $('#checkout_date').val()

        query_string = "?city=" + $('#city').val() + "&checkin_date=" + checkin_date + "&checkout_date=" + checkout_date
    }

    $('#table_results > tbody').html("");
    $('#table_results').addClass("hide");

    $.get( base_url + "/availabilities" + query_string, function( data ) {

        if ( data.length > 0 ){

            $('.message').addClass("hide");
            $('#table_results').removeClass("hide");
            $('#table_results > tbody').html("");

            $.each(data, function( i, value ){
                $('#table_results > tbody:last-child').append("<tr><td>"+value.city+"</td><td>"+value.hotel+"</td></tr>");
            });

        }else{

            $('.message').removeClass("hide");

        }

    });

});