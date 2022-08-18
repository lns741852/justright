import axios from 'axios'
import API_URL from '../js/API'

const API = API_URL(API) + '/'

const service = axios.create({
    responseType: 'arraybuffer'
})
service.interceptors.request.use(config => {
    config.headers['Authorization'] = localStorage.getItem("authorization");
    return config
}, error => {
    console.log(error)
});

service.interceptors.response.use(
    resp => {
        const headers = resp.headers;
        let reg = RegExp(/application\/json/);
        if (headers['content-type'].match(reg)) {
            alert(resp["Response"]["msg"])
            resp.data = uintToString(resp.data);
        } else {

            let fileDownload = require('js-file-download');
            // let fileName = headers["content-disposition"].split(";")[1].split("filename=")[1];
            let contentType = headers["content-type"];
            let fileName = decodeURIComponent("員工月報表.xlsx");
            fileDownload(resp.data, fileName, contentType)
        }
    }, error => {
        alert("查詢無資料")
        console.log(error);
    }
);
let base = API;
export const downloadRequest = (url, params) => {
    return service({
        method: 'get',
        url: `${base}${url}`,
        params
    })
}

function uintToString(uintArray) {
    let encodedString = String.fromCharCode.apply(null, new Uint8Array(uintArray)),
        decodedString = decodeURIComponent(escape(encodedString));
    return JSON.parse(decodedString);
}
export default service