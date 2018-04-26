const ProductsView = Vue.component('ProductsView', {
  template: '#products-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      products: [],
      cart: {},
      cartUniqueProducts: [],
      cartProducts: 0
    }
  },

  mounted: function () {
    this.fetchData()
  },
  methods: {
  	fetchData: function () { _.debounce(this.fetchProducts, 500)() },

    fetchProducts: function () {
      const apiUrl = '/inventory/api/products/'

      this.$http.get(apiUrl).then(response => {
        this.products = response.body.results;
      }, response => {
        console.log('error')
      })
    },

    addToCart: function (product) {
    	this.cart[product.id] = product
    	this.cartUniqueProducts = Object.values(this.cart).filter(item => item.orderQuantity > 0)
    	this.cartProducts = 0
    	for (let i = 0; i < this.cartUniqueProducts.length; i++) {
    		this.cartProducts += parseInt(this.cartUniqueProducts[i].orderQuantity)
    	}
    }
  }
})
