/* eslint-disable no-use-before-define */
import axios from 'axios'
import API_URL from '../js/API'
import authHeader from './auth-header';
import { downloadRequest } from '../js/download';

// const API = API_URL(API) + '8000/'
const API = API_URL(API) + '/'

class UserServices {
    /** 登入驗證 */
    async tokenCheck() {
        let token = await authHeader();
        const data = await axios.post(API + 'HRCS/RefreshJWTToken', token).then(res => res.data);
        return data;
    }

    /** 取得員工資料 */
    async getEmpdata() {
        const data = await axios.get(API + 'HRCS/getEmpdata', {
            headers: authHeader()
        }).then(res => res.data);
        return data;
    }

    /** 新增員工資料 */
    async addEmpdata(empData) {
        await axios.post(API + 'HRCS/getEmpdata', empData, {
                headers: authHeader()
            })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function(error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 補打卡 */
    async addAttendanceData(attendanceData) {
        await axios.post(API + 'HRCS/attendanceData', attendanceData, {
                headers: authHeader()
            })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function(error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }



    /** 更新員工資料 */
    async updataEmpdata(empData) {
        await axios.put(API + 'HRCS/getEmpdata', empData, {
                headers: authHeader()
            })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function(error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 取得公司資料 */
    async getCompanydata() {
        const data = await axios.get(API + 'HRCS/getCompanydata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得部門資料 */
    async getDepdata() {
        const data = await axios.get(API + 'HRCS/getDepdata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得組別資料 */
    async getGroupdata() {
        const data = await axios.get(API + 'HRCS/getGroupdata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得職位資料 */
    async getWPdata() {
        const data = await axios.get(API + 'HRCS/getWorkpositionList', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得出勤狀況資料 */
    async getAttendancedata(attr) {
        const data = await axios.get(API + 'HRCS/getAttendanceEmpViewdata' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取消打卡 */
    async deleteAttendPunch(attend_no) {
        const data = await axios.post(API + 'HRCS/deleteAttendPunch', {
            attend_no
        }, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得排班表資料 */
    async getShiftdata(attr) {
        const data = await axios.get(API + 'HRCS/Shiftdata' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得時段資料 */
    async getTimePerioddata() {
        const data = await axios.get(API + 'HRCS/getTimePeriod', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 編輯時段資料 */
    async editTimePerioddata(attr) {
        const data = await axios.put(API + 'HRCS/getTimePeriod', attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 新增時段資料 */
    async addTimePerioddata(attr) {
        const data = await axios.post(API + 'HRCS/getTimePeriod', attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 新增排班表資料 */
    async addScheduledata(newSchedule) {
        let MSG = ""
        await axios.post(API + 'HRCS/Shiftdata', JSON.parse(newSchedule), {
                headers: authHeader()
            })
            .then(res => {
                if (res.data) {
                    MSG = {
                        code: res.status,
                        msg: res.data.status
                    }
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
            })
            .catch(function(error) {
                // console.log(error);
                if (error.res.data) {
                    MSG = error.res.data
                    localStorage.setItem('MSG', JSON.stringify(error.res.data))
                }
            })
        return MSG
    }

    /** 修改排班表資料 */
    async modShiftdata(shift) {
        await axios.put(API + 'HRCS/Shiftdata', JSON.stringify(shift), {
                headers: authHeader()
            })
            .then(res => {
                // console.log("modShiftdata", res);
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function(error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 刪除排班表資料 */
    async delShiftdata(shiftNo) {
        await axios.delete(API + 'HRCS/Shiftdata/' + shiftNo, {
                headers: authHeader()
            })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function(error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 出勤資料查詢 */
    async getAttendanceEmpViewQuery(attr) {
        const data = await axios.get(API + 'HRCS/getAttendanceEmpViewQuery' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 出勤資料查詢_Jay */
    async getShiftsAttendanceEmpViewQuery(attr) {
        const data = await axios.get(API + 'HRCS/getShiftsAttendanceEmpViewQuery' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 加班資料查詢 */
    async getWorkOvertimeQuery(attr) {
        const data = await axios.get(API + 'HRCS/getWorkOvertimeQuery' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 個人月報表匯出 */
    exportRMPdata(attr) {
        downloadRequest('HRCS/exportRMPQuery' + attr);
        // const data = axios.get(API + 'HRCS/exportRMPQuery' + attr, {
        //     headers: authHeader()
        // }).then(res => res.data)
        // return data
    }

    /** 取得公司資料(TEST) */
    async TESTgetEmpdata() {
        const data = await axios.get(API + 'TEST/getEmpdata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }
}

export default new UserServices()