export default class schedule {
    constructor(shift_no, emp_no, date, punch_in, punch_out, text) {
        this.shift_no = shift_no;
        this.emp_no = emp_no;
        this.date = date;
        this.punch_in = punch_in;
        this.punch_out = punch_out;
        this.text = text;
    }
}