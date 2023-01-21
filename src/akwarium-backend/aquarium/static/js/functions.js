// md - measurementDevices
async function getMetricsCounter() {
    return await getMetrics()
}

// ed - executiveDevices
async function displayExecutiveDevicesCounter() {
    const edBlock = document.getElementById('executiveDevicesNumber')
    const edResult = await getExecutiveDevice()
    edBlock.innerText = edResult.length
}

function addGraph(title, id) {
    const container = document.createElement("div")
    container.classList.add("w-full", "md:w-1/2", "p-3")

    const innerContainer = document.createElement("div")
    innerContainer.classList.add("bg-white", "border", "rounded", "shadow")

    const innerContainerTitle = document.createElement("div")
    innerContainerTitle.classList.add("border-b", "p-3")

    const graphTitle = document.createElement("h5")
    graphTitle.classList.add("font-bold", "uppercase", "text-gray")
    graphTitle.appendChild(document.createTextNode(title))

    innerContainerTitle.appendChild(graphTitle)

    const chartJsContainer = document.createElement("div")
    chartJsContainer.classList.add("p-5")
    const canvas = document.createElement("canvas")
    canvas.id = id
    canvas.width = undefined
    canvas.height = undefined
    chartJsContainer.appendChild(canvas)


    innerContainer.appendChild(innerContainerTitle)
    innerContainer.appendChild(chartJsContainer)

    container.appendChild(innerContainer)
    return container
}

function printGraphs(metrics) {
    console.log(metrics)
    const graphsBlock = document.getElementById('graphsFlexBox')
    metrics.forEach(metric => {
        const newGraph = addGraph(`${metric.device.name} - ${metric.parameter.name}`, `metric-${metric.id}`)
        graphsBlock.appendChild(newGraph)
    })
}