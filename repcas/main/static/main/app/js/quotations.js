const QuotationsView = Vue.component('QuotationsView', {
  template: '#quotations-view',
  delimiters: ['[[', ']]'],
  mixins: [paginationMixin],
  data: function () {
    return {
      quotation: { id: undefined },
      quotations: [],
      filters: {
      }
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
      this.filters.page = this.pagination.page
      const params = { params: this.filters }

      this.$http.get(apiUrl, params).then(response => {
        this.quotations = response.body.results
        this.setPagination(response)
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
