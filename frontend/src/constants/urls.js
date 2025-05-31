const baseURL = '/api'

const auth = '/auth'
const sellers = '/sellers'
const auto_salon = '/auto_salon'
const admin = '/admin'


const urls = {
    auth: {
        login: auth,
        siteRole: `${auth}/site_role`,
        refresh: `${auth}/refresh`,
        socket: `${auth}/socket`
    },
    sellers,
    auto_salon,
    admin
}







export {baseURL, urls}