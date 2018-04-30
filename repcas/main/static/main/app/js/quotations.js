const QuotationsView = Vue.component('QuotationsView', {
  template: '#quotations-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      quotation: { id: undefined },
      quotations: []
    }
  },

  watch: {
    '$route': function () {
      if (this.$route.name === 'quotations') {
        this.fetchData()
      }
    },
  },

  mounted: function () {
    this.fetchData()
  },

  methods: {
    fetchData: function() {
    	const apiUrl = '/accounting/api/quotations/'

      this.$http.get(apiUrl).then(response => {
        this.quotations = response.body.results
      }, response => {
        console.log('error')
      })
    },

    fetchQuotation: function() {
			const apiUrl = '/accounting/api/quotations/' + this.quotation.id

      this.$http.get(apiUrl).then(response => {
        this.quotation = response.body
      }, response => {
        console.log('error')
      })    	
    }
  }
})
