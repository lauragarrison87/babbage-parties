async function drawBalloons(url){

    // 1. access data
    let parties = await d3.json(url)
    //console.table(parties[0])

    const partySizeFactor = 4
   
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
    const svg = d3.select("#storylines")
    .append("svg")
      .attr("width", dimensions.width)
      .attr("height", dimensions.height)

    const drawArea = svg.append("g")
        .style("transform", `translate(${
            dimensions.margin.left
        }px, ${
            dimensions.margin.top
        }px)`)
    
    drawArea.append("defs").append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", dimensions.boundedWidth)
        .attr("height", dimensions.boundedHeight)
        
    drawArea.attr("clip-path","url(#clip)");


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


    let party_group = drawArea.selectAll("g")
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
        .attr("r", p => p.party_size * partySizeFactor)
        .attr("fill", "pink")
        .attr("stroke", "gray")
        .attr("class", "zoomable")
    

    // 6. draw peripherals 
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale)

    const xAxis = svg.append("g") 
        .call(xAxisGenerator)
        .style("transform", `translate(${
            dimensions.margin.left
        }px, ${
            dimensions.boundedHeight + dimensions.margin.top
        }px)`)

    xAxis.append("text")
        .attr("class", "axis-label")
        .attr("x", dimensions.boundedWidth/2)
        .attr("y", dimensions.margin.bottom)
        .attr("fill","black")
        .style("font-size", "1.3em")
        .text("Date of event")

    // 7. Interaction 

    // Creating a zoom object
    var zoom = d3.zoom()
      .scaleExtent([0.5, 7])
      .extent([[0, 0], [dimensions.boundedWidth, dimensions.boundedHeight]])
      .on('zoom', updateZoom);

    svg
      .style('pointer-events', 'all')
      .call(zoom);

    // function to redraw while zooming (from https://stackoverflow.com/questions/66808447/how-can-i-zoom-into-this-graph-using-d3v6)
    function updateZoom(event) {
      // get the new scale
      var transform = event.transform;
      var newX = transform.rescaleX(xScale);
      var newY = transform.rescaleY(yScale);

      // update the axes
      xAxis.call(d3.axisBottom(newX));


      // update the chart
      d3.selectAll("line.zoomable")
        .attr("x1", p => newX(xAccessor(p)))
        .attr("y1", p => newY(yAccessor(p)))
        .attr("x2", p => newX(xAccessor(p)))
        //.attr("y2", dimensions.boundedHeight)


      d3.selectAll('circle.zoomable')
          .attr('cx', p => newX(xAccessor(p)))
          .attr('cy', p => newY(yAccessor(p)))
          .attr('r',  p => p.party_size * partySizeFactor * transform.k)
    
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
