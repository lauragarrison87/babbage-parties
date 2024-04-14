async function drawBalloons(url){

    // 1. access data
    let parties = await d3.json(url)
    console.table(parties[0])
   
    // helper functions to transform data /////
    const dateParser = d3.timeParse("%Y-%m-%d")
    
    // 2. create chart dimensions
    let dimensions = {
    width: window.innerWidth * 0.85,
    height: window.innerHeight * 0.9,
    margin: {
        top: 10,
        right: 10,
        bottom: 50,
        left: 50,
    },
    }
    dimensions.boundedWidth = dimensions.width
    - dimensions.margin.left
    - dimensions.margin.right
    dimensions.boundedHeight = dimensions.height
    - dimensions.margin.top
    - dimensions.margin.bottom


    // 3. draw canvas 
    const wrapper = d3.select("#storylines")
    .append("svg")
      .attr("width", dimensions.width)
      .attr("height", dimensions.height)

    const bounds = wrapper.append("g")
        .style("transform", `translate(${
            dimensions.margin.left
        }px, ${
            dimensions.margin.top
        }px)`)


    // 4. create scales 
    const xScale = d3.scaleTime()
        .domain([dateParser("1830-01-01"),dateParser("1851-01-01")])
        .range([0, (dimensions.boundedWidth - 2)])
        .nice()

    const yScale = d3.scaleLinear()
        .domain([0,1])
        .range([dimensions.boundedHeight, 0])
        .nice()


    // 5. draw data 
    const xAccessor = p => dateParser(p.year + "-" + p.month + "-" + p.day);
    const yAccessor = p => p.ypos;


    let party_group = bounds.selectAll("g")
        .data(parties)
        .enter()
        .append("g")
        .attr("id", p =>p.pid)

    party_group.append("line")
        .attr("x1", p => xScale(xAccessor(p)))
        .attr("y1", p => yScale(yAccessor(p)))
        .attr("x2", p => xScale(xAccessor(p)))
        .attr("y2", dimensions.boundedHeight)
        .attr("stroke", "gray")
        .attr("class", "zoomable")

    
    party_group.append("circle")
        .attr("cx", p => xScale(xAccessor(p)))
        .attr("cy", p => yScale(yAccessor(p)))
        .attr("r", p => p.party_size * 4)
        .attr("fill", "pink")
        .attr("stroke", "gray")
        .attr("class", "zoomable")
    

    // 6. draw peripherals 
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale)

    const xAxis = bounds.append("g")
        .call(xAxisGenerator)
        .style("transform", `translateY(${
            dimensions.boundedHeight
        }px)`)

    const yAxisGenerator = d3.axisLeft()
        .scale(yScale)

    const yAxis = bounds.append("g")
        //.call(yAxisGenerator)
        // .style("transform", `translateX(${
        //     0
        // }px)`)


    // 7. Interaction stuff 

    // Creating a zoom object
    var zoom = d3.zoom()
      .scaleExtent([0.5, 20])
      .extent([[0, 0], [dimensions.boundedWidth, dimensions.boundedHeight]])
      .on('zoom', updateZoom);

    wrapper
      .style('pointer-events', 'all')
      .call(zoom);

    // function to redraw while zooming (from https://stackoverflow.com/questions/66808447/how-can-i-zoom-into-this-graph-using-d3v6)
    function updateZoom(event) {
      console.log('zoomed')
      // get the new scale
      var transform = event.transform;
      var newX = transform.rescaleX(xScale);
      var newY = transform.rescaleY(yScale);

      // update the axes
      xAxis.call(d3.axisBottom(newX));
      //yAxis.call(d3.axisLeft(newY));


      // update the chart
      d3.selectAll("line.zoomable")
        .attr("x1", p => newX(xAccessor(p)))
        .attr("y1", p => newY(yAccessor(p)))
        .attr("x2", p => newX(xAccessor(p)))
        //.attr("y2", dimensions.boundedHeight)


      d3.selectAll('circle.zoomable')
          .attr('cx', p => newX(xAccessor(p)))
          .attr('cy', p => newY(yAccessor(p)))
          .attr('r',  p => p.party_size * 4 * transform.k)
    
    }
    // // Tooltips
    // bounds.selectAll("circle")
    //     .on("mouseenter", onMouseEnter)
    //     .on("mouseleave", onMouseLeave)

    // const tooltip = d3.select("#tooltip")
    
    // function onMouseEnter(e, d) {
        
    //     //get the x and y coord of dot, offset by left and right margins
    //     const x = xScale(xAccessor(d))
    //     + dimensions.margin.left
    //     const y = yScale(yAccessor(d))
    //     + dimensions.margin.top

    //     tooltip.select("#names")
    //         .text(d.guest)


    //     tooltip.style("transform", `translate(`
    //     + `calc(3% + ${x}px),`
    //     + `calc(-5% + ${y}px)`
    //     + `)`)
       
    //     tooltip.style("opacity", 1) 
    //     //tooltip.style("background",'#BCC5F7');  
    // }

    // function onMouseLeave() {
    //     tooltip.style("opacity", 0)

    // }

}
