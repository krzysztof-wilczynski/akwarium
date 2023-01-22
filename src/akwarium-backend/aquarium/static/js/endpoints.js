async function getMetrics(id = "") {
    try {
        const {data} = await axios.get(`/api/device_parameter/${id}`)
        return data
    } catch (error) {
        console.log(error)
    }
}

async function getExecutiveDevice(id = "") {
    try {
        const {data} = await axios.get(`/api/executive_device/${id}`)
        return data
    } catch (error) {
        console.log(error)
    }
}

async function getPointValues(id = "") {
    try {
        const {data} = await axios.get(`/api/point_value/?id=${id}`)
        return data
    } catch (error) {
        console.log(error)
    }
}

async function getSetpoints(id = "") {
    try {
        const {data} = await axios.get(`/api/setpoint/${id}`)
        return data
    } catch (error) {
        console.log(error)
    }
}

async function postSetpoints(data) {
    try {
        return await axios.post(`/api/update_setpoints/`, {data},
            {
                withCredentials: true,
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken'
            })
    } catch (error) {
        console.log(error)
    }
}