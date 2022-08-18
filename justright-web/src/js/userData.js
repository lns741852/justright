

export default function userData() {
    let user = localStorage.getItem('user')
    user = JSON.parse(user)

    return user
}