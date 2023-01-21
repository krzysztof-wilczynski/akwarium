async function getMetrics(id = undefined) {
    try {
        // TODO: kurwa mam jakieś zaćmienie umysłu,
        //  to nie może tak wyglądać
        let URL = '/api/device_parameter'
        if (id) {
            URL += `?id=${id}`
        }
        const {data} = await axios.get(URL)
        return data
    } catch (error) {
        console.log(error)
    }
}

async function getExecutiveDevice(id = undefined) {
    try {
        let URL = '/api/executive_device'
        if (id) {
            URL += `?id=${id}`
        }
        const {data} = await axios.get(URL)
        return data
    } catch (error) {
        console.log(error)
    }
}