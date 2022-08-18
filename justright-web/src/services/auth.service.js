import axios from 'axios';

import API from '../js/API'

const API_URL = API(API_URL) + "/"

class AuthService {
    /** 登入 */
    async login(user) {
        let data = await axios
            .post(API_URL + 'HRCS/Login', user)
            .then(response => response.data)
            .catch(error => error)
            // console.log(data);
        if (data.Response[0].token !== undefined) {
            localStorage.setItem('user', JSON.stringify(data.Response[0]));
            return data.Response[0]
        } else {
            if (data.Response !== undefined) {
                data = data.Response
            }
            // console.log(data);
            return data
        }
    }

    /** 寄出重置代碼 */
    async resetCode(empNo, empMail, deadLine, url) {
        let data = await axios
            .post(API_URL + 'HRCS/ForgetPassword', {
                emp_no: empNo,
                mail: empMail,
                deadline: deadLine,
                url: url
            })
            .then(response => response.data)
            .catch(error => error)
        return data
    }

    /** 驗證重置密碼的token */
    async checkResttoken(token) {
        let data = await axios
            .post(API_URL + 'HRCS/verifyReset', {
                token: token,
            })
            .then(response => response.data)
            .catch(error => error)
        return data
    }

    /** 重設密碼 */
    async resetPW(resetData) {
        let data = await axios
            .post(API_URL + 'HRCS/ResetPassword', resetData)
            .then(response => response.data)
            .catch(error => error)
        return data
    }

    /** 登出，並清除localStorage */
    logout() {
        localStorage.clear();
    }
}

export default new AuthService();