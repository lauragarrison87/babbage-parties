async function drawStory(){

    // 1. access data
    let dataset = await d3.csv("./parties-imputed-date.csv")

    // helper functions to transform data /////
    const dateParser = d3.timeParse("%Y-%m-%d")
    const partyGuestCount = d3.rollup(dataset, D => D.length, d => d.date_imputed);//, (d) => d.guest);

    // this is another way to try to show the lines for each party guest 
    const partyGuest = d3.rollup(dataset, D => D.length,(d) => d.guest, d => d.date_imputed);
    console.log(partyGuest)

    let guests = Array.from(d3.group(dataset, (d) => d.guest).keys()); 

    let guestsDict = {}

    for (let g in guests) {
        // console.log(guests[g])
        // guestsDict.push({
        //     key: guests[g],
        //     value: Math.random() //just for now something to try 
        // })
        guestsDict[guests[g]] = Math.random() //TODO can I add this instead to the dataset as a new column? Would let me then get rid of guestsDict as its own separate thing 
    }

    // nested function for use in d3.filter() when drawing lines for each party guest 
    function pickByGuest(guest){
        return function pickGuest(d){
            return d.guest == guest
        }
    }

    // accessor functions for charting //////
    const xAccessor = d => dateParser(d.date_imputed)
    const yAccessor = d => guestsDict[d.guest]
    const sizeAccessor = d => partyGuestCount.get(d.date_imputed)

    console.log(xAccessor(dataset[0]))
    //console.log(yAccessor(dataset[0]))
   
    
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
        .domain(d3.extent(dataset, xAccessor))
        .range([0, (dimensions.boundedWidth - 2)])
        .nice()

    const yScale = d3.scaleLinear()
        .domain(d3.extent(dataset, yAccessor))
        .range([dimensions.boundedHeight, 0])
        .nice()

    // 5. draw data 
    const lineGenerator = d3.line()
        .x(d => xScale(xAccessor(d)))
        .y(d => yScale(yAccessor(d)))
        //.curve(d3.curveNatural)

    for (let g in guests) {
        //console.log(guests[g])
        const line = bounds.append("path")
            .attr("d", lineGenerator(dataset.filter(pickByGuest(guests[g])))) // .filter() expects the name of a function that takes 1 argument
            .attr("fill", "none")
            .attr("stroke", "#af9358")
            .attr("stroke-width", 2)
    }

    const dots = bounds.selectAll("circle")
        .data(dataset)
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

    // Tooltips
    bounds.selectAll("circle")
        .on("mouseenter", onMouseEnter)
        .on("mouseleave", onMouseLeave)

    const tooltip = d3.select("#tooltip")
    
    function onMouseEnter(e, d) {
        
        //get the x and y coord of dot, offset by left and right margins
        const x = xScale(xAccessor(d))
        + dimensions.margin.left
        const y = yScale(yAccessor(d))
        + dimensions.margin.top

        tooltip.select("#names")
            .text(d.guest)


        tooltip.style("transform", `translate(`
        + `calc(3% + ${x}px),`
        + `calc(-5% + ${y}px)`
        + `)`)
       
        tooltip.style("opacity", 1) 
        //tooltip.style("background",'#BCC5F7');  
    }

    function onMouseLeave() {
        tooltip.style("opacity", 0)

    }

}

drawStory();