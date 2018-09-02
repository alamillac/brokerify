import 'whatwg-fetch';
import Logger from 'plugins/logger';
import config from "plugins/app-config";
//import error_codes from "plugins/errors";


const logger = Logger.createLogger("Api");
const useCors = config.get("useCors", false),
    baseUrl = config.get("baseUrl", "");

function queryParams(params) {
    return Object.keys(params)
        .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
        .join('&');
}

function buildUrl(baseUrl, _params) {
    const params = _params || {},
        getParams = queryParams(params);
    if(!getParams) {
        return baseUrl;
    }
    return baseUrl + "?" + getParams;
}

const request = (url, args) => {
    return fetch(baseUrl + url, args).then((response) => {
        if(response.ok) {
            return response.json();
        }
        return Promise.reject(response);
    });
};


const headers = {'Content-Type': 'application/json'},
    credentials = useCors? 'include': 'same-origin'; //"include" for cross-origin requests else "same-origin"


const Api = {
    get(url, getParams) {
        const method = "GET";
        logger.debug(method +" "+url);

        return request(
            buildUrl(url, getParams),
            {headers, method, credentials}
        );
    },
    post(url, params) {
        const method = "POST";
        logger.debug(method +" "+url);

        const body = JSON.stringify(params);
        return request(url, {headers, method, body, credentials});
    },
    put(url, params) {
        const method = "PUT";
        logger.debug(method +" "+url);

        const body = JSON.stringify(params);
        return request(url, {headers, method, body, credentials});
    },
    delete(url, params) {
        const method = "DELETE";
        logger.debug(method +" "+url);

        const body = JSON.stringify(params);
        return request(url, {headers, method, body, credentials});
    }
};

export default Api;
