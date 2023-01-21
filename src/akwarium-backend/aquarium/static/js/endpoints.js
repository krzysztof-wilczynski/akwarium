async function getMeasurementDevice(id = 0) {
    try {
        const {data} = axios.get(`/api/measuring_device?id=${id}`)
        return data
    } catch (error) {
        console.log(error)
    }
}