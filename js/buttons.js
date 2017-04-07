
    // Creates our title
    function make_title(P_title) {
            
        // Define element
        var r = $('<a class="title info">'+P_title+'</a>');
        // Append element
        $(  ".main_title" ).append( r ).hide();            
        
    };
    

    //  Creates our Graph Buttons
    function make_graph_button (P_graph, P_x_fields, P_y_fields) {
        
        // Define new element
        var r = $(' <button class="graph_button" axis="i" id="'+P_graph+'">'+P_graph+'</button>');
        // Bind click event to element
        r.on('click', function () {
            
         
            // Set buttons as clicked
            $('.graph_button').removeClass('clicked');
            $(this).addClass('clicked');

            
            // Disable all buttons
            $('button').prop('disabled', true);
            setTimeout(function() {
                $('button').prop('disabled', false);
                $('#'+P_graph).prop('disabled', true);
            },   3000);

            
            // Switch field buttons
            remove_object('axis_buttons', function() {
                make_field_buttons(P_y_fields, 'Y');
                make_field_buttons(P_x_fields, 'X');
                show_object('.axis_buttons');
            });
        });
        
        // Append new element
        $(  ".graph_buttons" ).append( r ).hide();


    };



    // Creates the field buttons for an axis
    function make_field_buttons (P_fields, P_axis) {
        // Define new element - div container for buttons
        var r = $('<div class="axis_buttons">');

        // Bind click event to new element
        $("."+P_axis).append( r )
        
        // Loop through our fields
        $.each(P_fields, function(d, i) {
            
            // Define new button element
            var r = $('<button class="field_button" axis="'+P_axis+'" id="'+i+'"> '+i+' </button>');
            
            // Bind click event to new element
            r.on('click', function() { 
                show_object('svg');

                // Disable buttons
                $('.field_button').prop('disabled', true);
                setTimeout(function() {
                    $('.field_button').prop('disabled', false);
                },   3000);
                
                $("button[axis='"+P_axis+"']").removeClass("clicked");
                $(this).addClass("clicked");
                
            });
            
            // Append new element
            $("."+P_axis+" .axis_buttons"  )
                .append( r.prop('disabled', true) )
                .hide();
                                                   
        });
                        
    };

    // Fades in an object 
    function show_object (P_object) {
     
        $(P_object).fadeIn(2000);

    };

    // Removes an object
    function remove_object(P_object, callback) {
        
        if ($('.'+P_object).length) {
            $('.'+P_object).fadeOut(1000, function() { $(this).remove(); });
            setTimeout(function() {
                callback();   
            },   1000);  
        } else {
            callback(); 
        };
    };
                    
     