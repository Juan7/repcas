const paginationMixin = {
	data: function () {
		return {
			pagination: {
				page: 1,
				count: undefined,
				next: undefined,
				previous: undefined,
				numbers: undefined
			}
		}
	},
	watch: {
		'pagination.page': function () {
			this.fetchData()
		}
	},
  methods: {
    setPagination: function (response) {
    	this.pagination.count = response.body.count
    	this.pagination.next = response.body.next
    	this.pagination.previous = response.body.previous
    	this.pagination.numbers = response.body.numbers
    }
  }
}
