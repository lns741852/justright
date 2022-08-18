export default function authHeader() {
    let user = JSON.parse(localStorage.getItem('user'));
    
    if (user && user.token) {
        // for Node.js Express back-end
        // return { 'x-access-token': user.accessToken };
        return { 'token': user.token };
    } else {
        return {};
    }
    // return { 'token': token };
}