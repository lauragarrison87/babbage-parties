async function drawStory(url){

    // 1. access data
    let guests = await d3.json(url)
    console.log(guests[1])

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
        .domain([dateParser("1830-01-01"),dateParser("1850-01-01")])
        .range([0, (dimensions.boundedWidth - 2)])
        .nice()

    const yScale = d3.scaleLinear()
        .domain([0,1])
        .range([dimensions.boundedHeight, 0])
        .nice()


    // 5. draw data 
    console.log("AAARGH", guests);


    const xAccessor = p => dateParser(p.year + "-" + p.month + "-" + p.day);
    const yAccessor = p => p.ypos;

    const lineGenerator = d3.line()
        .x(p => xScale(xAccessor(p)))
        .y(p => yScale(yAccessor(p)))
        .curve(d3.curveNatural)

    let guest_group = bounds.selectAll('sdhfbsdjh')
        .data(guests)
        .enter()
        .append('g').text(g => g.name)

    guest_group.append("path")
        .attr("d", g => lineGenerator(g.parties)) 
        .attr("fill", "none")
        .attr("stroke", "#af9358")
        .attr("stroke-width", 2)

    guest_group.selectAll("circle")
        .data(g => g.parties)
        .enter().append("circle")
            .attr("cx", d => xScale(xAccessor(d)))
            .attr("cy", d => yScale(yAccessor(d)))
            .attr("r", 4)


    // 6. draw peripherals 
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale)

    const xAxis = bounds.append("g")
        .call(xAxisGenerator)
        .style("transform", `translateY(${
            dimensions.boundedHeight
        }px)`)


    // 7. Interaction stuff 

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
