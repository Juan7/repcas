const routes = [
  { path: '/', name: 'invoices', component: InvoicesView },
  { path: '/productos', name: 'products', component: ProductsView },
  { path: '/cotizaciones', name: 'quotations', component: QuotationsView },
  { path: '/carrito-de-compras', name: 'cart', component: CartView }
]


const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
	el: '#app'
})

Vue.filter('date', str => moment(str).format('DD/MM/YYYY'))

Vue.http.interceptors.push((request, next) => {
   request.headers.set('X-CSRFToken', getCookie('csrftoken'))
   next()
})

function getCookie(name) {
    var cookieValue = null
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';')
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i])
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}
