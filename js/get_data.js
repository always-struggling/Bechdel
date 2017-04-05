    
    // AJAX call to api
    function get_data(graph, arr) {
        var new_data;
        var api_url = 'http://localhost:8000/bechdel_' + graph;
        $.ajax({
            url: api_url,
            type: 'POST',
            data: JSON.stringify(arr),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
            beforeSend: function() {
               // $('#loading_gif').show()
               console.log('getting data')
            },
            complete: function() {
               // $('#loading_gif').show()
               console.log('got data')
            },
            success: function(json) {
                new_data = jQuery.parseJSON(json);
                //console.log(new_data);

        }
        });
        return new_data;
        
    };  