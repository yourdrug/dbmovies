new Vue({
    el: '#movies',
    data: {
        movies_list: []
    },
    created: function() {
        const vm = this;
        axios.get('/movie/')
        .then(function(response){
        vm.movies_list = response.data
        })

    }
}

)
