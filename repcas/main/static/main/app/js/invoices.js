const InvoicesView = Vue.component('InvoicesView', {
  template: '#invoices-view',
  delimiters: ['[[', ']]'],
  mixins: [paginationMixin],
  data: function () {
    return {
      invoices: [],
      filters: {
        'is_payed': false,
        'number__icontains': undefined,
        'client__name__icontains': undefined
      }
    }
  },
  watch: {
    'filters.is_payed': function () {
      this.fetchData()
    },

    'filters.number__icontains': function () {
      this.filters.client__name__icontains = this.filters.number__icontains
      this.fetchData()
    }
  },
  mounted: function () {
    this.fetchData()
  },
  methods: {
    fetchData: function () { _.debounce(this.fetchInvoices, 200)() },

    fetchInvoices: function () {
      const apiUrl = '/accounting/api/invoices/'
      this.filters.page = this.pagination.page

      const params = { params: this.filters }

      this.$http.get(apiUrl, params).then(response => {
        this.invoices = response.body.results;
        this.setPagination(response)
        console.log(this.invoices)
      }, response => {
        console.log('error')
        // error callback
      })
    },

    showReport: function () {
      const parsedFilters = $.extend({}, this.filters)
      parsedFilters.date__gte = new Date()

      const startDate = moment(parsedFilters.date__gte, 'YYYY-MM-DD').toDate()
      parsedFilters.date__gte = moment(startDate).subtract(60, 'days').toISOString()

      const apiUrl = '/accounting/api/invoices-report/'
      const params = {
        params: parsedFilters
      }

      const url = apiUrl + this.objectToQuerystring(params.params)
      console.log(url)
      window.open(url, 'Download')
    },

    objectToQuerystring (obj) {
      return Object.keys(obj).reduce((str, key, i) => {
        var delimiter, val
        delimiter = (i === 0) ? '?' : '&'
        key = encodeURIComponent(key)
        val = encodeURIComponent(obj[key])
        return [str, delimiter, key, '=', val].join('')
      }, '')
    }
  }
})
