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

function printSetpoints(setpoints) {
    const elements = []

    setpoints.forEach(sp => {
        const tr = document.createElement('tr')
        tr.classList.add('border-b')

        const td1 = document.createElement('th')
        td1.setAttribute("scope", "row")
        td1.classList.add("px-6", "py-4", "font-medium", "text-gray-900", "whitespace-nowrap")
        const td1text = document.createTextNode(sp.parameter)
        td1.appendChild(td1text)

        const td2 = document.createElement('td')
        const td2text = document.createTextNode(sp.value)
        td2.classList.add("px-6", "py-4", "text-center")
        td2.appendChild(td2text)

        const td3 = document.createElement('td')
        td3.classList.add("px-6", "py-4")
        const input = document.createElement('input')
        input.classList.add("shadow", "appearance-none", "border", "rounded", "w-full", "py-2", "px-3", "text-gray-700", "leading-tight", "focus:outline-none", "focus:shadow-outline")
        input.setAttribute("id", sp.id)
        input.setAttribute("type", "number")
        input.setAttribute("placeholder", sp.value)
        input.setAttribute("value", sp.value)
        input.setAttribute("min", "0")
        input.setAttribute("step", "0.1")

        const errorP = document.createElement('p')
        errorP.classList.add("text-red-500", "text-xs", "italic")
        errorP.setAttribute('id', `error-${sp.id}`)

        td3.appendChild(input)
        td3.appendChild(errorP)

        tr.appendChild(td1)
        tr.appendChild(td2)
        tr.appendChild(td3)

        elements.push(tr)
    })
    return elements
}