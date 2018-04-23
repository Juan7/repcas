const routes = [
  { path: '/', name: 'invoices', component: InvoicesView },
  { path: '/productos', name: 'products', component: ProductsView },
  { path: '/cotizaciones', name: 'quotations', component: QuotationsView },
]


const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
	el: '#app'
})

Vue.filter('date', str => moment(str).format('DD/MM/YYYY'))
