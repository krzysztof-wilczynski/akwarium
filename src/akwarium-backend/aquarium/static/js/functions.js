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
    const graphsBlock = document.getElementById('graphsFlexBox')
    const graphIDsList = []
    metrics.forEach(metric => {
        const ID = `metric-${metric.id}`
        const newGraph = addGraph(`${metric.device.name} - ${metric.parameter.name} [${metric.parameter.unit}]`, ID)
        graphIDsList.push(ID)
        graphsBlock.appendChild(newGraph)
    })
    return graphIDsList
}

async function createGraph(graphID) {
    const ctx = document.getElementById(graphID)

    const api_data = await getPointValues(graphID.split('-')[1])

    const labels = api_data.map(x => new Date(x.timestamp).toLocaleTimeString())
    const values = api_data.map(x => x.value)

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                fill: false,
                borderColor: 'rgb(107,107,107)',
                tension: 0.5
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    })
}

async function updateChart(chart) {
    const api_data = await getPointValues(chart.canvas.id.split('-')[1])
    const labels = api_data.map(x => new Date(x.timestamp).toLocaleTimeString())

    const first_new_label = labels[0]
    let new_entries = 0
    for (const old_label of chart.data.labels) {
        if (old_label === first_new_label) {
            break;
        } else {
            new_entries++
        }
    }

    if (new_entries > 0) {
        const new_data = api_data.reverse().slice(0, new_entries).map(x => x.value)
        chart.data.labels.push(labels.reverse().slice(0, new_entries))
        chart.data.datasets[0].data.push(new_data)

        chart.data.labels = chart.data.labels.splice(new_entries)
        chart.data.datasets[0].data = chart.data.datasets[0].data.splice(new_entries)
        chart.update()
    } else if (new_entries <= 0 && chart.data.labels.length < 50 &&
        chart.data.labels[chart.data.labels.length - 1] !== labels[labels.length - 1]) {
        const new_data = api_data.reverse().splice(0, labels.length - chart.data.labels.length).map(x => x.value)
        const new_labels = labels.reverse().splice(0, labels.length - chart.data.labels.length)
        chart.data.labels.push.apply(chart.data.labels, new_labels.reverse())
        chart.data.datasets[0].data.push.apply(chart.data.datasets[0].data, new_data.reverse())
        chart.update()
    }
}