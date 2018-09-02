import config from 'config';

const envConfig = config[__ENV_BUILD__] || {};
envConfig['environment'] = __ENV_BUILD__;
envConfig['isDevelop'] = __ENV_BUILD__ === 'develop';

export default {
    get(config_name) {
        if(envConfig[config_name] === undefined) {
            console.error(`Config ${config_name} is not defined in ${__ENV_BUILD__}`);
        }
        return envConfig[config_name];
    }
};
