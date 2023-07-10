import { axios } from '@/utils/request'

export function getDiscovery() {
    return axios({
        url: `/v0.1/adr`,
        method: 'GET'
    })
}

export function postDiscovery(data) {
    return axios({
        url: `/v0.1/adr`,
        method: 'POST',
        data
    })
}

export function putDiscovery(id, data) {
    return axios({
        url: `/v0.1/adr/${id}`,
        method: 'PUT',
        data
    })
}

export function deleteDiscovery(id) {
    return axios({
        url: `/v0.1/adr/${id}`,
        method: 'DELETE'
    })
}

export function getHttpCategories(name) {
    return axios({
        url: `/v0.1/adr/http/${name}/categories`,
        method: 'GET',
    })
}

export function getHttpAttributes(name, params) {
    return axios({
        url: `/v0.1/adr/http/${name}/attributes`,
        method: 'GET',
        params
    })
}

export function getSnmpAttributes(name) {
    return axios({
        url: `/v0.1/adr/snmp/${name}/attributes`,
        method: 'GET',
    })
}

export function getCITypeDiscovery(type_id) {
    return axios({
        url: `/v0.1/adt/ci_types/${type_id}`,
        method: 'GET',
    })
}

export function postCITypeDiscovery(type_id, data) {
    return axios({
        url: `/v0.1/adt/ci_types/${type_id}`,
        method: 'POST',
        data
    })
}

export function putCITypeDiscovery(adt_id, data) {
    return axios({
        url: `/v0.1/adt/${adt_id}`,
        method: 'PUT',
        data
    })
}

export function deleteCITypeDiscovery(id) {
    return axios({
        url: `/v0.1/adt/${id}`,
        method: 'DELETE'
    })
}

export function getADCCiTypes(params) {
    return axios({
        url: `/v0.1/adc/ci_types`,
        method: 'GET',
        params
    })
}

export function getADCCiTypesAttrs(type_id) {
    return axios({
        url: `/v0.1/adc/ci_types/${type_id}/attributes`,
        method: 'GET'
    })
}

export function updateADCAccept(adc_id) {
    return axios({
        url: `/v0.1/adc/${adc_id}/accept`,
        method: 'PUT'
    })
}

export function getAdc(params) {
    return axios({
        url: `v0.1/adc`,
        method: 'GET',
        params
    })
}

export function deleteAdc(adc_id) {
    return axios({
        url: `v0.1/adc/${adc_id}`,
        method: 'DELETE',
    })
}
