
                
    function make_grouped_bar (P_data, x) {
        
        
        // Get keys of data which are distinct values of z
        var keys =  d3.keys(P_data[0]).filter(function(d) {return d !== 'Banding'; });
        
        // Define our scales.
        // We will set the range once we have loaded the data. 
        var xScale0 = d3.scaleBand()
                        .rangeRound([0, w])
                        .paddingInner(0.1);

        var xScale1 = d3.scaleBand()
            .padding(0.05);

        var yScale = d3.scaleLinear() 
            .rangeRound([h, 0]);

        var zScale = d3.scaleOrdinal();
       
        //Define the domains of our scales
        xScale0.domain(P_data.map(function(d) { return d['Banding']; }));

        xScale1.domain(keys).rangeRound([0, xScale0.bandwidth()]);

        yScale.domain([0, d3.max(P_data, function(d) { return d3.max(keys, function(key) { return d[key]; }); })]).nice();
                   
        zScale.range(['red', 'green']);
        
        // update axes
        update_axes(P_data, xScale0, yScale);
            
        // Create our grouping for our bars
        var band = svg.append("g")
                      .selectAll("g")
                      .data(P_data)
                      .enter().append("g")
                      .attr("transform", function(d) { return "translate(" + xScale0(d['Banding']) + ",0)"; })
        
        // Append rect to our svg
        band.selectAll("rect")
            .data(function(d) { return keys.map(function(key) { return {key: key, value: d[key]}; }); })
            .enter()
            .append("rect")
              .attr('id', function(d) { return d.key; })
              .attr("x", function(d) { return xScale1(d.key); })
              .attr("y", h)
              .attr("width", xScale1.bandwidth())
              .attr("height", 0)
              .attr("fill", function(d, i) { return zScale(i); })
              .attr('fill-opacity', 0.75);
              
        band.selectAll("rect")
            .data(function(d) { return keys.map(function(key) { return {key: key, value: d[key]}; }); })
            .transition()
            .duration(dur)
            .attr("y", function(d) { return yScale(d.value); })
            .attr("height", function(d) { return h - yScale(d.value ); })
            
        };  

    function make_scatter(P_data, x, y, r, z, t) {
                                    
        // Define our scales.
        // We will set the range once we have loaded the data. 
        var xScale = d3.scaleLinear()
                       .range([0, w]);
                                
        var yScale = d3.scaleLinear()
                       .range([h, 0]);
                       
        var rScale = d3.scaleLinear()
                       .range([0.1, 2]);
                       
                                    
        //Define the domains of our scales
        xScale.domain([0, d3.max(P_data, function(d) {return d[x]; })]);
        
        yScale.domain([0, d3.max(P_data, function(d) {return d[y]; })]);
                            
        // update axes
        update_axes(P_data, xScale, yScale);
       
        // Append points to our svg
        svg.append('g')
           .attr('clip-path', '#chart-area')
           .selectAll("circle")
           .data(P_data)
           .enter()
           .append("circle")
           .attr("cx", w/2)
           .attr("cy", h/2)
           .attr("r", 4)
           .attr('id', function(d) {
               return d[z];
           })
           .attr('title', function(d) {
               return d[t];
           })               
           .attr("fill-opacity", 0)
           .attr("fill", "white")
           .on('mouseover', function(d) {
           
              var xPosition = parseFloat(d3.select(this).attr("cx")) + 7;
              var yPosition = parseFloat(d3.select(this).attr("cy")) - 7;
              
               svg.append('text')
                  .attr('id', 'tooltip')
                  .attr('x', xPosition)
                  .attr('y', yPosition)
                  .attr("text-anchor", "left")
                  .attr("font-family", "sans-serif")
                  .attr("font-size", "11px")
                  .attr("fill", "grey")
                  .text(d[t]);
            })
            .on("mouseout", function() {

                //Remove the tooltip
                d3.select("#tooltip").remove();

            })
           
        svg.selectAll('circle')
           .transition()
           .duration(dur)
           .attr("cx", function(d) {
               return xScale(d[x]);
           })
           .attr("cy", function(d) {
               return yScale(d[y]);
           })
           .attr("r",function(d) {
               return 3;
           })
           .attr("fill-opacity", 0.75)
           .attr("fill", function(d){
               if (d[z] == 0) {
                   return 'red';
              } else {
                   return 'green';
              }
           });
               
    };
                        
        
    function update_axes(P_data, xScale, yScale) {

        // Reset the axis
        var format_axis_label = function() {

            // set default attributes
            var rotate = "rotate(0)";
            var anchor = "middle";
            var dx = '0em';
            var dy = '1em';
            
            // if graph is 'bar'
            //    and axis label length > bandwidth
            // then overwrite default parameters
            if ( graph == 'bar' ) {
                if ( ( w / P_data.length ) - (d3.max(P_data, function(d) {return d['Banding'].length; })*5) < 6 ) {
                    rotate = "rotate(-20)"
                    anchor = "end";
                    dx = "-.3em";
                    dy = ".15em";
                }
            };
            
            return {'rotation':rotate, 'anchor':anchor, 'dx':dx, 'dy':dy}
            
        };

        var axis_format = format_axis_label();
        
        yAxis.scale(yScale)
             .ticks(5)
             .tickFormat(d3.format(".1s"));
                    
        xAxis.scale(xScale)
             .ticks(5)
             .tickFormat(d3.format(".3s"));
        
        yAxis.scale(yScale)
             .ticks(5);
        
        xAxis.scale(xScale)
             .ticks(5);
        
        svg.select('.y.axis')
            .transition()
            .duration(dur)
            .call(yAxis);                

        svg.select(".x.axis")
            .transition()
            .duration(dur)
            .call(xAxis)
            .selectAll('text')
                .style("text-anchor", axis_format['anchor'])
                .attr("dx", axis_format['dx'])
                .attr("dy", axis_format['dy'])
                .attr("transform", function(d) {
                    return axis_format['rotation']
                    });
                    
        // Append y axis label
        svg.append("text")
           .attr('class', 'label')
           .attr("transform", "rotate(-90)")
           .attr("y", 0 - margin.left)
           .attr("x",0 - h / 2)
           .attr("dy", "1em")
           .style("text-anchor", "middle")
           .attr("font-family", "sans-serif")
           .attr("font-size", "14px")
           .attr("fill", "white")
           .text(y)
           .transition()
           .duration(2500)
           .attr('fill', 'grey')
           
        // Append x axis label
        svg.append('text')
           .attr('class', 'label')
           .attr('x', w/2)
           .attr('y', h + margin.bottom)
           .style('text-anchor', 'middle')
           .attr("font-family", "sans-serif")
           .attr("font-size", "14px")
           .attr("fill", "white")
           .text(x)
           .transition()
           .duration(dur)
           .attr('fill', 'grey');
                    
    };   
    
    function update_z_colors(button_id) {
        
        console.log(button_id)
        // function which toggles opacity
        var toggle_opacity = function(opacity) {
            if (opacity == 0) {
                return 0.75
            } else {
                return 0
            }
        };                      
        
        // set element - circle or rect
        var element;
        if ( graph == 'bar' ) {
            element = 'rect';
        } else {
            element = 'circle';
        };
        
        // toggle opacity
        svg.selectAll(element)
            .transition()
            .duration(1000)
            .attr("fill-opacity", function(d) {
                if (button_id == 'toggle') {
                    return toggle_opacity(d3.select(this).attr('fill-opacity'));
                } else if ( button_id == d3.select(this).attr('id')) {
                    return toggle_opacity(d3.select(this).attr('fill-opacity'));
                } else {
                    return d3.select(this).attr('fill-opacity');
                }
            });
    };    
    
    function remove_data(graph) {

        yAxis.scale(fyScale);
        xAxis.scale(fxScale); 

        svg.select(".y.axis")
           .transition()
           .duration(dur)
           .call(yAxis);
           
        svg.select(".x.axis")
           .transition()
           .duration(dur)
           .call(xAxis);
           
        svg.selectAll('.label')
           .transition()
           .duration(dur)
           .attr('fill', 'white')
           .remove();
        
        if ( graph == 'bar' ) {                          
            svg.selectAll("rect")
               .transition()
               .duration(dur)
               .attr("y", h)
               .attr("height", 0)
               .attr("fill-opacity", 0)
               .remove()
        } else {
            svg.selectAll("circle")
               .transition()
               .duration(2500)
               .attr("cx", w/2)
               .attr("cy", h/2)
               .attr("r", 4)
               .attr("fill", 'white')
               .remove()
        };

    };